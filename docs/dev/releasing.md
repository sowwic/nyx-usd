# Releasing

## Branches and versions

`develop` is the default and PR branch; `main` is the release branch. Work on a feature
branch named after the GitHub issue.

The version lives in `VERSION`. `make update-version` copies it into `pyproject.toml`
(and `make build` does that first). Add a section for it at the top of `CHANGELOG.rst`,
one bullet per user-visible change with the issue number where there is one: new nodes,
new inputs, changed behaviour of an operation.

## Release

```bash
make release VERSION=1.2.3 [RELEASE_TITLE="..."]
```

Runs the release script of `sowwic/gh-workflows`: it tags `main`, pushes, and merges back
into `develop`. The tag triggers `.github/workflows/release.yml`, which creates the GitHub
release from the changelog section.

## What gets released

| Part | Where users get it |
| --- | --- |
| `nyx_usd`, the operations | The package `sowwic-nyx-usd` (PyPI), which they install in the interpreter with USD. |
| `plugins/usd_plugin`, the nodes | **Not in the package.** Users put the `plugins` folder of a checkout or of the release's source archive on `NYX_PLUGIN_PATH`. |

The plugin and the package have to be of the same version: a node calls the function of
that name with those arguments. Say so in the changelog when an operation changes.

## Publishing to PyPI

The distribution is called `sowwic-nyx-usd` and imports as `nyx_usd`. The targets come
from the `general/pypi` module of [sowwic/makefiles](https://github.com/sowwic/makefiles):

```bash
make pypi-publish-dev     # build and upload to TestPyPI
make pypi-publish         # build and upload to PyPI
```

Both run `clean` and `build` first, so only a fresh build is uploaded. `uv publish` reads
the token from `UV_PUBLISH_TOKEN`, so put it in the environment for the run, not in a
file:

```bash
UV_PUBLISH_TOKEN=pypi-... make pypi-publish
```

The first upload needs an account-wide token, a token for one project can only be made once
it exists. A published version can't be replaced: to fix a bad release, bump `VERSION` and
publish again, to hide one, yank it on pypi.org.

## CI

Workflows in `.github/workflows/` are thin callers of the shared ones in
`sowwic/gh-workflows`: tests, lint, docs deployment to GitHub Pages (on `main`) and the
release.
