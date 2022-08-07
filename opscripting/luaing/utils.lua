local logging = require("lllogger")
local logger = logging:get_logger("luaing.opsbase.utils")

local _M = {}
_M["logger"] = logger

-- we make some global functions local as this will improve performances in
-- heavy loops.
local tostring = tostring
local select = select
local tableconcat = table.concat


function _M.conkat(...)
  --[[
  The loop-safe string concatenation method.
  All args passed are converted to string using tostring()
  ]]
  local buf = {}
  for i=1, select("#",...) do
    buf[ #buf + 1 ] = tostring(select(i,...))
  end
  return tableconcat(buf)
end

return _M