
import islpy as isl

class Counter(object):

    def __init__(self, fmt):
        self.fmt = fmt
        self.next_id = 0

    def next(self):
        name = self.fmt % (self.next_id,)
        self.next_id += 1
        return name

    def __iter__(self):
        for i in xrange(self.next_id):
            yield self.fmt % (i,)

stmt_counter = Counter("S%d")

def rename_bm(bm, name):
    return bm.set_tuple_name(isl.dim_type.in_, name)

def rename_expr(expr, name):
    if expr[0] == 'var':
        return ('var', rename_bm(expr[1],name))
    elif expr[0] == 'const':
        return expr
    elif expr[0] == 'call':
        return (expr[0],expr[1], tuple(rename_expr(e,name) for e in expr[2]))
    else:
        raise NotImplementedError

def rename_statement(create_op):  
  def wrapper(*args, **kwargs):
    op = create_op(*args, **kwargs)
    name = stmt_counter.next()
    return (
        rename_bm(op[0], name),
        rename_expr(op[1], name))
  return wrapper

