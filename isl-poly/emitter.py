
import islpy as isl

INT_FUN_TYPE = {
    '<': 'infix',
    '>': 'infix',
    '<=': 'infix',
    '>=': 'infix',
    '==': 'infix',
    '!=': 'infix',
    '&&': 'infix',
    '||': 'infix',
    '+': 'infix',
    '-': 'infix',
    '*': 'infix',
    '/': 'infix',
    '_': "prefix",
    '%': 'infix',
    'max': 'fun2',
    'min': 'fun2',
    'select': 'select'
}

INT_FUN_FMT = {
    '_': '-',
}

def format_int_call(fun, args):
    t = INT_FUN_TYPE[fun]

    if t == 'infix':
        return "({} {} {})".format(format_int_expr(args[0]), INT_FUN_FMT.get(fun,fun), format_int_expr(args[1]))
    elif t == 'prefix':
        return "({} {})".format(INT_FUN_FMT.get(fun,fun), format_int_expr(args[0]))
    elif t == 'fun1':
        return "({}({}))".format(INT_FUN_FMT.get(fun,fun), format_int_expr(args[0]))
    elif t == 'fun2':
        return "({}({},{}))".format(INT_FUN_FMT.get(fun,fun), format_int_expr(args[0]), format_int_expr(args[1]))
    elif t == 'select':
        return "(({})?({}):({}))".format(format_int_expr(args[0]), format_int_expr(args[1]), format_int_expr(args[2]))

    raise NotImplementedError

def format_int_expr(ast):
    if ast[0] == 'var':
        return '{}'.format(ast[1])
    elif ast[0] == 'int':
        return "%d"%(ast[1],)
    elif ast[0] == 'call':
        return format_int_call(ast[1], ast[2])
    raise NotImplementedError

def format_element(v, indices):
    return "%s%s"%(v, "".join("[%s]"%(format_int_expr(i),) for i in indices))

FUN_TYPE = {
    '+': 'infix',
    '-': 'infix',
    '*': 'infix',
    '/': 'infix',
    '_': 'prefix',
    '**': 'fun2',
    'exp': 'fun1',
    'log': 'fun1',
    '==': 'infix',
    'max': 'fun2',
    'min': 'fun2',
}

FUN_FMT = {
    '_': '-',
    '**': 'powf',
    'exp': 'expf',
    'log': 'logf',
    'max': 'fmax',
    'min': 'fmin',
}

def format_call(table, fun, args):
    t = FUN_TYPE[fun]
    if t == 'infix':
        return "({} {} {})".format(format_ast(table, args[0]), FUN_FMT.get(fun,fun), format_ast(table, args[1]))
    elif t == 'prefix':
        return "({} {})".format(FUN_FMT.get(fun,fun), format_ast(table, args[0]))
    elif t == 'fun1':
        return "({}({}))".format(FUN_FMT.get(fun, fun), format_ast(table, args[0]))
    elif t == 'fun2':
        return "({}({},{}))".format(FUN_FMT.get(fun, fun), format_ast(table, args[0]), format_ast(table, args[1]))

    raise NotImplementedError

def format_ast(table, ast, format_kernel=None):
    if isinstance(ast, list):
        return "".join(format_ast(table, node, format_kernel) for node in ast)
    if ast[0] == 'for':
        return "for(int {v} = {init}; {cond}; {v} = {v} + {inc}){{\n{body}}}\n".format(
            v = format_int_expr(ast[1]),
            init = format_int_expr(ast[2]),
            inc = format_int_expr(ast[3]),
            cond = format_int_expr(ast[4]),
            body = format_ast(table, ast[5], format_kernel))
    elif ast[0] == 'if':
        return "if({cond}){{\n{then}}}\n".format(
            cond = format_int_expr(ast[1]),
            then = format_ast(table, ast[2], format_kernel))
    elif ast[0] == 'ifelse':
        return "if({cond}){{\n{then}}}\nelse{{\n{else_}}}".format(
            cond = format_int_expr(ast[1]),
            then = format_ast(table, ast[2], format_kernel),
            else_ = format_ast(table, ast[3], format_kernel))
    elif ast[0] == 'assign':
        assert ast[1][0] == 'element'
        if len(ast[1][2]) == 0:
            assert len(ast[1][2]) == 0
            return "{} = {};\n".format(
                ast[1][1],
                format_ast(table, ast[2], format_kernel))
        return "{} = {};\n".format(
            format_element(ast[1][1], ast[1][2]),
            format_ast(table, ast[2], format_kernel))
    elif ast[0] == 'call':
        return format_call(table, ast[1], ast[2])
    elif ast[0] == 'element':
        if len(ast[2]) == 0:
            assert len(ast[2]) == 0
            return "({}[0])".format(ast[1])
        else:
            return "({})".format(format_element(ast[1], ast[2]))
    elif ast[0] == 'const':
        return "%f"%(ast[1],)
    elif ast[0] == 'var':
        return ast[1]
    else:
        raise NotImplementedError

def emit_source(statements, ast):
  return format_ast(statements, ast)

