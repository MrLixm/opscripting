--[[
Supports for multiple time-samples.

[OpScript]
parameters.location = "location where attribute must be modified"
parameters.applyWhere = "at specific location OR at locations matching CEL"
user.attributes = """
  (string array)
  list of attribute path to apply the same math operation
  - [1*n] = path of the attribute relative to the location
  - [2*n] = expression to specify indesx to skip like :
    Every X indexes, skip indexes N[...] == N,N,.../X == (%d+,*)+/%d+
    ex: skip 2/3/4th index every 4 index == "2,3,4/4"
"""
user.multiply = """
  (float) multiplier to apply on all value
"""
user.add = """
  (float) offset to apply on all the values
"""
user.op_order = """
   (string)(optional) use "add" if the offset need to be applied first
   or "multiply" for the inverse
"""
]]
local luakat = require("luakat")
local luabased = require("luabased")
local logging = require("lllogger")

local logger = logging.getLogger(...)

local function err(...)
  --[[
  Raise an error for this module.
  Concat the given arguments to string and pass them as the error's message.
  ]]
  local arg = { ... }
  arg.insert("[attr_math]", 1)
  luabased.raising.errorc(unpack(arg))

end

local function getSkipTable(arguments)
  --[[
  Args:
    arguments(str): string formatted as [%d,]+%/%d+
  ]]

  -- if not specified
  if arguments == "" then
    return { ["tuple"] = 1, ["skip"] = {} }
  end

  if not arguments:match("[%d,]+%/%d+") then
    err("[getSkipTable] Argument not formatted properly: ", arguments)
  end

  local out = {}
  out.tuple = tonumber(arguments:sub(-1))
  arguments = arguments:sub(1, -3) -- strip the 2 last characters (ex:/3)
  out.skip = {}
  -- split at the ,
  for each in arguments:gmatch("([^,]+)") do

    if tonumber(each) > out.tuple then
      err(
          "[getSkipTable] Index <", each, "> to skip is bigger than \z
          the tuple size <", out.tuple, ">"
      )
    end

    out.skip[tonumber(each)] = true

  end

  return out

end

local function run()

  local order_add = "add"
  local order_mult = "multiply"

  local u_attr_list = luakat.attribute.getUserAttrValue("attributes")
  assert(u_attr_list ~= nil, "[attr_math][run] Missing <user.attributes>")

  local u_mult = luakat.attribute.getUserAttrValue("multiply")
  assert(u_mult ~= nil, "[attr_math][run] Missing <user.multiply>")
  u_mult = u_mult[1]

  local u_add = luakat.attribute.getUserAttrValue("add")
  assert(u_add ~= nil, "[attr_math][run] Missing <user.add>")
  u_add = u_add[1]

  local u_order = luakat.attribute.getUserAttrValue("op_order", { order_add })[1]

  local attr_skip
  local attr_path
  local attr_data
  local attr_type
  local new_value
  local new_value_smpls

  for iattr = 0, #u_attr_list / 2 - 1 do

    attr_path = u_attr_list[iattr * 2 + 1]  -- string
    attr_skip = getSkipTable(u_attr_list[iattr * 2 + 2]) -- table
    attr_data = luakat.attribute.getAttr(attr_path)  -- DataAttribute
    attr_type = luakat.attribute.getAttributeClass(attr_data)  -- DataAttribute

    -- check that the user specified tuple size seems valid
    new_value = attr_data:getNearestSample(0)
    if #new_value / attr_skip.tuple ~= math.floor(#new_value / attr_skip.tuple) then
      err(
          "[run] The skip tuple size specified <",
          attr_skip.tuple,
          ">, divided by the number of value <",
          #new_value,
          "> is not an integer."
      )
    end

    new_value_smpls = {}

    for smplindex = 0, attr_data:getNumberOfTimeSamples() - 1 do

      -- convert the smplindex to sampletime (shutterOpen/Close values)
      smplindex = attr_data:getSampleTime(smplindex)
      new_value = attr_data:getNearestSample(smplindex)

      for i = 0, #new_value / attr_skip.tuple - 1 do
        -- /!\ performances

        for ii = 1, attr_skip.tuple do

          -- if the index is not specified as skipable, do the math
          if not attr_skip.skip[ii] then

            if u_order == order_add then
              new_value[i * attr_skip.tuple + ii] = (new_value[i * attr_skip.tuple + ii] + u_add) * u_mult
            elseif u_order == order_mult then
              new_value[i * attr_skip.tuple + ii] = new_value[i * attr_skip.tuple + ii] * u_mult + u_add
            else
              err("[run] user argument <order> value <", u_order, "> is not supported.")
            end
            -- end if index not skipped
          end
          -- end tuple loop
        end
        -- end #new_value loop
      end

      new_value_smpls[smplindex] = new_value

      -- end smplidnex loop
    end

    Interface.SetAttr(
        attr_path,
        attr_type(new_value_smpls, attr_data:getTupleSize())
    )
    -- end attributes iterations
  end

end

return run