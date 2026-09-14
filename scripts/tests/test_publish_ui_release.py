"""Verify UI note publication without network access or publishing a release."""

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import publish_cli_release as publisher


class UiPublishTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.notes = self.root / 'ui-0.2.2.md'
        self.source = 'b' * 40
        self.notes.write_text(f'<!-- release\nsource: {self.source}\nchannel: staged\n-->\n\n# Card Factory UI 0.2.2\n\nChanges.\n')

    def assets(self, directory):
        for platform in ('macos-aarch64.dmg', 'windows-x64.msi'):
            name = f'card-factory-ui-0.2.2-{platform}'
            (directory / name).write_bytes(b'installer')
            (directory / (name + '.sha256')).write_text(f'{hashlib.sha256(b"installer").hexdigest()}  {name}\n')

    def test_product_heading_and_channel_are_explicit(self):
        self.assertEqual((self.source, 'staged'), publisher.parse_notes(self.notes)[:2])
        self.notes.write_text(self.notes.read_text().replace('UI 0.2.2', 'CLI 0.2.2'))
        with self.assertRaises(ValueError):
            publisher.parse_notes(self.notes)

    def test_exact_installers_and_checksums(self):
        directory = self.root / 'assets'
        directory.mkdir()
        with self.assertRaises(ValueError):
            publisher.verify_assets(directory, 'ui-0.2.2')
        self.assets(directory)
        publisher.verify_assets(directory, 'ui-0.2.2')
        with self.assertRaises(ValueError):
            publisher.verify_assets(directory, 'cli-0.2.2')
        (directory / 'card-factory-ui-0.2.2-windows-x64.msi').write_bytes(b'corrupt')
        with self.assertRaises(ValueError):
            publisher.verify_assets(directory, 'ui-0.2.2')

    def test_mixed_versions_or_extra_intel_assets_fail(self):
        directory = self.root / 'assets'
        directory.mkdir()
        self.assets(directory)
        with self.assertRaises(ValueError):
            publisher.verify_assets(directory, 'ui-0.2.3')
        (directory / 'card-factory-ui-0.2.2-macos-x64.dmg').write_bytes(b'extra')
        with self.assertRaises(ValueError):
            publisher.verify_assets(directory, 'ui-0.2.2')

    def test_published_notes_are_unchanged(self):
        with patch.object(publisher, 'gh', return_value=json.dumps({'isDraft': False})) as gh:
            publisher.publish(self.notes, 'owner/repo')
            self.assertEqual(1, gh.call_count)

    def test_source_mismatch_stops_before_download(self):
        with patch.object(publisher, 'gh', return_value=json.dumps({'isDraft': True, 'body': 'wrong'})) as gh:
            with self.assertRaises(ValueError):
                publisher.publish(self.notes, 'owner/repo')
            self.assertEqual(1, gh.call_count)

    def test_staged_stable_check_only_and_changed_draft(self):
        for channel, check_only, changed in [('staged', False, False), ('stable', False, False), ('staged', True, False), ('staged', False, True)]:
            with self.subTest(channel=channel, check_only=check_only, changed=changed):
                text = self.notes.read_text().replace('channel: staged', f'channel: {channel}').replace('channel: stable', f'channel: {channel}')
                self.notes.write_text(text)
                draft = {'isDraft': True, 'body': f'Source commit: `{self.source}`\n', 'assets': []}
                calls = []
                def fake_gh(*args):
                    calls.append(args)
                    if args[1] == 'view':
                        return json.dumps(draft if len(calls) == 1 or not changed else {**draft, 'isDraft': False})
                    if args[1] == 'download':
                        self.assets(Path(args[args.index('--dir') + 1]))
                    return ''
                with patch.object(publisher, 'gh', side_effect=fake_gh):
                    if changed:
                        with self.assertRaises(ValueError):
                            publisher.publish(self.notes, 'owner/repo')
                    else:
                        publisher.publish(self.notes, 'owner/repo', check_only)
                edits = [c for c in calls if c[1] == 'edit']
                self.assertEqual(0 if check_only or changed else 1, len(edits))
                if edits:
                    self.assertIn(f'--prerelease={str(channel == "staged").lower()}', edits[0])
                    self.assertIn('--latest=false', edits[0])


if __name__ == '__main__':
    unittest.main()
