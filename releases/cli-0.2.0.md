# Card Factory CLI 0.2.0

## Platform assets

- Available platforms: macOS ARM64 (Apple Silicon), macOS x64 (Intel), and Windows x64.
- Each platform ZIP has a matching SHA-256 file.
- Download the named ZIP and its SHA-256 file. The automatic Source code archives contain public documentation, not the application.

## Features

- Install, personalize and test supported EMV test-card applets.
- Bundled Java 25 runtime, GlobalPlatformPro, common PPSE and six payment-scheme CAPs.
- Signed CAP update discovery, downloads, local cache and explicit artifact selection.
- CLI update checks with manual upgrade guidance.
- Applet compilation and maintainer signing tools are excluded from this distribution.

## Compatibility and upgrade

- Host version: 0.2.0; bundled CAP package version: 0.23.
- Requires install manifest schema 2; personalization protocol 3; applet contract 1.
- CAP target: Java Card Classic 3.0.5. Card memory and crypto support still require validation on the intended hardware.
- Existing schema 1 artifact sets must be replaced or regenerated.
- Extract the complete archive into a separate directory and run bin/card-factory doctor.
- Downloading/selecting CAPs does not update a card; replacement and personalization remain explicit operations.
- The ZIP has not been project-signed or notarized for macOS.

## Build provenance and validation

- Source commit: `03e3e783323db03922d1a4f37a7f67f79acd1e87`. The additional Intel Mac and Windows archives contain matching application class files and CAP artifacts; Windows text resources differ only in line endings.
- Update repository: `howardman0209/EmvTestCardFactory-CLI`.
- Host tests: 159 passing (60 core, 10 artifacts, 89 CLI).
- All scheme CAP conversion/manifest build tasks passed or were verified up to date.
- Extracted macOS distribution smoke check passed with bundled Java 25.0.2, GPPro and CAP checksums.
- No physical-card operation was performed for this publication; no reader was detected during the macOS ARM64 smoke check.
- Imported Intel Mac and Windows archives were checked for ZIP integrity, SHA-256, host/update settings, native runtime architecture and application/CAP consistency. Their native execution was not repeated on the publishing Mac.
- macOS ARM64 archive SHA-256: `65d15039b284dd779cdf44660f8c348d9c8497669000bd807273f7d183c05c79`.

## Usage

See the [installation guide](https://github.com/howardman0209/EmvTestCardFactory-CLI/blob/main/docs/INSTALLATION.md) and [CLI/CAP update guide](https://github.com/howardman0209/EmvTestCardFactory-CLI/blob/main/docs/UPDATES.md).


## Platform archive verification

| Platform | Bundled Java | ZIP SHA-256 |
| --- | --- | --- |
| macos-aarch64 | 25.0.2 | `65d15039b284dd779cdf44660f8c348d9c8497669000bd807273f7d183c05c79` |
| macos-x64 | 25.0.4.1 | `344334a13dd02bc38c48045bc0e9d6805e96e1bd39260258a596868a1f715729` |
| windows-x64 | 25.0.4.1 | `bae33d2c135f1e4d47e22b4be3add495bab8b219de74b7a3088883dfda25e1c9` |
