import os.path

from Katana import NodegraphAPI

from customtooling.nodebase import OpScriptTool


def buildUserParams(userparam, as_expression=False):
    # type: (NodegraphAPI.Parameter, bool) -> None

    p = userparam.createChildStringArray("attributes", 2)
    p.setExpression("=^/user.attributes", as_expression)
    p.setTupleSize(2)
    hint = {
        "resize": True,
        "tupleSize": 2,
        "help": (
            "<p>n Rows of 2 columns:<br/>"
            "-[1 * n] = path of the attribute relative to the location<br/>"
            "-[2 * n] = new DataAttribute type to use, ex: StringAttribute<br/>"
            "<br/>"
            "DataAttributes available are:<br/>"
            "- IntAttribute<br/>-FloatAttribute<br/>-DoubleAttribute<br/>-StringAttribute"
        ),
    }
    p.setHintString(repr(hint))

    p = userparam.createChildString("method", "array")
    p.setExpression("=^/user.method", as_expression)
    hint = {
        "widget": "popup",
        "options": ["table", "array"],
        "help": (
            "<p>which method to use for querying attributes:<br/>"
            "- <code>table</code>: max of 2^27 (134 million) values per attribute<br/>"
            "- <code>array</code> <em>(default)</em>: a bit slower, no size limit</p>"
        ),
    }
    p.setHintString(repr(hint))

    return


class AttrTypeSwap(OpScriptTool):

    name = "AttrTypeSwap"
    version = (1, 0, 2)
    color = None
    description = (
        "Change the type of an attribute. ex: FloatAttribute -> DoubleAttribute"
    )
    author = "<Liam Collod pyco.liam.business@gmail.com>"
    maintainers = []

    luamodule = os.path.splitext(os.path.basename(__file__))[0]

    def _buildOpScript(self):

        script = """
local script = require("opscriptlibrary.{module}")
script()"""
        script = script.format(module=self.luamodule)

        node = self.getDefaultOpScriptNode()

        node.getParameter("CEL").setExpression("=^/user.CEL", True)
        node.getParameter("applyWhere").setValue("at locations matching CEL", 0)
        node.getParameter("script.lua").setValue(script, 0)

        buildUserParams(node.getParameter("user"), as_expression=True)
        return

    def _build(self):
        # type: () -> NodegraphAPI.Node

        userparam = self.user_param
        p = userparam.createChildString("CEL", "")
        hint = {"widget": "cel"}
        p.setHintString(repr(hint))
        buildUserParams(userparam, as_expression=False)

        self._buildOpScript()

        self.moveAboutParamToBottom()
        return


NODE = AttrTypeSwap
