# AttrMath

Apply basic math operation on attributes values.

# Features

- math operations :
  - multiplication
  - addition
  - changes operation order
- skip indexes
- motion blur support

## Use

First set the scene-graph location where you want to modify some of its attributes
in the `location` parameter at top.

You can then modify the `user.attributes` parameter to add attribute to modify.
Each row corresponds to an attribute to modify where :

- column [1*n] = path of the attribute relative to the location
- column [2*n] = expression to specify indesx to skip like :
  Every X indexes, skip indexes N[...] == `N,N,.../X` == `(%d+,*)+/%d+`
  ex: skip 2/3/4th index every 4 index == `2,3,4/4` (so process only 1/4)

