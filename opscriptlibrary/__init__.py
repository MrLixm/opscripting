"""
The goal is to have every BaseCustomNode subclasses available in this namespace.
So we can iterate over this package to retrieve all the nodes to create.

This mean you can organise this package as you wish as long as the subclass that you want
to register is imported here.

All objects imported here that are not subclasses of BaseCustomNode OR whose name starts
with a "_" will be ignored.
"""
from .attr_math import AttrMath
from .attr_type_swap import AttrTypeSwap
from .light_viewer_annotate import LightViewerAnnotate
from .point_width import PointWidth
from .resolution_divide import ResolutionDivide
from .xform2P import Xform2P
