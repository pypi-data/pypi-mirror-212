from DTM_filtrations import *
import persistence_statistics as ps

import gudhi
import numpy as np
import matplotlib.pyplot as plt

def compute_simplicial_complex(X,ptype: str,max_dimension=2,p=1,m=0.1,is_plot=False):
  '''
  compute_persistence takes a point cloud X and a ptype indicating whether the
  type of simplicial complex computed is Rips complex, Alpha complex or DTM filtrations, 
  and returns the computed simplicial complex of X. If is_plot is true, it also plots
  its persistence diagram.

  The extra parameter max_dimension can be specified for Rips complex and DTM
  filtrations; and for the case of DTM filtrations, the additional parameters 
  p and m can be specified.
  '''

  # create a complex
  if ptype == 'Rips':
    st = gudhi.RipsComplex(points=X).create_simplex_tree(max_dimension)
  elif ptype == 'Alpha':
    st = gudhi.AlphaComplex(points=X).create_simplex_tree()
  elif ptype == 'DTM':
    st = DTMFiltration(X, m, p, max_dimension)
  else:
    raise ValueError('ptype is not one of Rips, Alpha or DTM.')

  # compute the persistence
  diagram = st.persistence()                                       

  # plot the persistence diagram
  if is_plot:
    gudhi.plot_persistence_diagram(diagram)
    if ptype == 'Rips':                    
      title = 'Persistence diagram of the Rips complex'
    elif ptype == 'Alpha':
      title = 'Persistence diagram of the Alpha complex'
    elif ptype == 'DTM':
      title = 'Persistence diagram of the DTM-filtration with parameter p ='+str(p)
    else:
      raise ValueError('ptype is not one of Rips, Alpha or DTM.')
    plt.title(title);

  return st


def bottleneck_distance(X, ptype1, ptype2, dim):
  '''
  bottleneck_distance takes a point cloud X and computes
  the bottleneck distance between persistence diagram of
  type ptype1 and the one of ptype2 in dimension dim.
  '''

  st1 = compute_simplicial_complex(X, ptype=ptype1)
  st2 = compute_simplicial_complex(X, ptype=ptype2)
  
  diag1 = st1.persistence_intervals_in_dimension(dim)
  diag2 = st2.persistence_intervals_in_dimension(dim)

  distance = gudhi.bottleneck_distance(diag1, diag2)

  message = "Bottleneck distance approximation = " + '%.2f' % gudhi.bottleneck_distance(diag1, diag2, 0.1)
  print(message)

  message = "Bottleneck distance value = " + '%.2f' % distance
  print(message)

  return distance


def plot_confidence_region(X, ptype: str, level=0.90):
  '''
  confidence_region takes a point cloud X and ptype
  indicating either a Rips complex or a Square-root
  Alpha complex used for computing the persistence,
  and plot the persistence diagram of X with confidence 
  region as red band. 

  The topological features in the region is considered
  'topological noise' and the features above the red 
  band is considered 'topological signal'.

  The desired confidence level can be specified using
  the parameter level.
  '''

  hatc = ps.hausd_interval(data=X, level=level)
  st = compute_simplicial_complex(X,ptype)
  if ptype == 'Rips':
    diagram = st.persistence()
  elif ptype == 'Alpha':
    st_list = st.get_filtration()
    for splx in st_list:
      st.assign_filtration(splx[0],filtration= np.sqrt(splx[1])) 
    diagram = st.persistence()
  else:
    raise ValueError('ptype is not either Rips or Alpha.')
  
  gudhi.plot_persistence_diagram(diagram,band=2*hatc);