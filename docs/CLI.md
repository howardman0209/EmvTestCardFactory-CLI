# Use the CLI

The shell examples below run from the extracted application directory on
macOS. On Windows, replace `./bin/card-factory` with
`.\bin\card-factory.bat` in PowerShell.

## Inspect available commands and devices

```shell
./bin/card-factory --help
./bin/card-factory schemes
./bin/card-factory readers
./bin/card-factory doctor --scheme visa
./bin/card-factory applet --help
./bin/card-factory card --help
./bin/card-factory profile --help
./bin/card-factory transaction --help
```

| Payment scheme | `--scheme` value |
| --- | --- |
| Visa | `visa` |
| Mastercard | `mastercard` |
| American Express | `amex` |
| UnionPay | `unionpay` |
| JCB | `jcb` |
| Discover/Diners | `discover-diners` |

`--reader` is optional when exactly one PC/SC reader is available. With several
readers, pass the current index printed by `readers` or the exact reader name;
with none, card commands report a PC/SC error. This applies to install, uninstall,
status, verify, provision, transaction and memory commands. Indexes can change
when devices reconnect. The examples use reader `0`; select the intended slot.

## Command reference

| Command | Purpose |
| --- | --- |
| `schemes` | List supported schemes and canonical identifiers. |
| `readers` | List PC/SC reader indexes and names. |
| `doctor` | Check runtime, update source, readers and artifacts without opening a card. |
| `applet install` | Install from a validated scheme manifest; preview with `--dry-run`. |
| `applet uninstall` | Remove the selected payment instance and package; retain PPSE by default. |
| `applet status` | Show PPSE and all six schemes with installation states and package versions. |
| `applet verify` | Check applet dispatch, versions and personalization status through PC/SC. |
| `card memory` | Read card-reported application count and free NVM/RAM without authentication. |
| `profile render` | Render the baseline profile with optional TLV overrides. |
| `profile provision` | Personalize installed applets; preview without card access using `--dry-run`. |
| `transaction run` | Run and verify a deterministic transaction; advances the card's ATC. |
| `update check` | Show a newer stable host release and download links. |
| `artifacts check` | List signed stable CAP releases and compatibility. |
| `artifacts download` | Download and verify; optional `--version`, without selecting or installing. |
| `artifacts list` | Show cached versions and the current selection. |
| `artifacts use <version-or-bundled>` | Select a cached version or bundled artifacts without changing a card. |

## Provide GlobalPlatform keys

Install, uninstall, status and provision require the card's GlobalPlatform keys.
An interactive terminal prompts separately for ENC, MAC and DEK without echoing
values. For automation, configure `CARD_FACTORY_GP_KEY_ENC`,
`CARD_FACTORY_GP_KEY_MAC` and `CARD_FACTORY_GP_KEY_DEK` through your secret-handling
workflow. The matching options are `--gp-key-enc`, `--gp-key-mac` and
`--gp-key-dek`; each option overrides its environment variable. Missing values
prompt individually, or fail when no interactive terminal is available.

For a card intentionally using one value for all three purposes, explicitly
supply `--gp-key` or `CARD_FACTORY_GP_KEY`. Shared-key input cannot be mixed with
separate key options or environment variables. No shared or default key is
assumed by the interactive prompt.

Keep key values out of shell history, issue reports and logs. The CLI redacts
keys in its own dry-run and error output, but GlobalPlatformPro receives them
as process arguments even when supplied through prompts or environment variables.

## Prepare a card profile

Render the built-in profile without changing a card:

```shell
./bin/card-factory profile render --scheme visa
```

Profile commands can accept supported flat TLV overrides through `--data` or
`--data-file`; these options are mutually exclusive. Use the command's `--help`
and the README included in the archive for the complete input reference.

## Preview installation and personalization

Preview the installation plan:

```shell
./bin/card-factory applet install --scheme visa --reader 0 --dry-run
```

This authenticates and inspects the GlobalPlatform registry without modifying
the card. Supply the keys as described above.

Remove `--dry-run` when you intend to execute the installation plan. The tool
does not replace incompatible packages automatically. `--replace-payment` and
`--replace-ppse` explicitly authorize replacing the respective packages, which
can remove their instances and personalization data. Preview the plan with the
necessary replacement flags before executing it.

Once the expected applets are installed, preview personalization:

```shell
./bin/card-factory profile provision --scheme visa --reader 0 --dry-run
```

This preview does not connect to or change the card. Remove `--dry-run` to
personalize it. Keep the selected CAP artifact set consistent with the applets
installed on the card; version or protocol mismatches must be resolved first.

## Verify and test

After installation and personalization:

```shell
./bin/card-factory applet verify --scheme visa --reader 0
./bin/card-factory transaction run --scheme visa --reader 0
```

`applet verify` checks applet dispatch, versions and personalization status.
A transaction is an active card operation and advances its application
transaction counter; it is not a read-only diagnostic.

To inspect Card Factory installation status:

```shell
./bin/card-factory applet status --reader 0
```

`applet status` authenticates but is read-only. It uses the bundled AID catalog,
so local CAP files and manifests are not required. It shows PPSE and every
supported payment scheme, including `Not installed`, `Package only`, `Unknown`
version and `Locked` states. Identity conflicts or missing source-package
evidence are shown explicitly and return exit code 4. Registry presence does
not establish personalization or transaction readiness.

The output is no longer the raw GlobalPlatform registry. Update scripts that
parsed the old output; use GlobalPlatformPro directly for unrelated applications
or the complete registry.

## Read card memory

```shell
./bin/card-factory card memory --reader 0
./bin/card-factory card memory --reader 0 --isd-aid A000000151000000
```

The command selects the Issuer Security Domain (default AID `A000000151000000`)
and sends GlobalPlatform `GET DATA FF21` over PC/SC. `--isd-aid` accepts a 5–16
byte hexadecimal AID. No keys, installed applets, CAPs or manifests are needed;
this command does not authenticate and has no `--gp` or `--gp-jar` options.

The output reports application count, free non-volatile memory and free volatile
memory in bytes and KiB. These are card-reported free resources, not total or
used capacity, and do not guarantee that a CAP fits. Unsupported, malformed or
authentication-required responses return exit code 4; no secure-channel retry
is attempted. Reader or transport failures return exit code 3.

## Remove a payment applet

Preview the exact targets before executing:

```shell
./bin/card-factory applet uninstall --scheme visa --reader 0 --dry-run
```

The preview authenticates and reads the registry, but sends no DELETE commands.
`--scheme` is required. `--manifest` can select an explicit manifest; the referenced
CAP files must still exist and pass validation. The GP tool and key options are
the same as for installation.

Remove `--dry-run` to delete the payment instance followed by its package.
The command verifies removal and skips missing targets on a rerun. Additional
applet classes or instances, identity conflicts and missing source-package
evidence block removal. A card can still reject deletion because of dependencies
not reported in its registry; completed actions are reported and processing stops.

PPSE remains unless you add `--include-ppse`. Other known payment instances or
uncertain identities block PPSE removal. Retained PPSE directory data is not
rewritten and may still advertise the removed application. There is no extra
confirmation prompt; removal can delete personalization data. Uninstalling a
card applet is separate from uninstalling the CLI from your computer.

## Artifact selection

The distribution includes CAPs for offline use. Use the
[update guide](UPDATES.md#update-cap-artifacts) to download and select newer
compatible bundles. Downloads and selection do not change a card.

The release CLI does not include `applet build`. Users do not need applet
sources or a Java Card SDK to install the distributed artifacts.
