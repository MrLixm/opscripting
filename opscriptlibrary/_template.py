import os.path

from Katana import NodegraphAPI

from katananodling.entities import OpScriptTool


def buildUserParams(userparam, as_expression=False):
    # type: (NodegraphAPI.Parameter, bool) -> None
    pass


class _Template(OpScriptTool):

    name = "_Template"
    version = (0, 1, 0)
    color = None
    description = "What the tool does in a few words."
    author = "<FirstName Name email@provider.com>"
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

        userparam = self.user_param
        p = userparam.createChildString("CEL", "")
        hint = {"widget": "cel"}
        p.setHintString(repr(hint))

        buildUserParams(userparam, as_expression=False)
        self._buildOpScript()
        self.moveAboutParamToBottom()

        return
