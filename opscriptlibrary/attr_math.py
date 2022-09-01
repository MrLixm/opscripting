import os.path

from Katana import NodegraphAPI

from katananodling.entities import OpScriptTool


def buildUserParams(userparam, as_expression=False):
    # type: (NodegraphAPI.Parameter, bool) -> None

    p = userparam.createChildStringArray("attributes", 2)
    p.setExpression("=^/user.attributes", as_expression)
    p.setTupleSize(2)
    hint = {
        "resize": True,
        "tupleSize": 2,
        "help": (
            "<p>n Rows of 2 columns:<br/>- [1*n] = path of the attribute relative"
            " to the location<br/>- [2*n] = expression to specify indesx to skip like"
            " :<br/>&nbsp;&nbsp; Every X indexes, skip indexes N[...] == N,N,.../X =="
            ' (%d+,*)+/%d+<br/>&nbsp;&nbsp; ex: skip 2/4st index every 4 index == "2,4/4"</p>    '
        ),
    }
    p.setHintString(repr(hint))

    p = userparam.createChildNumber("multiply", 1.0)
    p.setExpression("=^/user.multiply", as_expression)
    hint = {
        "slider": True,
        "slidermax": 10,
    }
    p.setHintString(repr(hint))

    p = userparam.createChildNumber("add", 0.0)
    p.setExpression("=^/user.add", as_expression)
    hint = {
        "slider": True,
        "slidermax": 10,
        "slidermin": -10,
    }
    p.setHintString(repr(hint))

    p = userparam.createChildString("op_order", "add")
    p.setExpression("=^/user.op_order", as_expression)
    hint = {
        "widget": "popup",
        "options": ["add", "multiply"],
        "help": "Which operation should be applied first.",
    }
    p.setHintString(repr(hint))

    return


class AttrMath(OpScriptTool):

    name = "AttrMath"
    version = (1, 0, 2)
    color = None
    description = "Perform some basic math operation on attributes values."
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

        userparam = self.user_param
        p = userparam.createChildString("CEL", "")
        hint = {"widget": "cel"}
        p.setHintString(repr(hint))

        buildUserParams(userparam, as_expression=False)
        self._buildOpScript()
        self.moveAboutParamToBottom()
        return
