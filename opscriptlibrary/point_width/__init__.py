from Katana import NodegraphAPI

from katananodling.entities import OpScriptCustomNode


def buildUserParams(userparam, as_expression=False):
    # type: (NodegraphAPI.Parameter, bool) -> None

    p = userparam.createChildNumber("point_scale", 1)
    p.setExpression("=^/user.point_scale", as_expression)
    hint = {
        "slider": True,
        "help": "multiplier of the point's scale in the viewer",
        "slidermax": 50,
    }
    p.setHintString(repr(hint))
    return


class PointWidth(OpScriptCustomNode):

    name = "PointWidth"
    version = (1, 0, 0)
    color = None
    description = "Change scale of the geometry points."
    author = "<Liam Collod pyco.liam.business@gmail.com>"

    def _buildOpScript(self):

        script = 'local script = require("{path}")\nscript()'
        script = script.format(path=self.getLuaModuleName())

        node = self.getDefaultOpScriptNode()

        node.getParameter("CEL").setExpression("=^/user.CEL", True)
        node.getParameter("applyWhere").setValue("at locations matching CEL", 0)
        node.getParameter("script.lua").setValue(script, 0)

        buildUserParams(node.getParameter("user"), as_expression=True)
        return

    def _build(self):

        p = self.user_param.createChildString("CEL", "")
        hint = {"widget": "cel"}
        p.setHintString(repr(hint))

        buildUserParams(self.user_param, as_expression=False)
        self._buildOpScript()
        self.moveAboutParamToBottom()
        return
