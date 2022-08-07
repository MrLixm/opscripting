local logging = require("lllogger")
local logger = logging:get_logger("luaing.opsbase.mathing")

local _M = {}
_M["logger"] = logger

-- we make some global functions local as this will improve performances in
-- heavy loops.
local mathpi = math.pi
local mathfloor = math.floor


function _M.round(a, prec)
    --[[
    SRC: https://stackoverflow.com/questions/9654496/lua-converting-from-float-to-int
    ]]
    return mathfloor(a + 0.5*prec) -- where prec is 10^n, starting at 0
end


function _M.degree_to_radian(rotation)
  --[[
  Args:
    rotation(num): rotation value to convert to radian
  Returns:
    num:
      rotation value converted to radian
  ]]
  return rotation * (mathpi/180.0)
end


function _M.radian_to_degree(radian)
  --[[
  Args:
    radian(num): radian value to convert to degree
  Returns:
    num:
      radian value converted to degree
  ]]
  return radian * (180.0/mathpi)
end


return _M