"""Exercise publication gates without network access or release mutations."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import publish_cli_release as publisher


class PublishTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.notes = self.root / 'cli-0.2.3.md'
        self.source = 'a' * 40
        self.notes.write_text(f'<!-- release\nsource: {self.source}\nchannel: stable\n-->\n\n# Card Factory CLI 0.2.3\n\nChanges.\n')

    def assets(self, root):
        for platform in ('macos-aarch64', 'macos-x64', 'windows-x64'):
            name = f'card-factory-0.2.3-{platform}.zip'
            (root / name).write_bytes(b'archive')
            (root / (name + '.sha256')).write_text(f'{hashlib.sha256(b"archive").hexdigest()}  {name}\n')

    def test_invalid_metadata(self):
        self.notes.write_text(self.notes.read_text().replace('channel: stable', 'channel: unknown'))
        with self.assertRaises(ValueError):
            publisher.parse_notes(self.notes)

    def test_heading_must_match(self):
        self.notes.write_text(self.notes.read_text().replace('CLI 0.2.3', 'CLI 0.2.4'))
        with self.assertRaises(ValueError):
            publisher.parse_notes(self.notes)

    def test_missing_and_corrupt_assets(self):
        root = self.root / 'assets'
        root.mkdir()
        with self.assertRaises(ValueError):
            publisher.verify_assets(root, 'cli-0.2.3')
        self.assets(root)
        publisher.verify_assets(root, 'cli-0.2.3')
        (root / 'card-factory-0.2.3-windows-x64.zip').write_bytes(b'corrupt')
        with self.assertRaises(ValueError):
            publisher.verify_assets(root, 'cli-0.2.3')

    def test_extra_assets_are_rejected(self):
        root = self.root / 'assets'
        root.mkdir()
        self.assets(root)
        (root / 'unexpected.zip').write_bytes(b'extra')
        with self.assertRaises(ValueError):
            publisher.verify_assets(root, 'cli-0.2.3')

    def test_invalid_tag_stops_before_network(self):
        with patch.object(publisher, 'gh') as gh:
            with self.assertRaises(ValueError):
                publisher.publish(self.root / 'cli-0.2.3-beta.md', 'owner/repo')
            gh.assert_not_called()

    @patch.object(publisher, 'gh')
    def test_published_history_is_never_edited(self, gh):
        self.notes.write_text('Historical notes without new metadata')
        gh.return_value = json.dumps({'isDraft': False})
        publisher.publish(self.notes, 'owner/repo')
        self.assertEqual(gh.call_count, 1)

    @patch.object(publisher, 'gh')
    def test_source_mismatch_stops_before_download(self, gh):
        gh.return_value = json.dumps({'isDraft': True, 'body': 'Wrong source'})
        with self.assertRaises(ValueError):
            publisher.publish(self.notes, 'owner/repo')
        self.assertEqual(gh.call_count, 1)

    def run_publication(self, channel, changed=False, check_only=False):
        self.notes.write_text(self.notes.read_text().replace('channel: stable', f'channel: {channel}'))
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
        return calls

    def test_stable_and_staged_flags(self):
        for channel in ('stable', 'staged'):
            calls = self.run_publication(channel)
            self.assertIn('--draft=false', calls[-1])
            self.assertIn(f'--prerelease={str(channel == "staged").lower()}', calls[-1])

    def test_changed_draft_is_not_edited(self):
        self.assertFalse(any(c[1] == 'edit' for c in self.run_publication('stable', changed=True)))

    def test_check_only_never_edits(self):
        self.assertFalse(any(c[1] == 'edit' for c in self.run_publication('stable', check_only=True)))


if __name__ == '__main__':
    unittest.main()
