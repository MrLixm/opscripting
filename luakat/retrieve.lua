local luabase = {}
luabase.formatting = require("luabase.formatting")
local logging = require("lllogger")

local logger = logging:get_logger("luakat.retrieve")

local _M = {}
_M["logger"] = logger

function _M.getUserAttr(name, default)
  --[[
  Return an OpScript user attribute.
  If not found return the default_value.

  OpScript user attribute are not assumed to be multi-sampled.

  Args:
      name(str): attribute location (don't need the <user.>)
      default(any): value to return if user attr not found.

  Returns:
      table or any: table of value on attribute or default value
  ]]
  local argvalue = Interface.GetOpArg(string.format("user.%s", name))

  if argvalue then
    return argvalue:getNearestSample(0)

  else
    return default

  end

end

function _M.getAttr(attr_path)
  --[[
  Get the given attribute on the currently visited location.
  Raise an error is nil result is found.

  Args:
    attr_path(str): path of the attribute on the location

  Returns:
    DataAttribute:
  ]]
  local lattr = Interface.GetAttr(attr_path)

  if not lattr then
    luabase.formatting:errorc(
        "[getAttr] Attr <",
        attr_path,
        "> not found on location ",
        Interface.GetInputLocationPath()
    )
  end

  return lattr

end

function _M.getAttributeClass(dataattribute)
  --[[
  Returned a non-instanced version of the DataAttribute given in arg.

  Args:
    dataattribute(str or DataAttribute):
      DataAttribute instance or name of the DataAttribute class
  Returns:
    table: DataAttribute class not instanced
  ]]
  if dataattribute == "IntAttribute" or Attribute.IsInt(dataattribute) == true then
    return IntAttribute
  elseif  dataattribute == "FloatAttribute" or Attribute.IsFloat(dataattribute) == true then
    return FloatAttribute
  elseif  dataattribute == "DoubleAttribute" or Attribute.IsDouble(dataattribute) == true then
    return DoubleAttribute
  elseif  dataattribute == "StringAttribute" or Attribute.IsString(dataattribute) == true then
    return StringAttribute
  else
    luabase.formatting:errorc(
        "[getAttributeClass] passed class type <",
        dataattribute,
        "> is not supported."
    )
  end
end

return _M