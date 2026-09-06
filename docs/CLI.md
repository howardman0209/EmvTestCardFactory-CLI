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

Use the current reader index printed by `readers`, or its exact reader name.
An index can change when readers are connected or removed. The examples use
reader `0`; substitute the intended reader before executing them.

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

This inspects the GlobalPlatform registry but does not modify the card. In an
interactive terminal, the command prompts for the GlobalPlatform key without
echoing it. For non-interactive use, provide `CARD_FACTORY_GP_KEY` through your
normal secret-handling workflow. Do not include keys in issue reports or logs.

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

To inspect the GlobalPlatform registry:

```shell
./bin/card-factory applet status --reader 0
```

## Artifact selection

The distribution includes CAPs for offline use. Use the
[update guide](UPDATES.md#update-cap-artifacts) to download and select newer
compatible bundles. Downloads and selection do not change a card.

The release CLI does not include `applet build`. Users do not need applet
sources or a Java Card SDK to install the distributed artifacts.
