import os.path

from Katana import NodegraphAPI

from opscripttools.tooling import OpScriptTool


class Xform2P(OpScriptTool):

    name = "Xform2P"
    version = (1, 0, 0)
    color = None
    description = "Merge xform transformations to the geometry.point.P attribute."
    author = "<Liam Collod pyco.liam.business@gmail.com>"
    maintainers = []

    luamodule = os.path.splitext(os.path.basename(__file__))[0]

    def _buildOpScript(self):

        script = """
    local script = require("opscriptlibrary.{module}")
    script()"""
        script = script.format(module=self.luamodule)

        self.getParameter("CEL").setExpression("=^/user.CEL", True)
        self.getParameter("applyWhere").setValue("at locations matching CEL", 0)
        self.getParameter("script.lua").setValue(script, 0)
        return

    def __build(self):
        # type: () -> NodegraphAPI.Node

        userparam = self.getParameter("user")
        p = userparam.createChildString("CEL", "")
        hint = {"widget": "cel"}
        p.setHintString(repr(hint))

        self._buildOpScript()

        self.moveAboutParamToBottom()
        return


NODE = Xform2P
