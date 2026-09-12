# Install Card Factory CLI

## Choose the application archive

Open the [CLI releases](https://github.com/howardman0209/EmvTestCardFactory-CLI/releases?q=cli-)
and select a published stable `cli-<version>` release. Read its release notes,
then download the matching ZIP and its `.zip.sha256` file.

The published `cli-0.2.2` release provides these archives:

| Computer | Archive name |
| --- | --- |
| Apple Silicon Mac | `card-factory-0.2.2-macos-aarch64.zip` |
| Intel Mac | `card-factory-0.2.2-macos-x64.zip` |
| Windows x64 | `card-factory-0.2.2-windows-x64.zip` |

Windows ARM64 is not published. Each archive includes a native Java runtime;
a Mac archive cannot be used as a Windows installation. For later versions,
check the actual asset list and [versioned release notes](../releases/README.md).

Do not download the automatic **Source code** archive as an installer. Do not
launch the application from inside the ZIP viewer; extract the entire archive.

## Install with Homebrew or Scoop

The package definitions currently select CLI `0.2.2`. Install the package manager
and the PC/SC reader driver first.

For Apple Silicon macOS 11 Big Sur or newer:

```shell
brew tap howardman0209/card-factory
brew install --cask card-factory
```

For Windows x64 in PowerShell:

```powershell
scoop bucket add howardman0209 https://github.com/howardman0209/scoop-card-factory
scoop install howardman0209/card-factory
```

Both expose `card-factory` on your command path and include Java,
GlobalPlatformPro and CAPs. No separate Java installation is needed. The
Homebrew cask does not support Intel Macs; use their published ZIP instead.
Windows 11 build 22631 was validated; older Windows versions and the Intel
Mac minimum OS have not been independently verified.

After installation:

```shell
card-factory --version
card-factory doctor --scheme visa
```

Use the [update guide](UPDATES.md#update-the-cli) for package-manager upgrades.
For manual ZIP installation, continue below.

## Verify the download

On macOS, run this from the folder containing both downloaded files, adjusting
the version and architecture to your download:

```shell
shasum -a 256 -c card-factory-0.2.2-macos-aarch64.zip.sha256
```

The result should report `OK`. On Windows, compare the SHA-256 reported by
PowerShell with the first value in the downloaded checksum file:

```powershell
Get-FileHash .\card-factory-0.2.2-windows-x64.zip -Algorithm SHA256
Get-Content .\card-factory-0.2.2-windows-x64.zip.sha256
```

Compare the full hexadecimal hash; letter case does not matter. A checksum
mismatch means the files should not be used. The checksum detects inconsistent
downloads; it is not an operating-system code-signing certificate. Follow the
release notes for the archive's signing/notarization status.

## Start the extracted application

Open a terminal in the extracted top-level directory, containing `bin`,
`runtime`, `lib`, `tools` and `artifacts`.

On macOS:

```shell
./bin/card-factory --version
./bin/card-factory --help
./bin/card-factory readers
./bin/card-factory doctor --scheme visa
```

On Windows, use PowerShell:

```powershell
.\bin\card-factory.bat --version
.\bin\card-factory.bat --help
.\bin\card-factory.bat readers
.\bin\card-factory.bat doctor --scheme visa
```

Use `card-factory`/`card-factory.bat`, rather than the internal
`card-factory-java` launcher. Keep the extracted directories together; moving
only the launcher loses its runtime, tools and artifacts.

`doctor` checks the runtime, GlobalPlatformPro, reader discovery and selected
artifacts without changing a card. No detected reader is reported as a warning;
connect a reader and install its operating-system driver before card operations.
CAPs currently target Java Card Classic 3.0.5. Read the release notes for tested
card environments and capabilities; the target alone does not establish support
for every card's memory or cryptographic implementation.

Continue with the [CLI workflow](CLI.md) or [update instructions](UPDATES.md).
