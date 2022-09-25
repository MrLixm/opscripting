--[[
Add a geometry.point.width attribute to control the viewer's size of the points
or scale the existing one.

[OpScript ]
user.point_scale = "(float)(1): multiplier of the points scale in the viewer"
parameters.location = "pointcloud scene graph location"
parameters.applyWhere = "at specific location"
]]
local _M_ = {}

local luakat =  require("luakat")
local logging = require("lllogger")

local logger = logging.getLogger(...)


function _M_.run()

  -- get OpArg
  --- @type number
  local point_scale = luakat.attribute.getUserAttrValue("point_scale", { 1.0 })[1]

  local points_width = Interface.GetAttr("geometry.point.width")
  if points_width then
    points_width = points_width:getNearestSample(0)
  end
  local points = Interface.GetAttr("geometry.point.P"):getNearestSample(0)

  local point_scaled = {}
  for i = 1, #points do
    if points_width then
      point_scaled[i] = points_width[i] * point_scale
    else
      point_scaled[i] = point_scale
    end
  end

  Interface.SetAttr("geometry.point.width", FloatAttribute(point_scaled, 3))
  return

end

return _M_