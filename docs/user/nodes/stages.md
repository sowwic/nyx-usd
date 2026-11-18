# Stage nodes

Tags: `stage`

Open a file or create a stage, save it, and close it. The other nodes work on the stage
handle these give, see [Using the nodes](../graphs.md#stage-handles).

| Node | Inputs | Output | What it does |
| --- | --- | --- | --- |
| **Open Stage**<br>`usd:open_stage` | `path` | stage | Opens a USD file in the client. |
| **Create Stage**<br>`usd:create_stage` | `path` | stage | Creates a stage in the client, in memory if no file is given. |
| **Save Stage**<br>`usd:save_stage` | `stage`<br>`path` | stage | Saves a stage to its file, or exports it to the given one. |
| **Close Stage**<br>`usd:close_stage` | `stage` | none | Closes a stage in the client without saving it. |

## Notes

- **Create Stage** without a `path` makes a stage in memory. Give a `path` to have a file
  to **Save Stage** to, or give the path when saving.
- **Save Stage** with an empty `path` saves the file the stage was opened from or created
  with. With a `path` it exports the stage there and the original file is left alone.
- **Open Stage** fails with the reason from USD when the file can't be opened.
- A stage stays open in the client until **Close Stage**, see
  [Starting a client](../starting-a-client.md#how-long-things-live).
