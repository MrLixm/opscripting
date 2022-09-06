"""
The goal is to have every BaseCustomNode subclasses available in this namespace.
So we can iterate over this package to retrieve all the nodes to create.

This mean you can organise this package as you wish as long as the subclass that you want
to register is imported here.

All objects imported here that are not subclasses of BaseCustomNode OR whose name starts
with a "_" will be ignored.
"""
from .attr_math import AttrMathNode
from .attr_type_swap import AttrTypeSwapNode
from .light_viewer_annotate import LightViewerAnnotateNode
from .point_width import PointWidthNode
from .resolution_divide import ResolutionDivideNode
from .xform2P import Xform2PNode
