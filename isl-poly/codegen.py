
import islpy as isl

OP = {
    'le': '<=',
    'ge': '>=',
    'lt': '<',
    'gt': '>',
    'max': 'max',
    'min': 'min',
    'sub': '-',
    'minus': '_',
    'add': '+',
    'eq': '==',
    'and_': '&&',
    'or_': '||',
    'mul': '*',
    'div': '/',
    'pdiv_q': '/',
    'pdiv_r': '%',
    'zdiv_r': '%',
    'select': 'select'
}

def convert_expr(expr):
    if expr.get_type() == isl.ast_expr_type.id:
        return ('var', expr.get_id().get_name())
    elif expr.get_type() == isl.ast_expr_type.int:
        return ('int', expr.get_val().to_python())
    elif expr.get_type() == isl.ast_expr_type.op:
        return ('call',
                OP[isl.ast_op_type.find_value(expr.get_op_type())],
                tuple(convert_expr(expr.get_op_arg(i)) for i in xrange(expr.get_op_n_arg())))
    else:
        raise NotImplementedError

def to_list(l):
    r = []
    l.foreach(lambda e: r.append(e))
    return r

def build_ast(stmts, node):
    if node.get_type() == isl.ast_node_type.block:
        return [build_ast(stmts, c) for c in to_list(node.block_get_children())]
    elif node.get_type() == isl.ast_node_type.for_:
        return ("for",
            convert_expr(node.for_get_iterator()),
            convert_expr(node.for_get_init()),
            convert_expr(node.for_get_inc()),
            convert_expr(node.for_get_cond()),
            build_ast(stmts, node.for_get_body()))
    elif node.get_type() == isl.ast_node_type.if_:
        if node.if_has_else():
            return (
                "ifelse",
                convert_expr(node.if_get_cond()),
                build_ast(stmts, node.if_get_then()),
                build_ast(stmts, node.if_get_else()))
        else:
            return (
                "if",
                convert_expr(node.if_get_cond()),
                build_ast(stmts, node.if_get_then()))
    elif node.get_type() == isl.ast_node_type.user:
        name = node.user_get_expr().get_id().get_name()
        return stmts[name]
    elif node.get_type() == isl.ast_node_type.mark:
        return (
            "mark",
            node.mark_get_id().get_name(),
            build_ast(stmts, node.mark_get_node())
        )
    else:
        raise NotImplementedError

def expr_to_element(expr):
    n = expr.get_op_n_arg()
    return ('element', expr.get_op_arg(0).get_id().get_name() , tuple(convert_expr(expr.get_op_arg(i)) for i in xrange(1,n)))

def transform_var(var, iterator_map, build, groups=None):
    pma = isl.PwMultiAff.from_map(isl.Map.from_union_map(iterator_map.apply_range(var)))
    return expr_to_element(build.access_from_pw_multi_aff(pma))

def transform_expr(expr, iterator_map, build, groups=None):
    if expr[0] == 'var':
        return transform_var(expr[1], iterator_map, build, groups)
    elif expr[0] == 'const':
        return expr
    elif expr[0] == 'call':
        return ('call', expr[1], tuple(transform_expr(e, iterator_map, build, groups) for e in expr[2]))
    else:
        raise NotImplementedError

def transform_stmt(stmt, iterator_map, build, groups=None):
    name = stmt[0].get_tuple_name(isl.dim_type.in_)

    return ("assign", transform_var(stmt[0], iterator_map, build, groups),
            transform_expr(stmt[1], iterator_map, build, groups))

def codegen(ctx, schedule, stmts):
  codegen_stmts = {}
  def at_each_domain(node, build):
     if node.get_type() != isl.ast_node_type.user:
       return node

     schedule = build.get_schedule()
     iterator_map = schedule.reverse()

     expr = node.user_get_expr()
     expr = expr.get_op_arg(0)
     name = expr.get_id().get_name()

     stmt = stmts[name]
     codegen_stmt = transform_stmt(stmt, iterator_map, build)
     codegen_stmts[name] = codegen_stmt

     return isl.AstNode.alloc_user(isl.AstExpr.from_id(isl.Id.alloc(ctx, name, None)))

  build = isl.AstBuild.alloc(ctx)
  build, _ = build.set_at_each_domain(at_each_domain)
  node = build.node_from_schedule(schedule)

  return build_ast(codegen_stmts, node)

