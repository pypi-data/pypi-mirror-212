# openfractal-client

[![test](https://github.com/OpenDrugDiscovery/openfractal-client/actions/workflows/test.yml/badge.svg)](https://github.com/OpenDrugDiscovery/openfractal-client/actions/workflows/test.yml)
[![release](https://github.com/OpenDrugDiscovery/openfractal-client/actions/workflows/release.yml/badge.svg)](https://github.com/OpenDrugDiscovery/openfractal-client/actions/workflows/release.yml)
[![docker](https://github.com/OpenDrugDiscovery/openfractal-client/actions/workflows/docker.yml/badge.svg)](https://github.com/OpenDrugDiscovery/openfractal-client/actions/workflows/docker.yml)
[![code-check](https://github.com/OpenDrugDiscovery/openfractal-client/actions/workflows/code-check.yml/badge.svg)](https://github.com/OpenDrugDiscovery/openfractal-client/actions/workflows/code-check.yml)
[![doc](https://github.com/OpenDrugDiscovery/openfractal-client/actions/workflows/doc.yml/badge.svg)](https://github.com/OpenDrugDiscovery/openfractal-client/actions/workflows/doc.yml)

A Python client based on [QCPortal](https://github.com/MolSSI/QCFractal) for Open Drug Discovery (ODD) QM large scale data generation.

## Development lifecycle

### Setup dev environment

```bash
micromamba create -n openfractal -f env.yml
micromamba activate openfractal

# Install the git version of QCPortal
pip install --no-deps git+https://github.com/MolSSI/QCFractal.git@c00627258f9344b4b35a7583ee4a9cc5ff2de3e8#subdirectory=qcportal
pip install --no-deps git+https://github.com/MolSSI/QCFractal.git@c00627258f9344b4b35a7583ee4a9cc5ff2de3e8#subdirectory=qcfractalcompute

# Install openfractal-client lib
pip install -e .
```

### Tests

You can run tests locally with:

```bash
pytest
```

## Changelogs

See the latest changelogs at [CHANGELOG.md](./CHANGELOG.md).

## License

Under the Apache-2.0 license. See [LICENSE](LICENSE).
