local logging = require("lllogger")
local logger = logging:get_logger("luaing.opsbase.formatting")

local _M = {}
_M["logger"] = logger

-- we make some global functions local as this will improve performances in
-- heavy loops.
local tostring = tostring
local select = select
local tableconcat = table.concat
local tableinsert = table.insert

function _M.conkat(...)
  --[[
  The loop-safe string concatenation method.
  All args passed are converted to string using tostring()
  ]]
  local buf = {}
  for i = 1, select("#", ...) do
    buf[#buf + 1] = tostring(select(i, ...))
  end
  return tableconcat(buf)
end

function _M.split(str, sep)
  --[[
  Same as python's string.split().

  SRC: https://stackoverflow.com/a/25449599/13806195
  ]]
  local result = {}
  local regex = ("([^%s]+)"):format(sep)
  for each in str:gmatch(regex) do
    tableinsert(result, each)
  end
  return result
end

function _M:errorc(...)
  --[[
  Conacatened error. Arguments are string concatened together.
  ]]
  error(self.conkat(...))
end


return _M