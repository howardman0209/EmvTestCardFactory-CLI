# Card Factory CLI

Card Factory installs, personalizes and tests EMV test-card applets on
compatible Java Cards. It supports Visa, Mastercard, American Express,
UnionPay, JCB and Discover/Diners.

This repository contains public documentation and downloadable releases.
Application source code is maintained separately. The distributed CLI uses
precompiled CAP files; it does not compile applet source code.

## Downloads

| What you need | Where to start |
| --- | --- |
| CLI application for your computer | [CLI releases](https://github.com/howardman0209/EmvTestCardFactory-CLI/releases?q=cli-) and the [installation guide](docs/INSTALLATION.md) |
| Updated Java Card applets | [CAP releases](https://github.com/howardman0209/EmvTestCardFactory-CLI/releases?q=caps-) and the [CAP update guide](docs/UPDATES.md#update-cap-artifacts) |

CLI releases use tags such as `cli-0.2.0`. A single CLI release can contain
separate macOS and Windows archives. CAP releases use independent tags such
as `caps-0.23.0` and contain one platform-independent bundle.

Download only assets that are actually listed in a published release. If a
release list is empty, that type of download has not been published yet.
Version numbers in this documentation are examples, not availability claims.

GitHub's automatic **Source code (zip/tar.gz)** links contain this repository's
documentation, not the application. Choose a named `card-factory-...zip` asset
under the release's **Assets** section. Binaries are distributed through
Releases, not committed to this repository's file history.

## Get started

1. [Download and extract](docs/INSTALLATION.md) the archive matching your OS
   and architecture.
2. Run `card-factory --version`, `card-factory readers` and `card-factory doctor`
   using the launcher inside the extracted archive.
3. Follow the [CLI guide](docs/CLI.md) to inspect artifacts and preview card
   operations.

Distributions include their Java runtime, GlobalPlatformPro and verified
PPSE/payment CAPs. Normal use does not require installing Java, Gradle or the
Java Card SDK. Card operations require a supported reader/driver, a compatible
Java Card and, for management operations, its GlobalPlatform key.

Card Factory is for controlled development and test-card environments. Its
built-in test keys and profiles are not intended for production issuance.

## Documentation

- [Installation and platform selection](docs/INSTALLATION.md)
- [CLI commands and card workflow](docs/CLI.md)
- [CLI and CAP updates, compatibility and troubleshooting](docs/UPDATES.md)

The archive also includes a CLI README and third-party notices. Downloading
or selecting a CAP bundle does not install it on a card. Card replacement
remains an explicit operation.
