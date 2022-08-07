--[[
OpScript for Foundry's Katana software

Divide the current render resolution by the given amount.
The divider amount can be supplied or by creating an OpArg (user.divider) or by creating a gsv "resolution_divider".

[OpScript]
location = "/root"
applyWhere = "at specific location"
user.divider = "(int) amount to divide the current resolution by"
]]
local luaing = {}
luaing.mathing = require("opscripting.luaing.mathing")
luaing.utils = require("opscripting.luaing.utils")
local logging = require("lllogger")

local logger = logging:get_logger("ops.resolution_divide")


local function getDivider()
  --[[
  Return the resolution divider from a graphstatevariable named
  "resolution_divider" if it exists, else from the OpArg `user.divider`

  Returns:
      num: resolution divider
  ]]
  local gsv_value = Interface.GetGraphStateVariable("resolution_divider")
  if gsv_value then
    return tonumber(gsv_value:getValue())
  end

  local argvalue = Interface.GetOpArg("user.divider")
  if argvalue then
    return argvalue:getValue()
  end

  error(
    "No divider found. Specify a \"resolution_divider\" GSV or the \z
    \"user.divider\" argument."
  )

end


local function run()

  local frame = Interface.GetCurrentTime() -- int
  local divider = getDivider(frame)

  -- divider == 0 or 1 means we doesn't want to apply any resolution reformating.
  if divider == 0 or divider==1 then
    return
  end

  local resolution = Interface.GetAttr("renderSettings.resolution"):getValue()
  resolution = ResolutionTable.GetResolution(resolution)
  if not resolution then
    error(
      "[resolution_divide][run] renderSettings.resolution has an issue.\z
      ResolutionTable.GetResolution() returned nil."
    )
    return
  end

  local new_resolution_x = luaing.mathing.round(resolution:getXRes() / divider, 0)
  local new_resolution_y = luaing.mathing.round(resolution:getYRes() / divider, 0)
  local new_resolution =  luaing.utils.conkat(new_resolution_x,"x",new_resolution_y) -- str

  Interface.SetAttr("renderSettings.resolution", StringAttribute(new_resolution))
  logger:info("[run] Resolution set to ", new_resolution)

end

return run