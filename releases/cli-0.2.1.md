# Card Factory CLI 0.2.1

Stable release for macOS ARM64 (Apple Silicon), macOS x64 (Intel), and Windows x64.

## Platform assets

- Available platforms: macOS ARM64 (Apple Silicon), macOS x64 (Intel), and Windows x64.
- Each platform ZIP has a matching SHA-256 file.
- Download the named ZIP and its SHA-256 file. The automatic Source code archives contain public documentation, not the application.

## Changes since 0.2.0

- Fixed: the POSIX launcher resolves its own path through symbolic links before locating the installation. When a package manager links `bin/card-factory` into its own bin directory, the launcher previously looked for `card-factory-java` and the bundled runtime beside the link and exited 126. Absolute, relative and chained links are handled, the link walk is bounded, and an unresolved target is reported by name.
- Added: Homebrew cask and Scoop manifest metadata for installing the CLI through a package manager. That metadata is promoted to its public repositories after this release is published; `brew` and `scoop` installation works from that point.
- No applet, CAP, crypto, personalization or transaction behavior changed. The bundled CAPs are unchanged from 0.2.0, and `caps-0.23.0` remains the current signed CAP bundle.

## Features

- Install, personalize and test supported EMV test-card applets.
- Bundled Java 25 runtime, GlobalPlatformPro, common PPSE and six payment-scheme CAPs.
- Signed CAP update discovery, downloads, local cache and explicit artifact selection.
- CLI update checks with manual upgrade guidance.
- Applet compilation and maintainer signing tools are excluded from this distribution.

## Compatibility and upgrade

- Host version: 0.2.1; bundled CAP package version: 0.23.
- Requires install manifest schema 2; personalization protocol 3; applet contract 1.
- CAP target: Java Card Classic 3.0.5. Card memory and crypto support still require validation on the intended hardware.
- Cached CAP releases declaring minHostVersion 0.2.0 and maxHostVersionExclusive 0.3.0 stay compatible. Upgrading from 0.2.0 needs no CAP re-download or re-selection.
- Existing schema 1 artifact sets must be replaced or regenerated.
- Extract the complete archive into a separate directory and run bin/card-factory doctor.
- Downloading/selecting CAPs does not update a card; replacement and personalization remain explicit operations.
- The ZIP has not been project-signed or notarized for macOS. Normal Gatekeeper quarantine was exercised on macOS ARM64 without bypassing it.
- Minimum macOS on ARM64 is 11 Big Sur, taken from the bundled runtime's declared minimum. Minimum operating-system support on Intel macOS and Windows has not been independently verified for this publication.

## Build provenance and validation

- Build source commit recorded in the draft: `f42ab657226ed31f5420240b272a0bc784887d87`. This provenance is retained from the existing draft; it was not independently reconstructed from the archives during publication.
- Java Card SDK submodule: `6a75ec0d6913db236d354f154df7dbc9573d976d`.
- Update repository: `howardman0209/EmvTestCardFactory-CLI`.
- Previously recorded host tests (not rerun during publication): 191 passing (60 core, 10 artifacts, 93 CLI, 28 applet).
- All scheme CAP conversion/manifest build tasks passed or were verified up to date.
- The earlier draft recorded a macOS ARM64 smoke check with Java 25.0.1. The uploaded ARM64 archive contains Java 25.0.2; that earlier check does not establish native execution of this final archive.
- Previously recorded runtime independence on macOS ARM64: with an invalid `JAVA_HOME` and a failing `java` ahead of it on `PATH`, `doctor` resolved the bundled runtime, GlobalPlatformPro and verified manifest checksums for all six schemes. `--help`, `--version`, `schemes` and `doctor` work with no network access.
- Previously recorded macOS ARM64 package lifecycle was exercised through a Homebrew cask: fresh install, a real 0.2.0 to 0.2.1 upgrade, uninstall, reinstall, artifact cache and selection preserved unchanged, a digest mismatch rejected without breaking a working installation, and an Intel host refused rather than given another architecture's runtime.
- No physical-card operation was performed for this publication; no reader was detected during the macOS ARM64 checks. The M8.6 physical-card gate is separate and remains pending.
- Publication checks: all three uploaded ZIPs were downloaded and matched their SHA-256 sidecars. ZIP integrity, CLI and packaged host version 0.2.1, the pinned public update repository, runtime CPU architecture, and all six scheme CAP manifest checksums were verified. Native execution on Intel macOS and Windows was not repeated on the publishing Mac.
- Native platform execution and physical-card validation were not rerun during this release-note update. The checks above are archive and metadata validation.

## Usage

See the [installation guide](https://github.com/howardman0209/EmvTestCardFactory-CLI/blob/main/docs/INSTALLATION.md) and [CLI/CAP update guide](https://github.com/howardman0209/EmvTestCardFactory-CLI/blob/main/docs/UPDATES.md).

## Platform archive verification

| Platform | Bundled Java | ZIP SHA-256 |
| --- | --- | --- |
| macos-aarch64 | 25.0.2 | `5523524aa06d12755e04470222c39d6ac3c41f7f20d6b7c80e83e9060d5da08e` |
| macos-x64 | 25.0.4.1 | `9313b5b5956826223e56a930d4af50f6644cd597d6095b0b64ca8ca45e35abea` |
| windows-x64 | 25.0.4.1 | `b675ef5f0bc45f8e312e34d07d133e0fe55abf20f96e13df72f86f4a3a5ef46b` |

