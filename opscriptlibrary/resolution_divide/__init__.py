from Katana import NodegraphAPI

from katananodling.entities import OpScriptCustomNode


def buildUserParams(userparam, as_expression=False):
    # type: (NodegraphAPI.Parameter, bool) -> None

    p = userparam.createChildNumber("divider", 1)
    p.setExpression("=^/user.divider", as_expression)
    hint = {
        "help": (
            "<p>Amount to divide the current resolution by.<br>"
            "You can also specify it using a GSV named "
            "<code>resolution_divider</code>.</p>"
        )
    }
    p.setHintString(repr(hint))

    return


class ResolutionDivideNode(OpScriptCustomNode):

    name = "ResolutionDivide"
    version = (1, 0, 0)
    color = None
    description = "Divide the current render resolution by the given amount."
    author = "<Liam Collod pyco.liam.business@gmail.com>"

    def _buildOpScript(self):

        script = 'local script = require("{path}")\nscript()'
        script = script.format(path=self.getLuaModuleName())

        node = self.getDefaultOpScriptNode()

        node.getParameter("location").setValue("/root", 0)
        node.getParameter("applyWhere").setValue("at specific location", 0)
        node.getParameter("script.lua").setValue(script, 0)

        buildUserParams(node.getParameter("user"), as_expression=True)
        return

    def _build(self):

        buildUserParams(self.user_param, as_expression=False)
        self._buildOpScript()
        self.moveAboutParamToBottom()
        return
