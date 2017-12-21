
import islpy as isl
import arrays

def add(ctx, Z, A, B):
  Z_out = arrays.get_default_space(ctx, Z[0])
  A_in = arrays.get_default_space(ctx, A[0])
  B_in = arrays.get_default_space(ctx, B[0])

  assert Z[1] == A[1]
  assert Z[1] == B[1]

  for s in Z[1]:
    Z_out = arrays.add_dimension(ctx, Z_out, s)
    A_in = arrays.add_dimension(ctx, A_in, s)
    B_in = arrays.add_dimension(ctx, B_in, s)

  return (Z_out, ('call', '+', (('var', A_in),
                                ('var', B_in))
                 )
         )

