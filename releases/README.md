# Release notes

Each CLI, UI or CAP version has a separate Markdown file. Historical files preserve
the published GitHub release body verbatim; their commits do not rebuild or
republish binaries.

| Version | Notes |
| --- | --- |
| CLI 0.2.2 | [cli-0.2.2.md](cli-0.2.2.md) |
| CLI 0.2.1 | [cli-0.2.1.md](cli-0.2.1.md) |
| CLI 0.2.0 | [cli-0.2.0.md](cli-0.2.0.md) |
| CAPs 0.23.0 | [caps-0.23.0.md](caps-0.23.0.md) |

## Publish a new CLI version

1. Build the version in the private source repository using its `cli-*` tag or
   manual release workflow. Wait for the three-platform draft to be complete.
2. Create `releases/cli-<version>.md` using the format below. Replace the example
   SHA with the full source commit recorded in that draft. Keep the generated
   draft source line intact until publication. Choose `stable` or `staged`
   explicitly; staged releases are published as prereleases and ignored by
   application update discovery.
3. Review the changes, platform validation and upgrade guidance in a PR.
   Merge one new version's notes into `main` when ready to publish. A direct
   push also publishes, so keep unfinished notes on a feature branch.
4. Wait for **Publish CLI release notes** to finish before merging the next
   version. It checks the draft source and all three ZIP/checksum pairs before
   publishing. It never builds binaries, uploads assets or accesses private
   source. The metadata comment is omitted from the GitHub release body.
5. Verify public downloads, then follow the separate package-manager promotion
   process. CAP signing and publication remain manual.

Example file format (the version is illustrative, not an available release):

```markdown
<!-- release
source: 0123456789abcdef0123456789abcdef01234567
channel: stable
-->

# Card Factory CLI 0.2.3

## Changes

- Describe verified user-visible changes.

## Compatibility and validation

- Record compatibility, platform checks and any remaining validation gaps.

## Upgrade

- Describe any required upgrade steps.
```

The public workflow needs only its repository's `GITHUB_TOKEN` with Contents
write; no additional secret is required. Tests run separately on PRs and
release-tooling changes. Keep the public repository limited to documentation,
publication tooling and downloadable release assets.

## Reruns and corrections

A missing draft, invalid metadata, source mismatch, incomplete asset set or
checksum mismatch stops publication. Fix the cause and rerun the failed run;
if the notes were wrong, push the corrected version file. A draft changed by
another actor during verification is rejected. Do not edit or upload to a
draft while publication is running.

An already-published version is always skipped, including historical backfills
and reruns after success. Editing its file records a documentation correction
only; it does not modify the GitHub release body or promote a prerelease.
Promote staged releases explicitly after validation using the existing manual
process. A changed binary requires a new version; published assets are never
replaced by this workflow.

## Publish a UI version

UI notes use independent `releases/ui-<version>.md` files and the heading
`# Card Factory UI <version>`. The source SHA and explicit `stable`/`staged`
metadata use the same format as CLI notes. Start with `channel: staged`; record
native installer, signing and physical-card evidence before stable publication.

The private UI workflow supplies exactly these four assets for one version:

- `card-factory-ui-<version>-macos-aarch64.dmg`
- `card-factory-ui-<version>-macos-aarch64.dmg.sha256`
- `card-factory-ui-<version>-windows-x64.msi`
- `card-factory-ui-<version>-windows-x64.msi.sha256`

**Publish UI release notes** runs only when UI note files change on `main`. It
checks the draft source commit, exact installer set and digests, then rechecks
that the draft has not changed before publication. CLI ZIPs and Intel Mac assets
are rejected for UI releases. Published versions remain unchanged on reruns.
The public workflow uses its own `GITHUB_TOKEN`; no new secret is required.

No UI version is available merely because this publication tooling exists.
Do not commit unfinished `ui-*.md` notes to `main`: that is a publication trigger.
