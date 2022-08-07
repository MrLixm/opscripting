# ops

[![root](https://img.shields.io/badge/back_to_root-536362?)](../README.md)
[![INDEX](https://img.shields.io/badge/index-blue?labelColor=blue)](INDEX.md)
[![ops](https://img.shields.io/badge/ops-fcb434)](ops.md)

This is where we store script to be used directly in OpScript nodes.

# Conventions

## script structure

The script will usually have a `run()` function that will be the only object
returned when imported as a module :

```lua
local function run()
  -- do something
end

return run
```

So then in the OpScript it can be imported as :

```lua
local script = require("opscripting.ops.attr_math")  -- return run function
script()
```

## OpScript node creation

It is possible to specify a python file that create the expected OpScript node
with the correct setup (instead of saving a macro or else).

The file must be specified alongside the `.lua` script and name exactly as it.

```shell
my_script.lua
# this one handle the node creation
my_script.py
```

This python file must have at least one function named `build` that when called,
will create and configure the node. (Nothing prevent you to create something
else than an OpScript node). This function must return the created node.

Here is a basic example :

```python
from Katana import NodegraphAPI


def build():
    # type: () -> NodegraphAPI.Node
    
    script_path = str(__file__).replace(".py", ".lua")
    with open(script_path, "r") as file:
        script = file.read()

    node = NodegraphAPI.CreateNode("OpScript", NodegraphAPI.GetRootNode())
    node.setName("OpScript_my_script_1")
    
    node.getParameter("script.lua").setValue(script, 0)

    return node


if __name__ in ["__main__", "__builtin__", "Katana"]:
    build()

```

But what would be preferred is creating a custom tool inside. It just a styled 
group node with an opscript node but will allow more flexibility.

```python
import os.path

from opscripting.tooling import createDefaultCustomTool

NAME = os.path.splitext(os.path.basename(__file__))[0]
VERSION = "0.1.0"

def build():
    # type: () -> NodegraphAPI.Node
    
    nodetool = createDefaultCustomTool(NAME)    
    
    script_path = str(__file__).replace(".py", ".lua")
    with open(script_path, "r") as file:
        script = file.read()

    node_opscript = nodetool.getDefaultOpScriptNode()
    node_opscript.getParameter("script.lua").setValue(script, 0)

    return nodetool.node


if __name__ in ["__main__", "__builtin__", "Katana"]:
    build()


```
