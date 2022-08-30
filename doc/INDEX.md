# Index

[![root](https://img.shields.io/badge/back_to_root-536362?)](../README.md)
[![INDEX](https://img.shields.io/badge/index-blue?labelColor=blue)](INDEX.md)
[![tools-library](https://img.shields.io/badge/tools--library-4f4f4f)](tools-library.md)

Welcome on the `opscripting` package documentation.

# What

`opscripting` is a "proof of concept" that we can have a better OpScript
workflow in a pipelined environement.

In my opinion, OpScript code should not live in the scene, and should only
import code stored in the pipeline arborescence.

This package offers the tools to get started on that road, but would deserve to
be a bit modified if actually used in a studio pipeline.

# Install

> **Info**: 
> You can check [../dev/launcher.Katana...sh](../dev/launcher.Katana-4.5.1.sh) to see some
> launcher examples.

This will explain how to use the package "as it is" but as mentionned,
ideally it would be better to create separate packages for all the components.


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
lua modules will be accesible from the `opscriptlibrary` namespace.

3. Add the only dependency `llloger` to the `LUA_PATH` too.

> **Download** : https://github.com/MrLixm/llloger/blob/main/lllogger.lua

```shell
LUA_PATH="$LUA_PATH:z/any/lllogerInstallDirectory/?.lua"
# where lllogerInstallDirectory/ contains `llloger.lua`, ...
```

llloger is directly imported as `require("llloger")`

## Registering tools

For the artist to access the created tool, you need to register them in Katana.

### 1. Registering as nodes

For this you will just need to run during Katana startup something like:

```python
from customtooling.loader import registerTools

# make sure "opscriptlibrary" parent dir is in the PYTHONPATH
locations_to_register = ("opscriptlibrary",)

registerTools(locations_to_register)
```

Make sure this is only executed once AND in gui and headless mode. I personally
put them in a `Startup/init.py` file registered in `KATANA_RESOURCES`.

### 2. Registering the layeredMenu

The above will allow the artist to create the tool via the traditional
`Tab` shortcut, but they will be drowned among the other nodes. To find
those nodes quicker there is a pre-made layeredMenu available that
you can register :

```python
from Katana import LayeredMenuAPI
import customtooling.menu

layered_menu = customtooling.menu.getLayeredMenuForAllCustomTool()
LayeredMenuAPI.RegisterLayeredMenu(layered_menu, "customtooling")
```

There is a demo in [../dev/KatanaResources/UIPlugins](../dev/KatanaResources/UIPlugins).
(you can add [../dev/KatanaResources](../dev/KatanaResources) to the `KATANA_RESOURCES` variable.)


# Lua Use

To import a module, use the [`require`](https://www.lua.org/pil/8.1.html) function.

## In an OpScript

No code should be found in the OpScript node. It should only import and
execute what it needs.

This means we need to store the lua code on disk in a file. The proposed 
convention is to store those file in a directory that will be registered in
the LUA_PATH.

```shell
opscriptlibrary/  <- # parent directory registered in LUA_PATH   
    my_script.lua
```

You can then use it as such in the OpScript :

```lua
local script = require("opscriptlibrary.my_script")
script()  -- if your module return a function
```

Make sure to check what the tools script is returning. In most of the case
it will be returning the `run()` function, so you can directly call the result
, but it might also return a table with different functions.

## In another lua script

In the OpScript script file you created as mentioned above, you might also
want to import other modules to reduce duplicated code.

This package offers 2 lua package `luaing`, `luakat` as a base to create OpScripts.

Here is how you could import `luaing` :

```lua
local luaing = {}
luaing.mathing = require("luaing.formatting")
luaing.utils = require("luaing.utils")
```

It's up to you to see how you want to namespace the module using a table.
In the above example I'm namespacing it using a `luaing` named table so for
example the commly used name `utils` is still free.

# Recommendation

This package was made with a studio pipeline in mind but kept on a structure
accesible for a smaller scale. 

The following directory better be split in their own package :

- `luabase`
- `luaing`
- `customtooling`

and of course `opscriptlibrary`. In my example I only have one library location
but you could technically have multiple of them at different stage of 
the pipeline (studio -> prod -> sequence ...)