# CLI and CAP updates

CLI releases and CAP releases share this repository but use independent
versions. `cli-<version>` identifies a host application release;
`caps-<version>` identifies a platform-independent applet bundle. Use those
prefixes rather than GitHub's single "Latest" badge to distinguish them.

Examples use the macOS launcher from the extracted installation directory.
On Windows, use `.\bin\card-factory.bat` instead of `./bin/card-factory`.

## Update the CLI

```shell
./bin/card-factory update check
```

If a newer stable host exists, the command displays its release page and a
download link matching the current platform, when that asset is available.
It does not replace the running installation.

Download the new archive and checksum, [verify and extract it](INSTALLATION.md)
into a separate directory, then run the new launcher's `--version` and
`doctor`. Keep the previous installation until the new one has been verified.
Downloaded CAPs and artifact selection are stored outside the installation.

If the running version already matches the newest release, "No newer stable
host release is available" is expected. Drafts and prereleases are not offered
as stable updates.

## Update CAP artifacts

List signed CAP releases and their host compatibility:

```shell
./bin/card-factory artifacts check
```

Download the newest compatible stable bundle:

```shell
./bin/card-factory artifacts download
```

Alternatively, request a specific published version:

```shell
./bin/card-factory artifacts download --version 0.23.0
```

`0.23.0` is an example: use a version actually shown by `artifacts check`.
The tool verifies the publisher signature, archive checksum and manifests.
An incompatible bundle is rejected; follow its required host version range
instead of editing metadata to bypass it.

Download does not activate a bundle. Inspect cached versions and select one:

```shell
./bin/card-factory artifacts list
./bin/card-factory artifacts use 0.23.0
./bin/card-factory doctor --scheme visa
```

Selection affects subsequent artifact-dependent operations, but it does not
replace anything on a card. Use the [card workflow](CLI.md) to preview an
installation and explicitly authorize replacement when needed. Replacement
can require personalization again.

To return to the distribution's bundled artifacts:

```shell
./bin/card-factory artifacts use bundled
```

Old downloaded versions remain cached. Selecting an older bundle does not
roll back a card or recover its earlier personalization data. Download failure,
a bad signature or incompatible content does not switch the current selection.
A corrupted selected cache produces an error rather than silently choosing
another version.

## Bundle contents and compatibility

Each CAP release has three assets:

- `card-factory-caps-<version>.zip`
- `cap-release.json`
- `cap-release.sig`

The bundle contains one common PPSE CAP, six scheme payment CAPs and six
install manifests. It is shared by macOS and Windows. The application verifies
it with its trusted public key; users do not need the private signing key.
Manual downloads are available on the
[CAP release pages](https://github.com/howardman0209/EmvTestCardFactory-CLI/releases?q=caps-),
but use `artifacts download` for the application's verified cache workflow.

Host 0.2.0 uses schema 2 manifests with a minimum host version, an exclusive
maximum host version, personalization protocol, applet contract and Java Card
target. A new CAP may require upgrading the CLI first. Older hosts without
update support need a manual host upgrade. The card's package version, CAP
bundle version and CLI version are separate identifiers.

## Local storage

| Platform | Default user-data directory |
| --- | --- |
| macOS | `~/Library/Application Support/CardFactory` |
| Windows | `%LOCALAPPDATA%/CardFactory` |
| Linux | `$XDG_DATA_HOME/card-factory`, or `~/.local/share/card-factory` |

`CARD_FACTORY_DATA_HOME` can override the directory. Versioned bundles are
stored under `artifacts/<version>/`; `selected-artifacts.txt` records selection.
The next host version rechecks the selected bundle's compatibility and local
contents before use. No automatic cache deletion is implemented.

## Troubleshooting

| Symptom | Next step |
| --- | --- |
| Repository page has documentation but no installer files | Open Releases and its Assets section; binaries are not source files. |
| Release list is empty | No stable release of that type has been published yet. |
| No newer CLI version is offered | Check the installed version and `cli-` releases; the current version is not an update to itself. |
| No matching platform archive | Use only an explicitly published compatible platform asset. |
| CAP requires a different host version | Run `update check` and review the required range before installing. |
| Signature/checksum validation fails | Do not edit the files to force acceptance. Retain a known-good set or use `artifacts use bundled`. |
| HTTP 404 or network error | Check public release access and connectivity. A build configured for a private release destination needs a correctly configured distribution. |
| On-card version differs from selected CAP | Select the matching artifacts or preview an explicit card update; downloading alone does not update the card. |

For the complete command and input reference, consult `--help` and the CLI
README included in the application archive.
