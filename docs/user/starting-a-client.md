# Starting a client

The USD nodes need a **client**: a running interpreter with USD that is connected to Nyx.
Pick one of the ways below. In every case the nodes go inside a **Remote Client** node,
which waits for the client and hands it to the nodes inside of it.

## The USD Client node

The simplest way. **USD Client** (`usd:client`) starts the interpreter for you, waits
until it has connected, runs the nodes inside of it, and stops the process when they are
done. It is a Launch Process node that builds the command itself.

```text
USD Client      python = /path/to/usd/python
└── Remote Client
    └── Create Stage ─▶ ... ─▶ Save Stage
```

| Input | Meaning |
| --- | --- |
| `python` | The interpreter that has USD. If empty, the `NYX_USD_PYTHON` environment variable is used. |
| `env` | A dictionary of environment variables added to the ones of Nyx. Use it for `PYTHONPATH` and the like. |
| `working_directory` | Folder to run in. Empty uses the current one. |
| `client_name` | Name the client connects as. Empty makes one up. |
| `wait_for_client` | Wait until the client has connected before the nodes inside run. On by default. |
| `timeout` | Seconds to wait for it to connect. 0 or less waits forever. |

| Output | Meaning |
| --- | --- |
| `client` | The name the client connected as. |
| `process_id` | The id of the process. |

The interpreter needs `pxr`, `nyx-bridge` and `nyx_usd`, see
[Installation](installation.md). If they are found through environment variables, add them
to `env`, for example:

```json
{
  "PYTHONPATH": "/path/to/nyx-usd/src:/path/to/openusd/lib/python"
}
```

!!! note
    `env` is added to the environment of Nyx, and a variable of the same name is
    **replaced**, not extended. Write the whole `PYTHONPATH` you need.

Set `NYX_USD_PYTHON` in the shell you start Nyx from to leave `python` empty in every
graph:

```sh
export NYX_USD_PYTHON=/path/to/usd/python
```

Leave `client_name` and `client_kind` empty on the Remote Client inside of it: inside a
USD Client node it uses the process that node started.

## A Launch Process node

The same thing with the generic node, when you want to control the command. Put this in
its `command` input, with `USD_PYTHON` set in the environment or in `env`:

```text
$USD_PYTHON -c "from nyx_bridge.client import NyxClient; NyxClient(name='$NYX_BRIDGE_CLIENT_NAME', reconnect=False).serve_forever()"
```

Launch Process gives the process the address and token of Nyx and the name it has to
connect as (`NYX_BRIDGE_ADDRESS`, `NYX_BRIDGE_TOKEN`, `NYX_BRIDGE_CLIENT_NAME`). The
client has to use that name, or Nyx keeps waiting for it. `$NAME` in the command is
replaced with the variable of that name.

## By hand

Start a client yourself when the interpreter is already running, or lives on another
machine. In that interpreter:

```python
from nyx_bridge.client import NyxClient

NyxClient(name="usd").serve_forever()
```

It keeps trying to reach Nyx and connects again if the connection drops. It finds Nyx
through the environment or the address file Nyx writes, see
[Finding the server](https://sowwic.github.io/nyx-bridge/user/addresses/). In Nyx, give
the Remote Client the name: `client_name = usd`.

## Maya and Blender

The applications have their own clients,
[nyx-bridge-maya](https://github.com/sowwic/nyx-bridge-maya) and
[nyx-bridge-blender](https://github.com/sowwic/nyx-bridge-blender). Connect the
application, make `nyx_usd` importable in its Python (see
[Installation](installation.md#maya-blender-and-houdini)), and select it with
`client_kind` on the Remote Client:

| Application | `client_kind` |
| --- | --- |
| Maya | `maya` |
| Blender | `blender` |

The graph does not change: only the Remote Client node does. Inside the application the
operations run on its main thread, like the other code Nyx sends.

## Which client does a Remote Client use?

| Remote Client is... | It uses |
| --- | --- |
| Inside a USD Client or Launch Process node, `client_name` and `client_kind` empty | The process that node started. |
| Anywhere, with `client_name` set | The client of that name. |
| Anywhere, with `client_kind` set | The one connected client of that kind. If several match it fails instead of choosing, so code never goes to the wrong application: give a name. |

## How long things live

The stages a client has opened stay open until a **Close Stage** node closes them, or
until the client ends. A client started by a USD Client or Launch Process node ends when
the nodes inside of it are done. A client you started by hand keeps its stages while it
runs, so close what you no longer need.
