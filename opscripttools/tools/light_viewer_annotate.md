# light_viewer_annotate

Welcome on the `light_viewer_annotate` tool documentation.

It is recommended then to set the CEL to match all light locations.
Usually this would work fine :

```
/root/world/lgt//*{@type=="light"}
```

You can of course modify the CEL to be more specific if you don't want to annotate 
all the lights.

# API

Listed are only objects useful for extend the script features/support.


## !["class"](https://img.shields.io/badge/"class"-6F5ADC) Light

### ![attribute](https://img.shields.io/badge/attribute-4f4f4f) `table` Light.tokens

#### ![attribute](https://img.shields.io/badge/attribute-4f4f4f) `table` Light.tokens.$token

#### ![attribute](https://img.shields.io/badge/attribute-4f4f4f) `table` Light.tokens.$token.$renderer

##### ![attribute](https://img.shields.io/badge/attribute-353535) `function` Light.tokens.$token.$renderer.func

optional if not `params`. A function to execute that return the value
for the corresponding token on the current location. As you guessed it the `params`
keys just under are the argument passed to this function.

##### ![attribute](https://img.shields.io/badge/attribute-353535) `table` Light.tokens.$token.$renderer.params

optional. Arguments for the `func` key function.

### ![method](https://img.shields.io/badge/method-4f4f4f) Light:get
### ![method](https://img.shields.io/badge/method-4f4f4f) Light:to_annotation


### ![function](https://img.shields.io/badge/function-6F5ADC) getLightRenderer

Return a string identifying the render-engine used by the currently
visited light.

```
Raises:
    when a renderer can't be found for the current light location
Returns:
    str:
```


## ![function](https://img.shields.io/badge/function-6F5ADC) run

Create the annotation for the current light visited by the OpScript.

# Development

## New render-engine

_renderer=render-engine_

You will need to modify the `getLightRenderer()` function and
the `Light` table.

### ![function](https://img.shields.io/badge/function-4f4f4f) getLightRenderer

Must return a string identifying the current render-engine used by the light.
This string must then be used as a key for the `Light.tokens.$token.$renderer`.

To add a renderer, copy/paste the previous `elseif` line and then modify the
`string.find` pattern based on how the `material` shader's name start. Just have
a look at the attribute on your light located in the `material` group.

### ![attribute](https://img.shields.io/badge/attribute-4f4f4f) Light.tokens.$token.$renderer

You can then add a key for each token in the `Light.tokens` table that correspond
to your new renderer name returned in `get_light_renderer()`.

```lua

local Light = {
  
    ["tokens"] = {
      
      ["exposure"] = {
        ["myRenderer"] = {
          func = getLightAttr,
          params = { { "material.myRendererLightParams.exposure" }, 0 },
        },
        ["prman"] = {
          func = getLightAttr,
          params = { { "material.prmanLightParams.exposure" }, 0 },
        },
      },
      -- ... other tokens
      
    }
}
```

## New token

You will only need to modify the `Light` table.



---

[![root](https://img.shields.io/badge/back_to_root-536362?)](../README.md)
