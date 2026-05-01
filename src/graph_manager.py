import networkx as nx
import json
from typing import Dict, Any, Optional


class GraphManager:
    """Manages graph operations using NetworkX."""
    
    def __init__(self):
        """Initialize the graph manager with an empty undirected graph."""
        self.graph = nx.Graph()
    
    def create_graph(self, directed: bool = False) -> None:
        """
        Create a new graph.
        
        Args:
            directed: If True, creates a DiGraph; otherwise creates an undirected Graph.
        """
        if directed:
            self.graph = nx.DiGraph()
        else:
            self.graph = nx.Graph()
    
    def add_node(self, label: str, properties: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a node to the graph.
        
        Args:
            label: The node identifier/label.
            properties: Dictionary of properties to attach to the node.
        """
        if properties is None:
            properties = {}
        self.graph.add_node(label, **properties)
    
    def update_node(self, label: str, properties: Optional[Dict[str, Any]] = None) -> None:
        """
        Update a node's properties.
        
        Args:
            label: The node identifier/label.
            properties: Dictionary of properties to update.
        """
        if label not in self.graph:
            raise ValueError(f"Node '{label}' does not exist in the graph.")
        
        if properties is None:
            properties = {}
        
        # Update node attributes
        self.graph.nodes[label].update(properties)
    
    def delete_node(self, label: str) -> None:
        """
        Delete a node from the graph.
        
        Args:
            label: The node identifier/label to delete.
        """
        if label in self.graph:
            self.graph.remove_node(label)
    
    def add_edge(self, source: str, target: str, label: str = "", 
                 properties: Optional[Dict[str, Any]] = None) -> None:
        """
        Add an edge between two nodes.
        
        Args:
            source: Source node identifier.
            target: Target node identifier.
            label: Edge label/name.
            properties: Dictionary of properties to attach to the edge.
        """
        if properties is None:
            properties = {}
        
        if label:
            properties['label'] = label
        
        self.graph.add_edge(source, target, **properties)
    
    def update_edge(self, source: str, target: str, label: str = "", 
                    properties: Optional[Dict[str, Any]] = None) -> None:
        """
        Update an edge's properties.
        
        Args:
            source: Source node identifier.
            target: Target node identifier.
            label: New edge label.
            properties: Dictionary of properties to update.
        """
        if not self.graph.has_edge(source, target):
            raise ValueError(f"Edge between '{source}' and '{target}' does not exist.")
        
        if properties is None:
            properties = {}
        
        if label:
            properties['label'] = label
        
        self.graph.edges[source, target].update(properties)
    
    def delete_edge(self, source: str, target: str) -> None:
        """
        Delete an edge from the graph.
        
        Args:
            source: Source node identifier.
            target: Target node identifier.
        """
        if self.graph.has_edge(source, target):
            self.graph.remove_edge(source, target)
    
    def get_node(self, label: str) -> Optional[Dict[str, Any]]:
        """
        Get node attributes.
        
        Args:
            label: The node identifier/label.
            
        Returns:
            Dictionary of node attributes, or None if node doesn't exist.
        """
        if label in self.graph:
            return dict(self.graph.nodes[label])
        return None
    
    def get_edge(self, source: str, target: str) -> Optional[Dict[str, Any]]:
        """
        Get edge attributes.
        
        Args:
            source: Source node identifier.
            target: Target node identifier.
            
        Returns:
            Dictionary of edge attributes, or None if edge doesn't exist.
        """
        if self.graph.has_edge(source, target):
            return dict(self.graph.edges[source, target])
        return None
    
    def save_graph(self, filename: str) -> None:
        """
        Save the graph to a JSON file.
        
        Args:
            filename: Path to the output JSON file.
        """
        data = {
            'directed': isinstance(self.graph, nx.DiGraph()),
            'nodes': [{'id': node, 'attr': dict(attrs)} 
                     for node, attrs in self.graph.nodes(data=True)],
            'edges': [{'source': u, 'target': v, 'attr': dict(attrs)} 
                     for u, v, attrs in self.graph.edges(data=True)]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_graph(self, filename: str) -> None:
        """
        Load a graph from a JSON file.
        
        Args:
            filename: Path to the JSON file to load.
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Create appropriate graph type
        self.create_graph(directed=data.get('directed', False))
        
        # Add nodes
        for node_data in data.get('nodes', []):
            self.add_node(node_data['id'], node_data.get('attr', {}))
        
        # Add edges
        for edge_data in data.get('edges', []):
            self.add_edge(
                edge_data['source'],
                edge_data['target'],
                properties=edge_data.get('attr', {})
            )
