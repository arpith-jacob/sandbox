
import islpy as isl
import arrays
from statement import rename_statement

@rename_statement
def add(ctx, Z, A, B):
  assert Z[1] == A[1]
  assert Z[1] == B[1]

  Z_out = arrays.poly_array(ctx, Z[0], Z[1])
  A_in = arrays.poly_array(ctx, A[0], A[1])
  B_in = arrays.poly_array(ctx, B[0], B[1])

  Z_out = arrays.add_access(ctx, Z_out, Z[2])
  A_in = arrays.add_access(ctx, A_in, A[2])
  B_in = arrays.add_access(ctx, B_in, B[2])

  return (Z_out, ('call', '+', (('var', A_in),
                                ('var', B_in))
                 )
         )

