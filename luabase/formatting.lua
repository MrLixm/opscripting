local mathing = require("luabase.mathing")
local StrFmtSettings =  require("luabase.formatting_settings")
local _M = {}

-- we make some global functions local as this will improve performances in
-- heavy loops.
local tostring = tostring
local select = select
local tableconcat = table.concat
local tableinsert = table.insert
local stringrep = string.rep
local type = type

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

function _M:stringify(source, index, settings)
  --[[
  Convert the source to a readable string , based on it's type.
  Args:
    source(any): any type
    index(int): recursive level of stringify
    settings(StrFmtSettings or nil): configure how source is formatted
  ]]
  if not settings then
    settings = StrFmtSettings:new()
  end

  if not index then
    index = 0
  end

  if (type(source) == "table") then
    source = self:table2string(source, index, settings)

  elseif (type(source) == "number") then
    source = tostring(mathing.round(source, settings.numbers.round))

  elseif (type(source) == "string") and settings.strings.display_quotes == true then
    source = self:conkat("\"", source, "\"")

  elseif (type(source) == "string") then
    -- do nothing

  else
    source = tostring(source)

  end

  return source

end

function _M:table2string(tablevalue, index, settings)
  --[[
  Convert a table to human readable string.
  By default formatted on multiples lines for clarity. Specify tdtype=oneline
    to get no line breaks.
  If the key is a number, only the value is kept.
  If the key is something else, it is formatted to "stringify(key)=stringify(value),"
  If the table is too long (max_length), it is formatted as oneline
  Args:
    tablevalue(table): table to convert to string
    index(int): recursive level of conversions used for indents
    settings(StrFmtSettings or nil):
      Configure how table are displayed.
  Returns:
    str:
  ]]

  -- check if table is empty
  if next(tablevalue) == nil then
    return "{}"
  end

  -- if no index specified recursive level is 0 (first time)
  if not index then
    index = 0
  end

  local tsettings
  if settings and settings.tables then
    tsettings = settings.tables
  else
    tsettings = StrFmtSettings:new().tables
  end

  local linebreak_start = "\n"
  local linebreak = "\n"
  local inline_indent = stringrep(
      " ", index * tsettings.indent + tsettings.indent
  )
  local inline_indent_end = stringrep(
      " ", index * tsettings.indent
  )

  -- if the table is too long make it one line with no line break
  if #tablevalue > tsettings.length_max then
    linebreak = ""
    inline_indent = ""
    inline_indent_end = ""
  end
  -- if specifically asked for the table to be displayed as one line
  if tsettings.linebreaks == false then
    linebreak = ""
    linebreak_start = ""
    inline_indent = ""
    inline_indent_end = ""
  end

  -- to avoid string concatenation in loop using a table
  local outtable = {}
  outtable[#outtable + 1] = "{"
  outtable[#outtable + 1] = linebreak_start

  for k, v in pairs(tablevalue) do
    -- if table is build with number as keys, just display the value
    if (type(k) == "number") and tsettings.display_indexes == false then
      outtable[#outtable + 1] = inline_indent
      outtable[#outtable + 1] = self:stringify(v, index + 1, settings)
      outtable[#outtable + 1] = ","
      outtable[#outtable + 1] = linebreak
    else

      if (type(v) == "function") and tsettings.display_functions == false then
        outtable[#outtable + 1] = ""
      else
        outtable[#outtable + 1] = inline_indent
        outtable[#outtable + 1] = self:stringify(k, index + 1, settings)
        outtable[#outtable + 1] = "="
        outtable[#outtable + 1] = self:stringify(v, index + 1, settings)
        outtable[#outtable + 1] = ","
        outtable[#outtable + 1] = linebreak
      end

    end
  end
  outtable[#outtable + 1] = inline_indent_end
  outtable[#outtable + 1] = "}"
  return tostring(tableconcat(outtable))

end

return _M