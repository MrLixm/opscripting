--[[
Annotate (& color) lights in the viewer using their attributes.

Supported Render-engines: Arnold, 3Delight, RenderMan

[OpScript]
parameters.location = "/root/world/lgt//*{@type=="light"}"
parameters.applyWhere = "at locations matching CEL"
user.annotation_colored = "(bool)(true): true to colro the annotation in the viewer"
user.lights_colored = "(bool)(true): true to color the light in the viewer"
user.annotation_template = """
  (str)("<name>"): Use tokens to build the annotation for each light.
  tokens are defined in Light.tokens and are surrounded with <>
"""
user.color_hue = "(float)(1): 0-1 range"
user.color_saturation = "(float)(1): 0-1 range"
user.color_value = "(float)(1): 0-1 range"
]]
local _M_ = {}

local luakat = require("luakat")
local luabased = require("luabased")
local logging = require("lllogger")

local logger = logging.getLogger(...)

--- scene graph location of the current light visited
--- @type string
local LOCATION = Interface.GetInputLocationPath()

-- we make some global functions local as this will improve performances in
-- heavy loops.
local stringfind = string.find

--- Raise an error for this module.
--- Concat the given arguments to string and pass them as the error's message.
local function err(...)
  local arg = { ... }
  arg.insert("[light_viewer_annotate]", 1)
  luabased.raising.errorc(unpack(arg))
end

--- From the currently visited light location, return which render-engine it
--- was build for.
--- Raise an error if the renderer can't be found.
---@return string one of "ai", "dl", "prman"
local function getLightRenderer()

  local mat = Interface.GetAttr("material")
  -- the shader name should always be the first Group index 0
  if stringfind(mat:getChildName(0), "arnold") then
    return "ai"
  elseif stringfind(mat:getChildName(0), "dl") then
    return "dl"
  elseif stringfind(mat:getChildName(0), "prman") then
    return "prman"
  else
    err(
        "[getLightRenderer] Can't find a render engine for the light ",
        LOCATION
    )
  end

end

local RENDERER = getLightRenderer()

--- @param attrs_list table numerical table of attributes path. Function return at the first attribute to return a value.
--- @param default_value any value to return if all attributes return nothing, pass ``error`` to raise an error instead.
--- @return any depends on parameters values
local function getLightAttr(attrs_list, default_value)

  for i = 1, #attrs_list do

    local attr = Interface.GetAttr(attrs_list[i])
    if attr then
      return attr:getNearestSample(0)
    end

  end

  if default_value == error then
    err(
        "[getLightAttr] No attribute found from ",
        luabased.stringing.stringify(attrs_list)
    )
  else
    return default_value
  end

end

--- @return string name of the light based on its scene graph location.
local function getLightName()
  return luakat.location.getLocationName(LOCATION)
end


--- Light table object
---
--- the ``tokens`` key hold all the supported tokens.
--- - Each token key hold render-engine keys
--- - each render-engine key hold a table with a ``func`` and a ``params`` key.
---
--- the default value for ``getLightAttr`` ``params`` is returned if the attribute
--- is not set locally (not modified)
local Light = {

  ["tokens"] = {

    ["name"] = {
      ["ai"] = { func = getLightName },
      ["dl"] = { func = getLightName },
      ["prman"] = { func = getLightName }
    },

    ["aov"] = {
      ["ai"] = {
        func = getLightAttr,
        params = { { "material.arnoldLightParams.aov" }, "default" },
      },
      ["dl"] = {},
      ["prman"] = {
        func = getLightAttr,
        params = { { "material.prmanLightParams.lightGroup" }, "none" },
      },
    },

    ["color"] = {
      ["ai"] = {
        func = getLightAttr,
        params = { { "material.arnoldLightParams.color" }, { 1, 1, 1 } },
      },
      ["dl"] = {
        func = getLightAttr,
        params = { { "material.dlLightParams.color" }, { 1, 1, 1 } },
      },
      ["prman"] = {
        func = getLightAttr,
        params = { { "material.prmanLightParams.lightColor" }, { 1, 1, 1 } },
      },
    },

    ["samples"] = {
      ["ai"] = {
        func = getLightAttr,
        params = { { "material.arnoldLightParams.samples" }, 1 },
      },
      ["dl"] = {},
      ["prman"] = {
        func = getLightAttr,
        params = { { "material.prmanLightParams.fixedSampleCount" }, 0 },
      },
    },

    ["exposure"] = {
      ["ai"] = {
        func = getLightAttr,
        params = { { "material.arnoldLightParams.exposure" }, 0 },
      },
      ["dl"] = {
        func = getLightAttr,
        params = { { "material.dlLightParams.exposure" }, 0 },
      },
      ["prman"] = {
        func = getLightAttr,
        params = { { "material.prmanLightParams.exposure" }, 0 },
      },
    },

    ["intensity"] = {
      ["ai"] = {
        func = getLightAttr,
        params = { { "material.arnoldLightParams.intensity" }, 1 },
      },
      ["dl"] = {
        func = getLightAttr,
        params = { { "material.dlLightParams.intensity" }, 1 },
      },
      ["prman"] = {
        func = getLightAttr,
        params = { { "material.arnoldLightParams.intensity" }, 1 },
      },
    }

  }

}

--- Return the light attribute value for the given attribute name
--- @return any type depends of what's queried, can be nil
function Light:get(attr_name)
  local attr = self.tokens[attr_name] or {}
  attr = attr[RENDERER] or {}  -- return the data for the current render-engine

  local func = attr.func
  local params = attr.params
  if func then
    if params then
      return func(unpack(attr.params))
    else
      return func()
    end
  else
    return nil
  end
end

--- @param annotation string annotation template submitted by the user (with tokens)
---@return string annotation with the tokens replaced
function Light:to_annotation(annotation)
  for attr_name, _ in pairs(self.tokens) do
    local token = ("<%s>"):format(attr_name)
    local value = luabased.stringing.stringify(self:get(attr_name))
    annotation = string.gsub(annotation, token, value)
  end

  return annotation

end

function _M_.run()

  local u_annotation_template = luakat.attribute.getUserAttrValue("annotation_template", "<name>")
  local u_annotation_colored = luakat.attribute.getUserAttrValue("annotation_colored", 1)
  local u_lights_colored = luakat.attribute.getUserAttrValue("lights_colored", 1)

  local u_hsl_h = luakat.attribute.getUserAttrValue("color_hue", 0)
  local u_hsl_s = luakat.attribute.getUserAttrValue("color_saturation", 1)
  local u_hsl_v = luakat.attribute.getUserAttrValue("color_value", 1)

  -- 1. Process the annotation
  local annotation = Light:to_annotation(u_annotation_template)
  Interface.SetAttr(
      "viewer.default.annotation.text",
      StringAttribute(annotation)
  )

  -- 2. Process the color
  -- initial color is linear
  local color = Light:get("color") -- table of float or nil
  color = luabased.coloring.hsv(color, u_hsl_h, u_hsl_s, u_hsl_v)
  -- apply a basic 2.2 transfer-function for display
  color[1] = color[1] ^ 2.2
  color[2] = color[2] ^ 2.2
  color[3] = color[3] ^ 2.2

  if u_annotation_colored == 1 then
    Interface.SetAttr(
        "viewer.default.annotation.color",
        FloatAttribute(color or { 0.1, 0.1, 0.1 })
    )
  end

  if u_lights_colored == 1 then
    Interface.SetAttr(
        "viewer.default.drawOptions.color",
        FloatAttribute(color or { 0.1, 1.0, 1.0 })
    )
  end

  --print("[LightViewerAnnotate][run] Finished. Annotation set to <"..annotation..">")

end

return _M_