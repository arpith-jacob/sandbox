
import islpy as isl
import arrays
import operations
import schedule
import codegen
import emitter
import statement

if __name__ == "__main__":
  isl_context = isl.Context.alloc()

  # Inputs: A[M,N], B[M,N]
  # Output: Z[M,N]
  # Operation: Z = A + B

  A_shape = [100, 200]
  B_shape = [100, 200]
  C_shape = [100, 200]
  Z_shape = [100, 200]

#  A = arrays.isl_array(isl_context, "A", A_shape)
#  B = arrays.isl_array(isl_context, "B", B_shape)
#  C = arrays.isl_array(isl_context, "C", C_shape)
#  Z = arrays.isl_array(isl_context, "Z", Z_shape)

  statements = {}
  stmt = operations.add(isl_context, ("C", C_shape, [0, 0]),
                        ("A", A_shape, [0, 1]), ("B", B_shape, [0, 0]))
  name = statement.get_name(stmt)
  statements[name] = stmt
  stmt = operations.add(isl_context, ("Z", Z_shape, [0, 0]),
                        ("C", C_shape, [0, 0]), ("B", B_shape, [0, 0]))
  name = statement.get_name(stmt)
  statements[name] = stmt

  for stmt in statements.values():
    print stmt

  schedule = schedule.build_schedule(isl_context, statements)
  print schedule

  ast = codegen.codegen(isl_context, schedule, statements)

  print
  print emitter.emit_source(statements, ast)

