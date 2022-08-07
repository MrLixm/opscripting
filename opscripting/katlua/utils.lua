local logging = require("lllogger")
local logger = logging:get_logger("katlua.utils")

local _M = {}
_M["logger"] = logger


function _M.getKatanaVersion()
  --[[
  Returns:
    num:
      Katana version as a float number like 451.00008
  ]]

  local version = Config.Get("KATANA_VERSION") -- "4.5.1.000008"
  version = version:gsub("%.", "", 2)
  version = tonumber(version)
  return version

end


return _M