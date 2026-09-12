"""Publish an existing verified CLI draft from versioned release notes."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


TAG = re.compile(r"cli-(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")


def gh(*args):
    return subprocess.check_output(["gh", *args], text=True)


def parse_notes(path):
    tag = path.stem
    if not TAG.fullmatch(tag):
        raise ValueError(f"Invalid CLI release filename: {path}")
    text = path.read_text()
    match = re.match(
        r"\A<!-- release\nsource: ([0-9a-f]{40})\nchannel: (stable|staged)\n-->\n\n(.+)\Z",
        text, re.DOTALL,
    )
    if not match:
        raise ValueError("Notes require a source SHA, explicit stable/staged channel and body")
    source, channel, body = match.groups()
    if not body.startswith(f"# Card Factory CLI {tag[4:]}\n"):
        raise ValueError("Release heading must match the filename version")
    return source, channel, body


def verify_assets(directory, tag):
    names = [f"card-factory-{tag[4:]}-{p}.zip" for p in
             ("macos-aarch64", "macos-x64", "windows-x64")]
    expected = set(names + [n + ".sha256" for n in names])
    if {p.name for p in directory.iterdir()} != expected:
        raise ValueError("Expected exactly three platform ZIPs and three checksums")
    for name in names:
        with (directory / name).open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        if (directory / (name + '.sha256')).read_text().strip() != f"{digest}  {name}":
            raise ValueError(f"Checksum mismatch: {name}")


def publish(path, repo, check_only=False):
    tag = path.stem
    if not TAG.fullmatch(tag):
        raise ValueError(f"Invalid CLI release filename: {path}")
    release = json.loads(gh('release', 'view', tag, '--repo', repo,
                            '--json', 'isDraft,body,assets'))
    # Historical notes and reruns never edit a published release.
    if not release['isDraft']:
        print(f"{tag}: already published; unchanged")
        return
    source, channel, body = parse_notes(path)
    if re.search(r"^Source commit: `" + source + r"`\s*$", release['body'], re.MULTILINE) is None:
        raise ValueError("Draft source commit does not match the approved notes")
    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary) / 'assets'
        directory.mkdir()
        gh('release', 'download', tag, '--repo', repo, '--dir', str(directory))
        verify_assets(directory, tag)
        if check_only:
            print(f"{tag}: draft and assets verified; publication disabled")
            return
        # Refuse to edit if another actor published while assets were being checked.
        current = json.loads(gh('release', 'view', tag, '--repo', repo,
                                '--json', 'isDraft,body,assets'))
        if current != release:
            raise ValueError("Draft changed during verification; rerun after review")
        notes = Path(temporary) / 'notes.md'
        notes.write_text(body.rstrip() + f"\n\nSource commit: `{source}`\n")
        gh('release', 'edit', tag, '--repo', repo, '--notes-file', str(notes),
           '--draft=false', f"--prerelease={'true' if channel == 'staged' else 'false'}",
           '--latest=false')
        print(f"{tag}: published as {channel}")


def main():
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    before = event['before']
    head = os.environ['GITHUB_SHA']
    if not re.fullmatch(r'[0-9a-f]{40}', before) or before == '0' * 40:
        raise ValueError('A valid previous main commit is required')
    changed = subprocess.check_output(
        ['git', 'diff', '--name-only', '--diff-filter=AM', '-z', before, head,
         '--', 'releases/cli-*.md'], text=True,
    ).split('\0')
    for name in filter(None, changed):
        publish(Path(name), os.environ['GITHUB_REPOSITORY'])


if __name__ == '__main__':
    main()
