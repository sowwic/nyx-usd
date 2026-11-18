# User Guide

This guide is for people who use the USD nodes in Nyx.

## Pages

| Page | What you learn |
| --- | --- |
| [Installation](installation.md) | The plugin for Nyx, `nyx_usd` for the interpreter with USD, and checking both. |
| [Starting a client](starting-a-client.md) | The USD Client node, Launch Process, starting one by hand, Maya and Blender. |
| [Using the nodes](graphs.md) | Stage handles, wiring, errors, and two worked examples. |
| [Nodes](nodes/index.md) | Every node: inputs, output and what it does, by area. |

## How it fits together

```text
   Nyx (Python 3.14)                        Interpreter with USD
┌──────────────────────┐   it connects out   ┌──────────────────────┐
│ Bridge server        │ ◀────────────────── │ nyx_bridge client    │
│ USD nodes            │ ── operation ─────▶ │ imports nyx_usd.ops  │
│                      │ ◀── result ──────── │ and runs it on pxr   │
└──────────────────────┘                     └──────────────────────┘
```

1. Nyx listens on a local port and holds a secret token.
2. An interpreter that has USD starts a client, which connects to Nyx. The **USD Client**
   node can start it for you.
3. A USD node inside a **Remote Client** node sends the name of an operation and its
   inputs. The client calls `nyx_usd.ops.<operation>`, which uses `pxr`, and answers with
   the result.

The stages live in the client, not in Nyx. What travels between nodes is a **stage
handle**, a string naming an opened stage, see [Using the nodes](graphs.md).

Protocol and server details are in the
[nyx-bridge documentation](https://sowwic.github.io/nyx-bridge/).
