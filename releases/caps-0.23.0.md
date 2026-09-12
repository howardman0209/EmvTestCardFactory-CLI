# Card Factory CAPs 0.23.0

## Contents

One platform-independent CAP bundle for macOS, Windows and other supported Card Factory hosts:

- Common PPSE CAP.
- Visa, Mastercard, American Express, UnionPay, JCB and Discover/Diners payment CAPs.
- Six schema 2 install manifests.

All three assets belong together: the ZIP, cap-release.json and cap-release.sig.
The GitHub automatic Source code archives contain public documentation, not applet sources or CAP bundles.

## Compatibility

- Requires Card Factory host >= 0.2.0 and < 0.3.0.
- Personalization protocol: 3; applet contract: 1.
- Java Card target: Classic 3.0.5; card memory and cryptographic capabilities must be appropriate for the selected scheme.
- Java Card package version: 0.23. This is distinct from CAP bundle release version 0.23.0 and host version 0.2.0.

## Installation and updates

Use artifacts check and artifacts download --version 0.23.0 from a compatible host, then explicitly select it with artifacts use 0.23.0.

Downloading or selecting this bundle does not change a card. Preview installation with applet install --dry-run. Replacing incompatible on-card packages requires explicit replacement options and may require personalization again.

## Provenance and validation

- Source commit recorded in signed metadata: `5b0164bbf45f589a744ea683a7faf82de579aacb`.
- Archive SHA-256: `4b099f0fc3962ec1be36b2dd54eed4daa1d4e03d8741128bb8476755cd78adb5`.
- Archive size: 165946 bytes.
- Existing signed artifacts were retained without rebuilding or overwriting the release identity.
- Signature, archive checksum and all six manifests were reverified using the CLI distribution's bundled runtime and runtime importer before upload.
- The current source checkout has no changes to applet build/source or core runtime source relative to the signed source commit.
- No physical-card operations were performed for this upload.

See the [CAP update guide](https://github.com/howardman0209/EmvTestCardFactory-CLI/blob/main/docs/UPDATES.md#update-cap-artifacts).
