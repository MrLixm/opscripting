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

3. Add the only dependency `llloger` to the `LUA_PATH` too.

> **Download** : https://github.com/MrLixm/llloger/blob/main/lllogger.lua

```shell
LUA_PATH="$LUA_PATH:z/any/lllogerInstallDirectory/?.lua"
# where opscripting/ contains `README.md`, ...
```

llloger is directly imported as `require("llloger")`

## Registering tools

For the artist to access the created tool, you need to register the
LayerMenu created for them.

For this you will just need to run during Katana startup something like:

```python
from Katana import LayeredMenuAPI

import opscripting.integrating

layeredMenu = opscripting.integrating.getLayeredMenu()
LayeredMenuAPI.RegisterLayeredMenu(layeredMenu, "opscripting")
```

As you can see the `integrating` python already offer a convenient function
that create the LayeredMenu to register.

There is a proof-of-concept in [dev/KatanaResources/UIPlugins](dev/KatanaResources/UIPlugins).
(you can add [dev/KatanaResources](dev/KatanaResources) to the `KATANA_RESOURCES` variable.)


# Use

To import a module, use the [`require`](https://www.lua.org/pil/8.1.html) function.

## In another lua script

```lua
local luabase = {}
luabase.mathing = require("luabase.mathing")
luabase.utils = require("luabase.utils")
```

It's up to you to see how you want to namespace the module using a table.
In the above example I'm namespacing it using a `luabase` named table so for
example the commly used name `utils` is still free.

## In an OpScript

In my opinion, in a studio environement, no code should ever live in the 
OpScript node itself. It should be written in a library and simply importer
and exectued in the OpScript.

In the `opscripting`, script means to be used directly in an OpScript node
are stored in the [`tools/`](../customtooling/tools) directory.

You can use it as such in the OpScript :

```lua
local script = require("opscripting.tools.attr_math")
script()
```

Make sure to check what the tools script is returning. In most of the case
it will be returning the `run()` function, so you can directly call the result
, but it might also return a table with different functions.

# Recommandation

This package was made with a studio pipeline in mind but still accesible at a 
smaller case. 

In my opinion the `tools/` directory might better live in a seperate repository,
and even same for `luakat` and `luabase` that should also have their own
repository to keep things clean.