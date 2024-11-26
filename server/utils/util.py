from typing import Tuple, List, Dict
import networkx as nx
import osmnx as ox

def route(origin: str, destination: str) -> Tuple[List[str], Dict]:
    """
    Generate a real route between the origin and destination using OSMnx and NetworkX.
    """
    try:
        # Load the graph based on the origin's location
        G = ox.graph_from_address(origin, network_type='drive')
        G = ox.add_edge_speeds(G)  # Add speed estimates to the graph
        G = ox.add_edge_travel_times(G)  # Add travel time estimates

        # Find the nearest nodes to the origin and destination
        origin_node = ox.nearest_nodes(G, *ox.geocode(origin))
        destination_node = ox.nearest_nodes(G, *ox.geocode(destination))

        # Find the shortest path using travel time as the weight
        path = nx.shortest_path(G, origin_node, destination_node, weight='travel_time')

        # Convert the path to a list of place names
        place_names = [ox.geocode_to_gdf({'y': G.nodes[node]['y'], 'x': G.nodes[node]['x']})['display_name'].iloc[0] for node in path]

        status = {
            'New': 0,
            'In Transit': 1,
            'Delivered': 2
        }

        return place_names, status

    except Exception as e:
        raise ValueError(f"Failed to calculate route: {e}")
