
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import momepy as mm
import networkx as nx
from shapely import Point, LineString, reverse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from pyproj import Transformer
import datetime



def direccionament(subGraph,edar):

    # nodes marcats com OUTFALL
    outfalls= [node for node, data in subGraph.nodes(data=True) if data['epa_type'] == 'OUTFALL']
    # nodes marcats com CHAMBERS i son inici de xarxa
    chambers_netinit= [node for node, data in subGraph.nodes(data=True) if data['nodecat_id'] == 'CEC' and subGraph.degree(node)==1]

    # S'intercanvien els valors del node 1 i node 2 de l'aresta
    attributes = ['node_', 'y', 'custom_y', 'elev', 'custom_elev', 'sys_elev', 'nodetype_', 'sys_y', 'r', 'z']
        
    def intercambiarValores(data):
        for attribute in attributes:
            if attribute+'1' in data:
                aux = data[attribute+'1']
                data[attribute+'1'] = data[attribute+'2']
                data[attribute+'2'] = aux
        if 'geometry' in data:
            data['geometry'] = reverse(data['geometry'])
        return data


# Per direccionar els arcs del subGraph que no arriben a la depuradora o als nodes de sobreiximent
# 1. Trobem tots els nodes que no arriben a la depuradora
# 2. Trobem els nodes del punt 1 que no arriben a cap outfall/chamberNETINIT
    no_llegan_depuradora = [node for node in subGraph.nodes if not nx.has_path(subGraph, node, edar)]

    no_llegan_outfall = []
    for node in no_llegan_depuradora:
        outfalls_i_chambers = outfalls + chambers_netinit
        if node not in outfalls_i_chambers :
            llega = False
            i = 0
            while not llega and len(outfalls_i_chambers)>i:
                llega = nx.has_path(subGraph, node, outfalls_i_chambers[i])
                i += 1
            if not llega:
                no_llegan_outfall.append(node)

    print('nodes que no arriben a la depuradora =', len(no_llegan_depuradora))
    print('nodes que no arriben a la depuradora ni a un outfall ni a un chamberNETINIT =', len(no_llegan_outfall))


    malament = no_llegan_outfall.copy()

# 3. Mentre hi hagi nodes que no arribin a la depuradora ni a un outfall
# 3.1 Per tots aquests nodes
# 3.1.1 Mirem si els seus veins arriben a la depuradora
# 3.1.2 Si algun vei arriba a la depuradora, afegim un nou arc que va del node al vei i eliminem l'antic
# 3.2 Si cap dels seus veins arriba a la depuradora, s'afegeix de nou a la llista  de nodes a revisar
    arcs_girats = []
    while len(no_llegan_outfall)>0:
        no = []
        for node in no_llegan_outfall:
            teCami = nx.has_path(subGraph, node, edar)
            if not teCami:
                veins = list(nx.all_neighbors(subGraph, node))
            while not teCami and len(veins)>0:
                v = veins.pop()
                teCami = nx.has_path(subGraph, v, edar)
                if teCami and subGraph.has_edge(v,node):
                    data = intercambiarValores(subGraph.get_edge_data(v, node))
                    data['girada'] = True
                    subGraph.add_edge(node, v, **data)
                    subGraph.remove_edge(v, node)
                    arcs_girats.append(data['code'])
            if not teCami:
                no.append(node)
        no_llegan_outfall = no
  
# Si tornem a veure els nodes que no arriben a la depuradora, haurien de quedar 1 (la depuradora)

    no_llegan_depuradora_arreglat = [node for node in subGraph.nodes if not nx.has_path(subGraph, node, edar)]

    no_llegan_outfall_arreglat = []
    for node in no_llegan_depuradora_arreglat:
        if node not in outfalls:
            llega = False
            i = 0
            while not llega and len(outfalls)>i:
                llega = nx.has_path(subGraph, node, outfalls[i])
                i += 1
            if not llega:
                no_llegan_outfall_arreglat.append(node)
        
    print('nodes que no arriben a la depuradora després del direccionament =', len(no_llegan_depuradora_arreglat))
    print('nodes que no arriben a la depuradora ni a un outfall després del direccionament =', len(no_llegan_outfall_arreglat))

    return subGraph, malament, arcs_girats





############################################################################################################
############################################################################################################
############################################################################################################


def slopes(subGraph,zero_slope=-0.001, max_iteratons=200):

#1.
# Calculem les h de tots els nodes (altura desde el nivell del mar)
    nodes_h = {}
    for node, data in subGraph.nodes(data=True):
        nodes_h[data['node_id']] = data['custom_top_elev'] - data['custom_ymax']

# Calculem la slope de totes les arestes
    arcs_slope_h = {}
    for u, v, data in subGraph.edges(data=True):
        codi1 = data['node_1']
        codi2 = data['node_2']
        arcs_slope_h[(codi1, codi2)] = (nodes_h[codi1] - nodes_h[codi2]) / data['gis_length']


# Mentre hi hagi elements amb una pendent negativa
    i = 0
    n = sum(np.array(list(arcs_slope_h.values())) <= zero_slope)
    t = 0
    p = 0.001# this is an small positive angles we use to correct the negative slopes that we adjust to impove convergency
    
    while sum(np.array(list(arcs_slope_h.values())) <= zero_slope) > 0 and t < max_iteratons:
        print(f"Iteració {i}. Falten {sum(np.array(list(arcs_slope_h.values())) <= zero_slope)} amb slope negatives amb min {min(np.array(list(arcs_slope_h.values())))}")
        # Recorrem totes les arestes
        for u, v, data in subGraph.edges(data=True):
            codi1 = data['node_1']
            codi2 = data['node_2']
    
# Si la pendent és negativa
            if arcs_slope_h[(codi1,codi2)] <= zero_slope:
                arcs_slope_h[(codi1,codi2)] = p   #p <-- corregtim amb un angle positiu p
                h1 = nodes_h[codi1]
                h2 = nodes_h[codi2]
      
                new_h1 = (h1 + h2) / 2
                new_h2 = (h1 + h2) / 2 - p*data['gis_length'] #p <-- corregtim amb un angle positiu p
      
                nodes_h[codi1] = new_h1
                nodes_h[codi2] = new_h2
# informem del canvi al veins  
                for j in subGraph.predecessors(u):
                    codi_j = subGraph.nodes[j]['node_id']
                    data_slope = subGraph.edges[j, u]
                    arcs_slope_h[(codi_j, codi1)] = (nodes_h[codi_j] - nodes_h[codi1]) / data_slope['gis_length']
                for j in subGraph.successors(u):
                    codi_j = subGraph.nodes[j]['node_id']
                    data_slope = subGraph.edges[u, j]
                    arcs_slope_h[(codi1, codi_j)] = (nodes_h[codi1] - nodes_h[codi_j]) / data_slope['gis_length']



                for j in subGraph.predecessors(v):
                    codi_j = subGraph.nodes[j]['node_id']
                    data_slope = subGraph.edges[j, v]
                    arcs_slope_h[(codi_j, codi2)] = (nodes_h[codi_j] - nodes_h[codi2]) / data_slope['gis_length']
                for j in subGraph.successors(v):
                    codi_j = subGraph.nodes[j]['node_id']
                    data_slope = subGraph.edges[v, j]
                    arcs_slope_h[(codi2, codi_j)] = (nodes_h[codi2] - nodes_h[codi_j]) / data_slope['gis_length']
      
        if n > sum(np.array(list(arcs_slope_h.values())) <= zero_slope):
            n = sum(np.array(list(arcs_slope_h.values())) <= zero_slope)
            t = 0
        else:
            t += 1
        i += 1

    print(f"Falten {sum(np.array(list(arcs_slope_h.values())) <= zero_slope)} slope negatives, amb min {min(np.array(list(arcs_slope_h.values())))}")


# Guardem la nova profunditat new_ymax=z-h de tots els nodes

    new_ymax=[]
    for node, data in subGraph.nodes(data=True):
        new_ymax_value= data['custom_top_elev'] - nodes_h[data['node_id']]
        data['custom_ymax']= data['custom_top_elev'] - nodes_h[data['node_id']]
        new_ymax.append({'code': data['code'], 'new_ymax': new_ymax_value})
    new_ymax=pd.DataFrame.from_records(new_ymax)


# Calculem les slopes
    slopes=[]
    slope_neg=0
    
    for u, v, data in subGraph.edges(data=True):
        data1 = subGraph.nodes[u]
        data2 = subGraph.nodes[v]
        Delta_h=(nodes_h[codi1]-nodes_h[codi2])
        slope_corr=(nodes_h[codi1]-nodes_h[codi2])/data['gis_length']

        data['custom_y2'] = new_ymax.loc[new_ymax['code'] == data2['code']]['new_ymax'].item()
        data['custom_y1'] = new_ymax.loc[new_ymax['code'] == data1['code']]['new_ymax'].item()

        h1 = data1['custom_top_elev'] - data['custom_y1']
        h2 = data2['custom_top_elev'] - data['custom_y2']
        slope=(h1-h2)/data['gis_length']
        
        if slope<0:
            #data['custom_y2'] = new_ymax.loc[new_ymax['code'] == data2['code']]['new_ymax'].item()
            data['custom_y1']=data1['custom_top_elev']-data2['custom_top_elev']+ data['custom_y2']
            slope_neg +=1
            #new_y1_y2.append({'code': data['code'], 'new_y2': data['custom_y1'], 'new_y2': data['custom_y2']})
        if slope > 0.15:
            #data['custom_y1'] = new_ymax.loc[new_ymax['code'] == data1['code']]['new_ymax'].item()
            data['custom_y2']=0.15*data['gis_length'] - (data1['custom_top_elev']-data['custom_y1']) + data2['custom_top_elev']
        #else:
        #    data['custom_y1'] = new_ymax.loc[new_ymax['code'] == data1['code']]['new_ymax'].item()
        #    data['custom_y2'] = new_ymax.loc[new_ymax['code'] == data2['code']]['new_ymax'].item()
            
            #new_y1_y2.append({'code': data['code'], 'new_y2': data['custom_y1'], 'new_y2': data['custom_y2']})
        h1 = data1['custom_top_elev'] - data['custom_y1']
        h2 = data2['custom_top_elev'] - data['custom_y2']
        slope_final=(h1-h2)/data['gis_length']
        slopes.append({'code': data['code'], 'slope_corr': slope_corr,'Delta_h_corr': Delta_h, 'slope_final': slope_final})
    slopes = pd.DataFrame.from_records(slopes)


    new_y1_y2=[]
    for node1, node2, data in subGraph.edges(data=True):
        new_y1_y2.append({'code': data['code'], 'new_y1': data['custom_y1'], 'new_y2': data['custom_y2']})
    new_y1_y2=pd.DataFrame.from_records(new_y1_y2)

    

    print(f" --> slopes negatives finals = ( {slope_neg} ), amb min = ( {min(np.array(list(slopes['slope_final'])))} )")

    return new_ymax, new_y1_y2, slopes
    