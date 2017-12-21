
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

  A = arrays.isl_array(isl_context, "A", A_shape)
  B = arrays.isl_array(isl_context, "B", B_shape)
  C = arrays.isl_array(isl_context, "C", C_shape)
  Z = arrays.isl_array(isl_context, "Z", Z_shape)

  statements = {}
  stmt = operations.add(isl_context, ("C", C_shape),
                        ("A", A_shape), ("B", B_shape))
  name = statement.get_name(stmt)
  statements[name] = stmt
  stmt = operations.add(isl_context, ("Z", Z_shape),
                        ("C", C_shape), ("B", B_shape))
  name = statement.get_name(stmt)
  statements[name] = stmt

  for stmt in statements.values():
    print stmt

  schedule = schedule.build_schedule(isl_context, statements)
  print schedule

  ast = codegen.codegen(isl_context, schedule, statements)

  print emitter.emit_source(statements, ast)

