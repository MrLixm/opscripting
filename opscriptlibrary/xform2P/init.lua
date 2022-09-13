--[[
Merge xform transformations to the `geometry.point.P` attribute.

! If your xform transform is interactive, think to disable
this ops before trying to move it in the viewer.

Supports motion blur.

[OpScript]
parameters.location = "location(s) to merge the xform attribute"
parameters.applyWhere = "at specific location OR at locations matching CEL"
]]
local _M_ = {}

local luakat = require("luakat")
local logging = require("lllogger")

local logger = logging.getLogger(...)

-- make a global local to improve perfs in big loops
local v3d = Imath.V3d

function _M_.run()

  logger:debug("[run] Started for location=", Interface.GetInputLocationPath())
  local stime = os.clock()

  local points_attr = luakat.attribute.getAttr("geometry.point.P")

  local xform = Interface.GetGlobalXFormGroup(Interface.GetInputLocationPath(), 0)
  local matrix_attr = XFormUtils.CalcTransformMatrixAtExistingTimes(xform)  -- DoubleAttribute

  local matrix
  local points
  local points_new = {}
  local pvector
  local pnew

  for smplindex = 0, matrix_attr:getNumberOfTimeSamples() - 1 do
    pnew = {}
    smplindex = matrix_attr:getSampleTime(smplindex)
    points = points_attr:getNearestSample(smplindex)
    matrix = Imath.M44d(matrix_attr:getNearestSample(smplindex))

    for i = 0, #points / 3 - 1 do

      pvector = v3d(
          points[i * 3 + 1],
          points[i * 3 + 2],
          points[i * 3 + 3]
      ) * matrix

      pnew[#pnew + 1] = pvector.x
      pnew[#pnew + 1] = pvector.y
      pnew[#pnew + 1] = pvector.z

    end

    points_new[smplindex] = pnew

  end

  Interface.SetAttr("geometry.point.P", FloatAttribute(points_new, 3))
  Interface.DeleteAttr("xform")

  logger:info(
      "[run] Finished in ",
      os.clock() - stime,
      "s for location",
      Interface.GetInputLocationPath()
  )
  return

end

return _M_