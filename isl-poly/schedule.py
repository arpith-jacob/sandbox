
import islpy as isl

def get_assign_map(ctx, statements):
  maps = [s[0] for s in statements]
  union_map = isl.UnionMap("{}", ctx)
  for m in maps:
    union_map = union_map.union(isl.UnionMap.from_map(m))
  return union_map

def get_use_map(ctx, statements):
  maps = [[s[1][2][0][1], s[1][2][1][1]] for s in statements]
  maps = sum(maps, [])
  union_map = isl.UnionMap("{}", ctx)
  for m in maps:
    union_map = union_map.union(isl.UnionMap.from_map(m))
  return union_map

def get_schedule_constraints(ctx, statements):
  def_map = get_assign_map(ctx, statements)
  use_map = get_use_map(ctx, statements)

  domain = def_map.domain()
  validity = def_map.apply_range(use_map.reverse())

  constraints = isl.ScheduleConstraints.on_domain(domain)
  constraints = constraints.set_validity(validity)

  return constraints

def build_schedule(ctx, statements):
  ctx.set_ast_build_detect_min_max(1)
  ctx.set_schedule_maximize_band_depth(1)
  ctx.set_schedule_maximize_coincidence(1)
  ctx.set_schedule_whole_component(0)
  ctx.set_schedule_separate_components(1)
  ctx.set_schedule_treat_coalescing(1)
  ctx.set_schedule_outer_coincidence(1)

  constraints = get_schedule_constraints(ctx, statements)
  schedule = constraints.compute_schedule()
  print
  print 'SCHEDULE:'
  schedule.dump()
  print

  return schedule
