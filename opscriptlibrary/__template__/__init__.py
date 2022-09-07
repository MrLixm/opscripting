from Katana import NodegraphAPI

from katananodling.entities import OpScriptCustomNode


def buildUserParams(userparam, as_expression=False):
    # type: (NodegraphAPI.Parameter, bool) -> None
    """
    Allow to create the same paramater on the OpScript node and on its parent node.
    The difference being that will set `as_expression=True` when called on the OpScript
    node so the value is retrived from the parent.

    You can choose to not use this function and delete it.
    """
    pass


class _TemplateNode(OpScriptCustomNode):

    name = "_Template"
    version = (0, 1, 0)
    color = None
    description = "What the node does in a few words."
    author = "<FirstName Name email@provider.com>"

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

        userparam = self.user_param
        p = userparam.createChildString("CEL", "")
        hint = {"widget": "cel"}
        p.setHintString(repr(hint))

        buildUserParams(userparam, as_expression=False)
        self._buildOpScript()
        self.moveAboutParamToBottom()

        return

    def upgrade(self):
        # optional
        pass
