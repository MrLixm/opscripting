--[[
[OpScript]
parameters.location = "location where attribute must be modified"
parameters.applyWhere = "at specific location"
user.attributes = """
(string array): array of string where:
    - [1*n] = path of the attribute relative to the location
    - [2*n] = new DataAttribute type to use, ex: StringAttribute
"""
user.method = """
(string)(optional): which method to use to get data:
    - table : max of 2^27 (134 million) values per attribute
    - array (default): a bit slower, no limit
"""
]]
local _M_ = {}

local luakat = require("luakat")
local luabased = require("luabased")
local logging = require("lllogger")

local logger = logging.getLogger(...)

--- Raise an error for this module.
--- Concat the given arguments to string and pass them as the error's message.
local function err(...)
  local arg = { ... }
  arg.insert("[attr_type_swap]", 1)
  luabased.raising.errorc(unpack(arg))

end

function _M_.run()

  local u_attr_list = luakat.attribute.getUserAttrValue("attributes")
  assert(u_attr_list ~= nil, "[attr_type_swap][run] Missing <user.attributes>")

  local method_table = "table"
  local method_array = "array"
  local u_method = luakat.attribute.getUserAttrValue("method", {method_array})[1]

  local attr
  local data
  local attr_type
  local new_value
  local sample
  local samples

  for i=0, #u_attr_list / 2 - 1 do

    attr = u_attr_list[i*2+1]
    attr_type = luakat.attribute.getAttributeClass(u_attr_list[i*2+2])
    data = luakat.attribute.getAttr(attr)
    new_value = {}

    if u_method == method_table then

      samples = data:getNumberOfTimeSamples()

      for smplindex=0, samples - 1 do
        -- convert the smplindex to sampletime (shutterOpen/Close values)
        sample = data:getSampleTime(smplindex)
        new_value[sample] = data:getNearestSample(sample)
      end

    elseif u_method == method_array then

      samples = data:getSamples()

      for smplindex=0, #samples - 1 do
        sample = samples:get(smplindex)
        new_value[sample:getSampleTime()] = sample:toArray()
      end

    else
      err("[run] method <", u_method, "> not supported.")
    end

    Interface.SetAttr(attr, attr_type(new_value, data:getTupleSize()))

  end

end

return _M_