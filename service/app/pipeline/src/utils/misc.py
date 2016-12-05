def apply_over(D, function, fun_args):
  for P in D:
    for T in P:
      T = function(T, fun_args)
  return D