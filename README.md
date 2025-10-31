# report

#TODO: how can i print automatically seleccionats prints() in README.md

La xarxa OPERATIVA completa a data de 2021 conte: 
nodes =  13572
arcs = 13682


La xarxa OPERATIVA completa a data de 2023 conte: 
nodes =  13608
arcs = 13720


--- ( 2021 ) ---

La xarxa connectada a la depuradora conte: 
nodes =  12017
arcs = 12516
nodes OUTFALL = 128
nodes CHAMBER= 189
nodes CHAMBER-NETINIT = 15  (camaras amb un sol arc)
nodes MANHOLE = 9812
arcs sobreeixidor (marcats) = 278

-- errors detectats --

nodes_amb_codi_erroni_2021 = (  2334  )
nodes_amb_codi_erroni_2023 = (  2346  )


nodes que no arriben a la depuradora ni a un outfall ni a un chamberNETINIT = 69
nodes direccionats cap a fora de la xarxa que no son outfall:37
camaras amb un sol arc: 15
(report_direccions)

nodes sobreeixidor detectats = 136
nodes sobreeixidor marcats = 278
nodes marcats com a sobreeixidors que no ho son: 166
nodes sobreeixidors detectat que no estan marcats: 26
(report_sobreeixidors)

correccio en nodes:

top_elev
nodes fora del rang esperat: 25
nodes_erronis incials 4430
(correccio implementat a nodes/arcs_corregits.gpkg)

ymax
nodes erronis fora del rang esperat: 194
nodes erronis totals incluint nan: 3063
(correccio implementada a nodes/arcs_corregits.gpkg)


correccio en arcs (erronis fora del rang esperat incluint nan):
y1 corregits = 5881
y2 corregits = 4875
(correccio implementada a nodes/arcs_corregits.gpkg)

arcs sobreeixidor = 136
Sobreeixidors (y1) arreglats = 63
(correccio implementada a nodes/arcs_corregits.gpkg)
Sobreixidor detectats extranys amb node_1  menys de 2 arcs connectats  10
['TR0022764', 'TR0023350', 'TR0022834', 'TR0022590', 'TR0022507', 'TR0010402', 'TR0025013', 'TR0050138', 'TR0011035', 'TR0005674']
(?) recomanem revisio per desconnexio de la xarxa


# xarxa

#TODO correccio sobreeixidors

#TODO correccio pendents

how update correctly with def

alguns (46) custim_y1 encara nan, perque?

els sobreixidors y1 no shan ficat correctament, perque?

arreglar slopes negatives i forarang 
localitzar bombes
rang slope esperat (-0.5,1)


WARNING 08: elevation drop exceeds length for Conduit 36017
WARNING 08: elevation drop exceeds length for Conduit 25022
WARNING 03: negative offset ignored for Link 35280

Error near line 18120 -> ['27172', '14970', '14968', 'CONDUIT', '2.0-3091.6295', '0.0200']

# dry_scenario

de la llista de manholes hem de extreure aquells que estan conectats a arcs amb
['fluid_type']=='PLUVIALS'




# WARNINGS
SWMM: 2H(time. exec. 00:02:00)
---

flow routing: -0.01%
indicates the percent difference between the inflow and outflow from the system due to the flow routing calculation. A negative value, as in your example, indicates that there is more outflow than inflow, similar to the continuity error.
A small negative flow routing value may not significantly affect the simulation results.
---

Continuity Error (%) .....        -0.009
The continuity error represents the difference between the total inflow and outflow at nodes in the system and is expressed as a percentage of the total inflow.
---




WARNING 03: negative offset ignored for Link 27481            
WARNING 03: negative offset ignored for Link 27481            
WARNING 03: negative offset ignored for Link 29884  

Offset values are used to specify the elevation difference between the invert (bottom) of a conduit or channel and the elevation of the downstream node.
A negative offset value implies that the invert of the conduit or channel is higher than the downstream node, which is physically impossible. Therefore, SWMM ignores the negative offset value and assumes that the invert elevation is equal to the downstream node elevation.  
---


WARNING 04: minimum elevation drop used for Conduit 26557   
WARNING 04: minimum elevation drop used for Conduit 35452 
WARNING 04: minimum elevation drop used for Conduit 26506     

The minimum elevation drop is the minimum allowable difference in elevation between the upstream and downstream nodes of a conduit. This value is specified in the input file to prevent unrealistic situations where the difference in elevation between the two nodes is too small.
When the elevation difference between the upstream and downstream nodes is less than the specified minimum elevation drop, SWMM will use the minimum elevation drop value instead. 
---


WARNING 02: maximum depth increased for Node 13910            
WARNING 02: maximum depth increased for Node 16317            
WARNING 02: maximum depth increased for Node 17617            

This warning message is generated when the depth of a node exceeds the maximum depth specified in the input file. When this happens, SWMM will automatically increase the maximum depth of the node to prevent it from overflowing.
The warning message is simply a notification to the user that the maximum depth has been increased, and it does not necessarily indicate an error in the model. 
---


WARNING 08: elevation drop exceeds length for Conduit 36545
WARNING 08: elevation drop exceeds length for Conduit 35822
WARNING 08: elevation drop exceeds length for Conduit 28804

The warning message means that the elevation difference between the upstream and downstream nodes of the conduit is greater than the length of the conduit. This situation is not physically possible and may indicate a mistake in the input data.
---




  







