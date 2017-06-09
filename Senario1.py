 
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 17:45:48 2017

@author: Hossein Pourghaemi
"""

from graph_tool.all import *
import numpy as np
np.random.seed(1)


g = Graph()
g.set_directed(False)

lambdas= [10,5,10,15,10,25,5,10,25,15,5,15,25,10,10,15,10,25]

g = load_graph("my_graph.xml.gz")

name = g.vp["name"]
weight = g.ep["weight"]
graph_draw(g, vertex_text=name, vertex_font_size=12, vertex_shape="double_circle",vertex_fill_color="#729fcf", vertex_pen_width=3,
              edge_pen_width=weight, output="search_example.pdf")

bins =[0,3,5,14,12,10,8,17,19,21,23,32,30,28,26,35,37,39,41,0]
shortest_lenght=0
for i in range(len(bins)-1):
    dist = graph_tool.topology.shortest_distance(g, source=g.vertex(bins[i]), target=g.vertex(bins[i+1]), weights=weight,
                                      negative_weights=False, max_dist=None, directed=None,
                                      dense=False, dist_map=None, pred_map=False)
    shortest_lenght += dist

print "Shortest cycle path with visiting all bins is :%d" %shortest_lenght

num_of_bins =18
hours = 24
total_cost = 0
for i in range(hours):
    poiss_rands= []
    for j in range(num_of_bins):          
        s = np.random.poisson(lambdas[j])
        poiss_rands.append(s)
    poiss_rands =np.asarray(poiss_rands)
    overflow = np.where(poiss_rands[:]>50)[0]
    num_of_overflow, = overflow.shape
    hour = i+1
    if num_of_overflow>0:
        print "Some overflows occurred at %d'th hour!!" %hour
    else : 
        print "their is no overflow at %d'th hour!!" %hour
        
    cost = shortest_lenght * 3.5 + num_of_overflow*20
    total_cost +=cost
print 'Total coust of waste collectin of city for 24 hours is: %f' %total_cost