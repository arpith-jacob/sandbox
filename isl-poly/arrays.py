
import islpy as isl

def isl_array(ctx, name, shape):
  space = isl.Space.set_alloc(ctx, 0, len(shape))
  space = space.set_tuple_name(isl.dim_type.set, name)

  basic_set = isl.BasicSet.nat_universe(space)

  for d, s in enumerate(shape):
    constraint = isl.Constraint.alloc_inequality(space)
    constraint = constraint.set_coefficient_val(isl.dim_type.set, \
                   d, isl.Val.int_from_si(ctx, -1))
    constraint = constraint.set_constant_val(isl.Val.int_from_si(ctx, s-1))

    basic_set = basic_set.add_constraint(constraint)

  return isl.Set.from_basic_set(basic_set)

def get_default_space(ctx, name):
  space = isl.Space.alloc(ctx, 0, 0, 0)
  space = space.set_tuple_name(isl.dim_type.in_, "S")
  space = space.set_tuple_name(isl.dim_type.out, name)
  return isl.Map.nat_universe(space)

def increase_dimension(v, dim_type):
  name = v.get_tuple_name(dim_type)
  return v.add_dims(dim_type, 1).set_tuple_name(dim_type, name)
  
def add_dimension(ctx, v, bound):
  n_in_ = v.dim(isl.dim_type.in_)
  n_out = v.dim(isl.dim_type.out)

  # Handle input dimension
  v = increase_dimension(v, isl.dim_type.in_)

  # i <= bound
  constraint = isl.Constraint.alloc_inequality(v.get_space())
  constraint = constraint.set_coefficient_val(isl.dim_type.in_,
                 n_in_, isl.Val.int_from_si(ctx, -1))
  constraint = constraint.set_constant_val(isl.Val.int_from_si(ctx, bound-1))
  v = v.add_constraint(constraint)

  # i >= 0
  constraint = isl.Constraint.alloc_inequality(v.get_space())
  constraint = constraint.set_coefficient_val(isl.dim_type.in_,
                 n_in_, isl.Val.int_from_si(ctx, 1))
  v = v.add_constraint(constraint)

  # Handle output dimension
  v = increase_dimension(v, isl.dim_type.out)

  constraint = isl.Constraint.alloc_equality(v.get_space())
  constraint = constraint.set_coefficient_val(isl.dim_type.in_, n_in_,
                 isl.Val.int_from_si(ctx, -1))
  constraint = constraint.set_coefficient_val(isl.dim_type.out, n_out,
                 isl.Val.int_from_si(ctx, 1))
  v = v.add_constraint(constraint)

  return v

