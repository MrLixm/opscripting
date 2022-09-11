# opscripting

![Python](https://img.shields.io/badge/Python->=2.7-4f4f4f?labelColor=3776ab&logo=python&logoColor=FED142)
![lua](https://img.shields.io/badge/Lua->=5.1.5-4f4f4f?labelColor=000090&logo=lua&logoColor=white)
![katana version](https://img.shields.io/badge/Katana->=3.6-4f4f4f?labelColor=111111&logo=katana&logoColor=FCB123)

Package for Foundry Katana software.

Proof of concept on how to integrate the OpScript workflow in a 
version-controled pipeline. OpScript code should not live in the scene in a
studio environment, and should only import code stored in the pipeline arborescence.

This package offer tools and conventions to facilitate the integration of such workflow.

Most of the update on this package will be to add new custom nodes I created
in the [opscriptlibrary](opscriptlibrary/).

## Content

Most of the content is just linking dependencies and documenting how they
work together.

### lua

2 Low level lua package for OpScripts:

- [luakat](luakat) : api to interact more easily with Katana
- [luabase](luabase) : because everyone needs to extend the base lua 


### python

See the [katananodling](katananodling/) package. It's a simple API to create
and register a custom type of node called "CustomNode".
We will use it to register a subclass of it called `OpScriptCustomNode`.

### library

Included as an example, but also for use, is my collection of existing OpScriptCustomNode
I made. Check the [opscriptlibrary](opscriptlibrary/) package. 

---

_Only have Katana and all the packages visible in this directory as dependencies._


# Documentation

> [![documentation](https://img.shields.io/badge/visit_documentation-blue)](./doc/INDEX.md)
> Or see the [./doc directory](./doc).


# Legal

Apache License 2.0

See [LICENSE.md](LICENSE.md) for full licence.

- ✅ The licensed material and derivatives may be used for commercial purposes.
- ✅ The licensed material may be distributed.
- ✅ The licensed material may be modified.
- ✅ The licensed material may be used and modified in private.
- ✅ This license provides an express grant of patent rights from contributors.
- 📏 A copy of the license and copyright notice must be included with the licensed material.
- 📏 Changes made to the licensed material must be documented

You can request a specific license by contacting me at [monsieurlixm@gmail.com](mailto:monsieurlixm@gmail.com) .

<a href='https://ko-fi.com/E1E3ALNSG' target='_blank'>
<img height='36' style='border:0px;height:36px;' src='https://cdn.ko-fi.com/cdn/kofi1.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' />
</a> 
