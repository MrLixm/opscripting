import os.path

from katananodling.entities import OpScriptCustomNode


class Xform2P(OpScriptCustomNode):

    name = "Xform2P"
    version = (1, 0, 0)
    color = None
    description = "Merge xform transformations to the geometry.point.P attribute."
    author = "<Liam Collod pyco.liam.business@gmail.com>"

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
        return

    def _build(self):

        userparam = self.getParameter("user")
        p = userparam.createChildString("CEL", "")
        hint = {"widget": "cel"}
        p.setHintString(repr(hint))

        self._buildOpScript()
        self.moveAboutParamToBottom()
        return
