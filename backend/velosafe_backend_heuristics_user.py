import osmnx as ox
import networkx as nx
import math
import random


# helper function to polish maxspeed data
def polish_maxspeed(x):
    if isinstance(x, list): # delistify
        x = x[0]
    if x == 'walk': # set walking speed
        return 30.0
    elif math.isnan(float(x)): # set default speed
        return 55.0
    elif float(x) > 80: # clamp
        return 80
    elif float(x) < 30: # clamp
        return 30
    else: # default
        return int(x)

# helper function to generate weight based on road type
def judge_road_type(x):
    if x == 'cycleway':
        return 0.5
    elif x == 'residential':
        return 0.6
    elif x == 'tertiary':
        return 0.9
    elif x == 'service':
        return 1.2
    elif x == 'primary':
        return 1.5
    elif x == 'trunk_link':
        return 1.5
    else:
        return 1.0

# fetch osm data for Zurich
# Note: The search term was found using: https://nominatim.openstreetmap.org/ui/search.html
print('[Velosafe] Fetching OSM data')
#graph = ox.graph_from_place('Altstadt, Zurich, District Zurich, Zurich, 8001, Switzerland', network_type="bike") # Fetch only Kreis 1
#graph = ox.graph_from_place('Zurich, District Zurich, Zurich, Switzerland', network_type="bike") # Fetch Zurich
graph = ox.graph_from_address('Bahnhofbrücke, Bahnhofquai, Hochschulen, Altstadt, Zurich, District Zurich, Zurich, 8001, Switzerland', network_type="bike", dist=1500) # Fetch Around Bahnhofbrücke

# Infer edge speeds and travel times
print('[Velosafe] Inferring travel times')
graph = ox.speed.add_edge_speeds(graph)
graph = ox.speed.add_edge_travel_times(graph)

# Add some points for later use
# Important: Note that longitude comes before latitude here
print('[Velosafe] Fetching locations')
places = {
    'HB': ox.distance.nearest_nodes(graph, 8.53959268566843, 47.377051947586345),
    'ETH': ox.distance.nearest_nodes(graph, 8.54862443374541, 47.376628475591325),
    'opera': ox.distance.nearest_nodes(graph, 8.546596941089128, 47.36529226241242),
    'sihlbruecke': ox.distance.nearest_nodes(graph, 8.532227979007738, 47.37327643359414)
}


## Modifying the graph
# Extracting GeoDataFrame from graph
print('[Velosafe] Applying custom weighting')
gdf_nodes, gdf_edges = ox.graph_to_gdfs(graph)

# Cleaning up Dataframe, making sure there are no lists
gdf_edges['osmid'] = gdf_edges['osmid'].apply(lambda x: x[0] if isinstance(x, list) else x) # delistify
gdf_edges['maxspeed'] = gdf_edges['maxspeed'].apply(lambda x: polish_maxspeed(x)) # polish maxspeed values
gdf_edges['highway'] = gdf_edges['highway'].apply(lambda x: x[0] if isinstance(x, list) else x) # delistify

# Adding columns for heuristics and user ratings
gdf_edges.insert(len(gdf_edges.columns), 'bias_h', 0.0)
gdf_edges.insert(len(gdf_edges.columns), 'bias_u', 0.0)


## Heuristics
#gdf_edges['bias_h'] = gdf_edges.apply(lambda x: x.bias_h + 1.5 if int(x.maxspeed) >= 50 else x.bias_h + 0.5, axis=1) # simple heuristics for speed
gdf_edges['bias_h'] = gdf_edges.apply(lambda x: x.bias_h + 0.5 + (x.maxspeed - 30) / 50, axis=1) # heuristics for speed
gdf_edges['bias_h'] = gdf_edges.apply(lambda x: x.bias_h + judge_road_type(x.highway), axis=1) # heuristics for road type


## User Rating
# currently randomised for demonstration purposes Once user ratings are supported, these weights will be configured by the users
gdf_edges['bias_u'] = gdf_edges['bias_u'].apply(lambda x: random.uniform(0.5, 1.5))

# Update travelcost
gdf_edges_h = gdf_edges.copy()
gdf_edges_h['travel_time'] = gdf_edges_h.apply(lambda x: x.travel_time * (x.bias_h/2), axis=1)

# Update travelcost (combine Heuristics and user rating)
gdf_edges_u = gdf_edges.copy()
weighting = 0.75 # 0: only heuristics, 1: only user rating
gdf_edges_u['travel_time'] = gdf_edges_u.apply(lambda x: x.travel_time * ((1-weighting)*(x.bias_h/2) + weighting*x.bias_u), axis=1)

# Assembling GeoDataFrame into graph
graph_h = ox.graph_from_gdfs(gdf_nodes, gdf_edges_h)
graph_u = ox.graph_from_gdfs(gdf_nodes, gdf_edges_u)

# Calculating the shortest path
print('[Velosafe] Calculating shortest and safest paths')
route_h = ox.shortest_path(graph_h, places['sihlbruecke'], places['opera'], weight="travel_time")
route_u = ox.shortest_path(graph_u, places['sihlbruecke'], places['opera'], weight="travel_time")



# Generating the output
print('[Velosafe] Creating plot')
plot = ox.plot_graph_folium(graph, color='#666666', opacity=0.5)
plot = ox.plot_route_folium(graph, route_h, weight=5, color='#ffff00', opacity=0.5, route_map=plot)
plot = ox.plot_route_folium(graph, route_u, weight=5, color='#00ff00', opacity=0.5, route_map=plot)
plot.save('output.html')