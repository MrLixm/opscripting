import os.path

from Katana import NodegraphAPI

from katananodling.entities import OpScriptTool


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


class PointWidth(OpScriptTool):

    name = "PointWidth"
    version = (1, 0, 0)
    color = None
    description = "Change scale of the geometry points."
    author = "<Liam Collod pyco.liam.business@gmail.com>"
    maintainers = []

    luamodule = "{}.{}".format(
        os.path.split(os.path.dirname(__file__))[-1],
        os.path.splitext(os.path.basename(__file__))[0],
    )

    def _buildOpScript(self):

        script = 'local script = require("{path}")\nscript()'
        script = script.format(path=self.luamodule)

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
