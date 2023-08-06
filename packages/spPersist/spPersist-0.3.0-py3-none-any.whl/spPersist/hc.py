from . import ph

def homological_classification(X, ptype:str):
  '''
  homological_classification takes a point cloud X
  and ptype indicating the persistence computed,
  and return a dictionary of homologies of X where
  the keys indicate connected components or n-dimensional
  holes and the values indicate the number of connected
  components or the number of holes of a given dimension.
  '''

  hc = {}
  st = ph.compute_simplicial_complex(X,ptype=ptype)
  bn = st.betti_numbers()
  for i in range(len(bn)):
    if i == 0:
      hc['connected components'] = bn[i]
    else:
      hc[str(i)+'-dimensional holes'] = bn[i]

  return hc