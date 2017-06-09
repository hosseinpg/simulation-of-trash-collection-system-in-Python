 
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 17:45:48 2017

@author: Hossein Pourghaemi
"""
from __future__ import division
from graph_tool.all import *
import numpy as np
np.random.seed(1)


g = Graph()
g.set_directed(False)

lambdas_per_hour= [10,5,10,15,10,25,5,10,25,15,5,15,25,10,10,15,10,25]


g = load_graph("my_graph.xml.gz")

name = g.vp["name"]
weight = g.ep["weight"]
graph_draw(g, vertex_text=name, vertex_font_size=12, vertex_shape="double_circle",vertex_fill_color="#729fcf", vertex_pen_width=3,
              edge_pen_width=weight, output="search_example.pdf")

bins =np.array([3,5,8,10,12,14,17,19,21,23,26,28,30,32,35,37,39,41])

X = 10 # 
hours=24
num_of_bins =18
alarm_treshold = 25
weights_of_bins = np.zeros(num_of_bins)
Total_dist_in_24h = 0
Total_num_of_overflows = 0
count = 0
for m in range(hours): 
    poiss_rands= []
    for j in range(num_of_bins):          

        s = np.random.poisson(lambdas_per_hour[j])
        poiss_rands.append(s)
    weights_of_bins += poiss_rands
            
    half_full_bins = np.where(weights_of_bins > alarm_treshold)[0]
    num_of_half_full_bins, = half_full_bins.shape
    
    if num_of_half_full_bins >= X:
        count+=1
        overflows = np.where(weights_of_bins > 50)[0]
        num_of_overflow, = overflows.shape        
        Total_num_of_overflows += num_of_overflow
        
        total_dist = 0    
        path = []
        Id_of_half_full_bins = bins[half_full_bins]
        weights_of_bins[half_full_bins] = 0
        remaining_nodes = Id_of_half_full_bins
        
        target = []
        for n in Id_of_half_full_bins:
            target.append(g.vertex(n))
            
        path.append(0)
        dist = graph_tool.topology.shortest_distance(g, source=g.vertex(0), target=target, weights=weight,
                                                     negative_weights=False, max_dist=None, directed=None,
                                                     dense=False, dist_map=None, pred_map=False)
        min_node = np.argmin(dist)
        total_dist += dist[min_node] 
        current_node = remaining_nodes[min_node]
        path.append(current_node)
        remaining_nodes = np.delete(remaining_nodes, min_node)
    
        
        while remaining_nodes.size > 1:
            target = []
            for n in remaining_nodes:
                target.append(g.vertex(n))
            dist = graph_tool.topology.shortest_distance(g, source=g.vertex(current_node), target=target, weights=weight,
                                                         negative_weights=False, max_dist=None, directed=None,
                                                         dense=False, dist_map=None, pred_map=False)
            min_node = np.argmin(dist)
            total_dist += dist[min_node]
            current_node = remaining_nodes[min_node]
            path.append(current_node)
            remaining_nodes = np.delete(remaining_nodes, min_node)
    
        
        dist = graph_tool.topology.shortest_distance(g, source=g.vertex(current_node), target=g.vertex(remaining_nodes[0]), weights=weight,
                                                     negative_weights=False, max_dist=None, directed=None,
                                                     dense=False, dist_map=None, pred_map=False)
        path.append(remaining_nodes[0])
        total_dist += dist
        dist = graph_tool.topology.shortest_distance(g, source=g.vertex(remaining_nodes[0]), target=g.vertex(0), weights=weight,
                                                     negative_weights=False, max_dist=None, directed=None,
                                                     dense=False, dist_map=None, pred_map=False)
        path.append(0)                                                                                            
        total_dist += dist
        
        Total_dist_in_24h +=total_dist
        

        
        print '----------------------------------'
        print "path of move is :",path
        print "cost of path is :",total_dist
        print '----------------------------------'
average_dist = Total_dist_in_24h/count
print "distance is",Total_dist_in_24h
print "average distance is ", average_dist
Total_cost = Total_dist_in_24h *3.5 + Total_num_of_overflows*20
print "Total cost at the end of day is :", Total_cost
print "Total_num_of_overflows is:" , Total_num_of_overflows
       
