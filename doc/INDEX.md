# Index

[![root](https://img.shields.io/badge/back_to_root-536362?)](../README.md)
[![INDEX](https://img.shields.io/badge/index-blue?labelColor=blue)](INDEX.md)
[![tools](https://img.shields.io/badge/tools-4f4f4f)](tools.md)

Welcome on the `opscripting` documentation.

# Install

1. Add the repo root directory to the `PYTHONPATH` env variable.

```shell
PYTHONPATH="z/any/opscripting"
# where opscripting/ contains `README.md`, ...
```

2. Add the repo root directory to the `LUA_PATH` env variable.

```shell
LUA_PATH="z/any/opscripting/?.lua"
# where opscripting/ contains `README.md`, ...
```

If you are familiar with the LUA module syntax, this means that all the
lua modules will be accesible from the `opscripting` namespace.

# Use

To import a module, use the [`require`](https://www.lua.org/pil/8.1.html) function.

## In another lua script

```lua
local luaing = {}
luaing.mathing = require("opscripting.luaing.mathing")
luaing.utils = require("opscripting.luaing.utils")
```

It's up to you to see how you want to namespace the module using a table.
In the above example I'm namespacing it using a `luaing` named table so for
example the commly used name `utils` is still free.

## In an OpScript

In my opinion, in a studio environement, no code should ever live in the 
OpScript node itself. It should be written in a library and simply importer
and exectued in the OpScript.

In the `opscripting`, script means to be used directly in an OpScript node
are stored in the [`tools/`](../opscripting/tools) directory.

You can use it as such in the OpScript :

```lua
local script = require("opscripting.tools.attr_math")
script()
```

Make sure to check what the tools script is returning. In most of the case
it will be returning the `run()` function, so you can directly call the result
, but it might also return a table with different functions.