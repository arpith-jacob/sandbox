
import islpy as isl
import arrays
import operations
import schedule
import codegen
import emitter

if __name__ == "__main__":
  isl_context = isl.Context.alloc()

  # Inputs: A[M,N], B[M,N]
  # Output: Z[M,N]
  # Operation: Z = A + B

  A_shape = [100, 200]
  B_shape = [100, 200]
  Z_shape = [100, 200]

  A = arrays.isl_array(isl_context, "A", A_shape)
  B = arrays.isl_array(isl_context, "B", B_shape)
  Z = arrays.isl_array(isl_context, "Z", Z_shape)

  statements = []
  stmt = operations.add(isl_context, ("Z", Z_shape),
                        ("A", A_shape), ("B", B_shape))
  print stmt
  statements.append(stmt)

  schedule = schedule.build_schedule(isl_context, statements)

  ast = codegen.codegen(isl_context, schedule, statements)

  print emitter.emit_source(statements, ast)

