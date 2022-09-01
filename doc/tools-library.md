# tools-library

[![root](https://img.shields.io/badge/back_to_root-536362?)](../README.md)
[![INDEX](https://img.shields.io/badge/index-blue?labelColor=blue)](INDEX.md)
[![tools-library](https://img.shields.io/badge/tools--library-fcb434)](tools-library.md)


This will explain how to store tools to be registered later.

A "tools library" is a simple directory that will contain a `__init__.py`,
making it a python package, and a bunch of python modules with
their associated lua file (for OpScripting)

```
myLibrary/
    __init__.py
    toolAlpha.lua
    toolAlpha.py
    toolBeta.lua
    toolBeta.py
```

The .py file will be in charge to describe how to create the node, and the .lua
file, the entry point for the OpScript, that will be imported.

You may find multiple libraries of tool to register.

> **Info**: note that actually you could only have a single .py file declaring
> a node interface to register simple tools.


# Structure

The first task will be to determine the name for your tool. It will be used
to name the files and access them. Try to think of something unique because
you really don't want duplicates in your tool library.

You have a name you will have to "slugify" it, so you can use it in file names.
On my side I decided to stick to the `snake_case` conventions.

ex: `Tree generator -> tree_generator`

## lua file

Seems logical to start by the reason of why we are doing all of this. This
will hold the logic **specific to our tool**. For everything else that
looks to be more abstract, it's best to put it in `luakat` or `luabase`.

This file will drive how we will build the node in python later, mainly for
its `oparg` that must be implemented as user parameters on the OpScript node,
but also because it might require to use some other nodes before/after the OpScript.
So it is good to start by here.

### file-name

Simply the slugified tool name. If for whatever reason you ever need 2 lua module
for this tool, just add the desired suffix like `tree_generator -> tree_generator_core`


### content

You can do whatever you want inside, but it will usually have a `run()` function
that will be the only object returned when imported as a module :

```lua
local function run()
  -- do something
end

return run
```

So then in the OpScript it can be imported as :

```lua
local script = require("opscriptlibrary.attr_math")  -- return run function
script()
```

Nothing prevent you to use the other lua way to create a module by returning
a table, but it is safe to say that is most of the case, a simple function is 
enough.


## node creation via python

It is possible to specify a python file that create the expected OpScript node
with the correct setup (instead of saving a macro or else). It will actually
be registered as a custom type of node in Katana.

### file-name

Same as for the lua file, the slugified tool name. If you need more than one
file, to not break the registering workflow it is recommended to use a python
package instead.

```shell
__init__.py
my_script.lua
# this one handle the node creation
my_script.py

# if very big tool
my_script.lua
my_script/
    __init__.py
    gen_something.py
    editor.py
    node.py
```

### content

The registering process will except one thing : a package whose namespace list
all the `katananodling.entities.BaseCustomNode` subclasses that must be registered.

So all we have to do will be to subclass `BaseCustomNode`. But this class is 
actually a "general" class made for any kind of tool. In our case we will
create a tool for OpScripting, so it seems logical to use a subclass of it
named `OpScriptCustomNode` that will do half the work for us:

```python
import os.path
from katananodling.entities import OpScriptCustomNode


# class can actually be named anything but let's keep it clean :)
class MyToolName(OpScriptCustomNode):
  name = "MyToolName"  # identifier used to register the tool in Katana !
  version = (0, 1, 0)
  color = None
  description = "What the tool does in a few words."
  author = "<FirstName Name email@provider.com>"

  luamodule = os.path.splitext(os.path.basename(__file__))[0]

  def _build(self):
    script = """
local script = require("opscriptlibrary.{module}")
script()"""
    script = script.format(module=self.luamodule)

    node = self.getDefaultOpScriptNode()
    node.getParameter("script.lua").setValue(script, 0)
    return

```

The above is a minimal working example that will simply load the lua script.

You simply have to override the `_build` method and write there how you want
your node to be configured. There is also a bunch of mandatory class variable
to override.

## registering process

As mentioned above, lua modules are registered by settings the `LUA_PATH`
environment variable. (see [INDEX.md](INDEX.md))and are simply imported into
the OpScript using `require()`.

On the python side it's a bit more complex. You can have a look at 
[../katananodling/loader.py](../katananodling/loader.py) to see what the code
actually does. Else let's start by the end :

- Each tool **class** will be registered in Katana using `NodegraphAPI.RegisterPythonNodeFactory` 
and a callback function when the node is created.
It will also receive a flavor using `NodegraphAPI.AddNodeFlavor` so you can 
quickly retrieve all custom tools.

- To retrieve the tool class we iterate through the given package object in
search for all objects which are subclasses of BaseCustomNode (and whose name
doesn't start with `_`)

- Now how do we retrieve the package as a python module object ? We will simply
do a :
  ```python
  package = importlib.import_module(package_id)  # type: ModuleType
  ```

- But what is `package_id` ? It's simply the name of this package. This mean
it has to be registered in the `PYTHONPATH` so it can be imported.

- And initally we have the `registerNodesFor()` function that will take as argument
a list of package name to import.

### library python configuration

```python

registerNodesFor(["libStudio", "libProject"])
# implies :

root/  # <-- in PYTHONPATH
    libStudio/
        __init__.py  # <-- contains "from . import MySubclass ..."
        tree_generator.py
        ...
    libProject/
        __init__.py
        ...
```

## documentation

It is possible to specify a documentation file that can be quickly opened by
the artist from Katana using an automatized button on the tool's node.

The file just has to be named exactly like the tool's python module/package
and have the `.md` extension.

```
myLibrary/
    __init__.py
    tree_generator.py
    tree_generator.lua
    tree_generator.md
```

---

[![root](https://img.shields.io/badge/back_to_root-536362?)](../README.md)
[![INDEX](https://img.shields.io/badge/index-blue?labelColor=blue)](INDEX.md)
[![tools-library](https://img.shields.io/badge/tools--library-fcb434)](tools-library.md)
