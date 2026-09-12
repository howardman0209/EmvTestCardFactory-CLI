# Card Factory CLI 0.2.2

Card management release for macOS ARM64 (Apple Silicon), macOS x64 (Intel), and Windows x64.
This is the first release built entirely on GitHub-hosted runners.

## Platform assets

- Available platforms: macOS ARM64 (Apple Silicon), macOS x64 (Intel), and Windows x64.
- Each platform ZIP has a matching SHA-256 file.
- Download the named ZIP and its SHA-256 file. The automatic Source code archives contain public documentation, not the application.

## Changes since 0.2.1

### Added

- `applet uninstall` removes the selected payment instance and package, preserving PPSE by default. The complete plan is checked before any DELETE is sent; `--dry-run` authenticates and reads the registry without deleting. The instance is removed before its package and the registry is reread to verify removal. Missing targets are skipped, so rerunning after a partial removal is supported. No cascading deletion is used: extra applet classes or instances, unknown source-package evidence, and identity conflicts block the operation. `--include-ppse` explicitly extends removal to PPSE; other known payment instances or uncertain identities block that. Retained PPSE directory data is not rewritten and may still advertise the removed application.
- `card memory` reads the card's Extended Card Resources with GlobalPlatform `GET DATA FF21` over direct PC/SC. It reports application count, free non-volatile memory and free volatile memory from tags `81`, `82` and `83`, accepts either the outer `FF21` template or a bare resource TLV sequence, and treats the values as unsigned. `--isd-aid` defaults to `A000000151000000`. The command needs no CAPs, manifests, installed applet or GlobalPlatform key, and does not authenticate. Support is card dependent; unsupported or malformed responses exit 4 with the operation and, when available, the status word, and never print an invented capacity. These are card-reported resources, not total or used capacity, and not a guarantee that a particular CAP fits.
- Separate GlobalPlatform key inputs: `--gp-key-enc`, `--gp-key-mac`, `--gp-key-dek`, and `CARD_FACTORY_GP_KEY_ENC`, `CARD_FACTORY_GP_KEY_MAC`, `CARD_FACTORY_GP_KEY_DEK`. Each key resolves independently through option, environment variable, then hidden prompt, and the values are forwarded to GlobalPlatformPro as `--key-enc`, `--key-mac` and `--key-dek`. Missing-key errors name the specific purpose that was not supplied.

### Changed

- `applet status` now prints a Card Factory inventory instead of the raw GlobalPlatform registry: PPSE above all six payment schemes, with aligned Status and Version columns. Every supported scheme is listed, including `Not installed`. `Package only` means a package without its expected instance, `Unknown` a present package with no reported version, and `Locked` a reported locked lifecycle. Identification uses the bundled canonical AID catalog and needs no local CAP files or manifests; identity conflicts and missing source-package evidence are shown explicitly and exit 4. **Scripts that parsed the previous raw output must be updated**; use GlobalPlatformPro directly for the complete registry.
- Reader selection is now identical across all seven card commands. `--reader` is optional when exactly one reader is available, is required by index or exact name when several are present, and reports a PC/SC error when none are. `applet install` and `applet status` no longer delegate selection to GlobalPlatformPro, so a host with multiple readers that previously relied on that delegation must now pass `--reader`. `--reader` became optional for `applet verify`, `profile provision` and `transaction run`, which previously required it. `--debug` prints the automatically selected reader name.
- The interactive key prompt asks separately for ENC, MAC and DEK and never selects shared-key mode. No shared or default key is assumed. `--gp-key` and `CARD_FACTORY_GP_KEY` remain supported as an explicit shared-key input for cards that intentionally use one value for all three purposes, and cannot be combined with any separate key input, including environment variables. Clear the conflicting variables before switching modes.
- All GlobalPlatform keys, not only the former single key, are redacted in the CLI's own dry-run and error output. GlobalPlatformPro still receives keys as process arguments, including when they came from prompts or environment variables.

### Build and release

- A `CLI build and release` workflow builds `macos-aarch64`, `macos-x64` and `windows-x64` on GitHub-hosted runners from one source revision, runs the host and applet tests and the standalone smoke test on each, verifies that exactly three ZIPs and three checksums exist for one version, and creates the public draft this release was published from. No local Intel Mac or Windows machine was used.
- Host version policy for the `0.x` series is now explicit: a minor bump marks a change to the CAP compatibility boundary, while features, fixes and build changes that preserve CAP compatibility take a patch bump. 0.2.2 is a patch release under that rule.

### Not changed

- No applet, CAP, core crypto, personalization or transaction source changed between the 0.2.1 and 0.2.2 build commits. The only changed areas are the CLI module, documentation, package-manager metadata, release tooling and the root version.
- The bundled CAPs are unchanged and `caps-0.23.0` remains the current signed CAP bundle.

## Features

- Install, personalize and test supported EMV test-card applets.
- Bundled Java 25 runtime, GlobalPlatformPro, common PPSE and six payment-scheme CAPs.
- Signed CAP update discovery, downloads, local cache and explicit artifact selection.
- CLI update checks with manual upgrade guidance.
- Applet compilation and maintainer signing tools are excluded from this distribution.

## Compatibility and upgrade

- Host version: 0.2.2; bundled CAP package version: 0.23.
- Requires install manifest schema 2; personalization protocol 3; applet contract 1.
- CAP target: Java Card Classic 3.0.5. Card memory and crypto support still require validation on the intended hardware.
- Cached CAP releases declaring minHostVersion 0.2.0 and maxHostVersionExclusive 0.3.0 stay compatible. Upgrading from 0.2.0 or 0.2.1 needs no CAP re-download or re-selection.
- Existing schema 1 artifact sets must be replaced or regenerated.
- Extract the complete archive into a separate directory and run bin/card-factory doctor.
- Downloading/selecting CAPs does not update a card; replacement and personalization remain explicit operations.
- Review the two behavior changes above before upgrading automation: `applet status` output and reader selection for `applet install`/`applet status`.
- The bundled runtime on macOS ARM64 is now Java 25.0.4.1 rather than 0.2.1's 25.0.2. All three platforms ship the same runtime version.
- The ZIP has not been project-signed or notarized for macOS. Normal Gatekeeper quarantine was not exercised for this publication; the archives were fetched with an authenticated GitHub client rather than a browser.
- Minimum macOS on ARM64 is 11 Big Sur, taken from the bundled runtime's declared `minos`. Minimum operating-system support on Intel macOS and Windows has not been independently verified for this publication.

## Build provenance and validation

- Source commit: `df8f1d160ffae430c9914f5e301c38525b547ebe`.
- Java Card SDK submodule: `6a75ec0d6913db236d354f154df7dbc9573d976d` (unchanged from 0.2.1).
- Update repository: `howardman0209/EmvTestCardFactory-CLI`.
- CI: all three platform builds and the release-asset validation job passed on the `cli-0.2.2` tag; each runner ran `:core:test :artifacts:test :card-io:test :cli:test :applet:test` and `:cli:buildCliRelease`, which includes the bundled-runtime smoke test.
- Host tests rerun at the build commit on the publishing Mac: 233 passing (60 core, 10 artifacts, 135 CLI, 28 applet; `card-io` has no test sources). 0.2.1 recorded 191.
- Publication checks on macOS ARM64: all three draft ZIPs were downloaded and matched their SHA-256 sidecars. Each archive's extraction root is `card-factory-0.2.2-<platform>`, and each bundles Java 25.0.4.1 with a native runtime for its own target (macOS arm64, macOS x86_64, Windows x86-64).
- Cross-platform consistency: the `core` and `card-io` jars and the complete `artifacts/` CAP and manifest tree are byte-identical across the three archives. The Windows `cli` and `artifacts` jars differ only in the CRLF line endings of three packaged text resources (`aids.properties`, `globalplatform.properties`, `cap-release-public-key.txt`), which are identical after newline normalization; no class file differs.
- macOS ARM64 archive execution: `--version` reports 0.2.2, `schemes` lists all six schemes, and `doctor` resolved the bundled runtime, bundled GlobalPlatformPro 26.06.04, PPSE and payment CAPs, and verified install-manifest checksums. `applet uninstall` and `card memory` are present in the command surface.
- Runtime independence on macOS ARM64: with an invalid `JAVA_HOME` and a failing `java` ahead of it on `PATH`, `--version` and `doctor` still resolved the bundled runtime and GlobalPlatformPro. No network access was needed.
- The POSIX launcher was exercised through a direct symbolic link and a chained link outside the installation, the arrangement a package manager's `bin` link creates; both resolved the installation correctly.
- Bundled install manifests declare schema 2 with minHostVersion 0.2.0, maxHostVersionExclusive 0.3.0, personalization protocol 3 and applet contract 1; bundled PPSE and payment CAP package version is 0.23.
- Native execution on Intel macOS and Windows was not repeated on the publishing Mac; those archives were validated by extraction, digest, binary architecture and content comparison only.
- No physical-card operation was performed for this publication; no reader was detected during the macOS ARM64 checks. The M8.6 physical-card gate is separate and remains pending, and the new `applet uninstall` and `card memory` commands have not been exercised against a physical card.
- Package-manager metadata was promoted after this publication, on 2026-09-11: Homebrew tap commit `56a1121` and Scoop bucket commit `43b0147`. Both pin the digests in the table below, were rendered from anonymous downloads of these published assets, and were read back anonymously after the push. `brew upgrade --cask card-factory` and `scoop update card-factory` both move an existing installation to 0.2.2; the macOS upgrade was reproduced on an Apple Silicon host and the Windows one was confirmed by the maintainer.

## Usage

See the [installation guide](https://github.com/howardman0209/EmvTestCardFactory-CLI/blob/main/docs/INSTALLATION.md) and [CLI/CAP update guide](https://github.com/howardman0209/EmvTestCardFactory-CLI/blob/main/docs/UPDATES.md).

## Platform archive verification

| Platform | Bundled Java | ZIP SHA-256 |
| --- | --- | --- |
| macos-aarch64 | 25.0.4.1 | `deac2a0f6d69f52cdd35f3cfaf54c5d358ce11cc9219637b567f01531e42211a` |
| macos-x64 | 25.0.4.1 | `4592fb5f13dc0a1c17aa9ceffce3ce05dba0cd28de8909aea8f2be43603bedf3` |
| windows-x64 | 25.0.4.1 | `973a5f806829eebef9814a1adafa42678e3dd819f9d5bfa1acec9cc0a2350ce6` |
