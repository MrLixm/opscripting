# opscripting

![Python](https://img.shields.io/badge/Python->=2.7-4f4f4f?labelColor=3776ab&logo=python&logoColor=FED142)
![lua](https://img.shields.io/badge/Lua->=5.1.5-4f4f4f?labelColor=000090&logo=lua&logoColor=white)
![katana version](https://img.shields.io/badge/Katana->=3.6-4f4f4f?labelColor=111111&logo=katana&logoColor=FCB123)

Package for Foundry Katana software.

Proof of concept on how to integrate the OpScript workflow in a 
version-controled pipeline. OpScript code should not live in the scene in a
studio environment, and should only import code stored in the pipeline arborescence.

This package offer tools and conventions to facilitate the integration of such workflow.

## Content

### lua

2 Low level lua package:

- [luakat](luakat) : api to interact more easily with Katana
- [luabase](luabase) : because everyone need to extend the base lua 


### python

See the [customtooling](customtooling) package. It's a simple API to create
and register a custom type of node called "CustomTool".

The scope goes actually outside OpScripting and could be used to create any kind
of node.

### library

You can see an "example" (prod-ready) in the [opscriptlibrary](opscriptlibrary)
package. This consist on a library of tool declaring each at least one python
file for the node interface, and a .lua file for the OpScript logic.

---

_Only have Katana and `llloger` (lua) for dependencies._


# Documentation

> [![documentation](https://img.shields.io/badge/visit_documentation-blue)](doc/INDEX.md)
> Or see the [./doc directory](doc).
