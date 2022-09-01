# katananodling

[![root](https://img.shields.io/badge/back_to_root-536362?)](../README.md)
[![INDEX](https://img.shields.io/badge/index-536362?labelColor=blue)](INDEX.md)
[![katananodling](https://img.shields.io/badge/katananodling-fcb434)](katananodling.md)
[![tools-library](https://img.shields.io/badge/tools--library-536362)](tools-library.md)

Documentation for the `katananodling` python package.

This package allows to register a custom type of node called CustomTool that
allow to quickly create new node to extend Katana. It is similar to SuperTools
with the difference it removes the need of going through Qt to build the interface.

The process of registering is also more flexible where you say which location
to register to a function called at startup. 
Those locations are a usual python package whose namespace list all the
CustomToolNode subclasses that can be registered.

# Registering CustomTools

This is achieved via the `registerTools` function of the 
[../katananodling/loader.py](../katananodling/loader.py) module.

This function will expect a list of package name as argument. Those package
must be already registered in the PYTHONPATH, so they can be imported.

```python
from katananodling.loader import registerTools

locations_to_register = ["libStudio", "libProject", "opscriptlibrary"]

registerTools(locations_to_register)
```

Each of this package will be imported and iterated directly to find the 
CustomToolNode subclasses. To declare a subclass to be registered, you just
need to import it in the `__init__` of your package :

```toml
parentDir/  # <- registered in PYTHONPATH
    libProject/
        __init__.py
            """
            from .myTool import MyTool
            """
        myTool.py
            """
            from katananodling.nodebase import CustomToolNode

            class MyTool(CustomToolNode):
            
                name = "MyToolName"
                ...
                
                def _build(self):
                    ...
            """
```

How you organize the package is up to you but it is recommended to create one
module per subclass.


## Register process in details.

Starting **by the end**, here is the registration process :

- Each tool **class** will be registered in Katana using `NodegraphAPI.RegisterPythonNodeFactory` 
and a callback function when the node is created.
It will also receive a flavor using `NodegraphAPI.AddNodeFlavor` so you can 
quickly retrieve all custom tools.

- To retrieve the tool class we iterate through the given package object in
search for all objects which are subclasses of CustomToolNode (and whose name
doesn't start with `_`)

- Now how do we retrieve the package as a python module object ? We will simply
do a :
  ```python
  package = importlib.import_module(package_id)  # type: ModuleType
  ```

- But what is `package_id` ? It's simply the name of this package. This mean
it has to be registered in the `PYTHONPATH` so it can be imported.

- And initally we have the `registerTools()` function that will take as argument
a list of package name to import.


# Creating CustomTools

A custom tool will always be a subclass of `nodebase.CustomToolNode`, but
it can also be a subclass of a subclass of CustomToolNode and so on ...

As it most basic structure, a CustomTool is :

- python :
  - some class variable for information to keep track of it
  - a `_build()` method to do whatever you want on the node.
  - an optional `upgrade()` method to handle porting of older version to newer ones.

```python
from katananodling.nodebase import CustomToolNode

# class can actually be named anything but let's keep it clean :)
class MyToolName(CustomToolNode):

    name = "MyToolName"  # identifier used to register the tool in Katana !
    version = (0, 1, 0)
    color = None
    description = "What the tool does in a few words."
    author = "<FirstName Name email@provider.com>"
    maintainers = []

    def _build(self):
      
        p = self.user_param.createChildNumber("amount", 666)
        hint = {
            "slider": True,
            "slidermax": 666,
            "help": "whatever",
        }
        p.setHintString(repr(hint))

    def upgrade(self):
        
        if self.version == self.about.version:
            return
        # now do whatever you need to upgrade

```


# Good to know

Be aware that you cannot open a scene with saved CustomTool if at least the base
CustomToolNode class is not registered in Katana. But you can open a scene
with CustomTool subclass even if they are not registered.