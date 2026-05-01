import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from typing import Optional

def render_graph_display(graph: nx.Graph) -> None:
    """
    Render an interactive graph visualization using Plotly.
    
    Args:
        graph: NetworkX graph object to visualize.
    """
    if graph.number_of_nodes() == 0:
        st.info("📊 Graph is empty. Add nodes to visualize the graph.")
        return
    
    # Calculate layout
    pos = nx.spring_layout(graph, k=2, iterations=50, seed=42)
    
    # Extract nodes and edges
    edge_x = []
    edge_y = []
    
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        showlegend=False
    )
    
    # Node positions
    node_x = []
    node_y = []
    node_text = []
    
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        # Create hover text with node properties
        attrs = graph.nodes[node]
        hover_text = f"<b>{node}</b><br>"
        for key, value in attrs.items():
            hover_text += f"{key}: {value}<br>"
        node_text.append(hover_text)
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[str(node) for node in graph.nodes()],
        textposition="top center",
        hovertext=node_text,
        hoverinfo='text',
        marker=dict(
            showscale=True,
            color=[graph.degree(node) for node in graph.nodes()],
            size=20,
            colorscale='YlGnBu',
            showscale=True,
            colorbar=dict(
                thickness=15,
                title='Node Degree',
                xanchor='left',
                titleside='right'
            ),
            line_width=2,
            line_color='white'
        ),
        showlegend=False
    )
    
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       title='<br>Graph Visualization',
                       titlefont_size=16,
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20, l=5, r=5, t=40),
                       annotations=[dict(
                           text="Hover over nodes to see properties",
                           showarrow=False,
                           xref="paper", yref="paper",
                           x=0.005, y=-0.002
                       )],
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                       )
    
    st.plotly_chart(fig, use_container_width=True)

def render_graph_controls(graph_manager) -> None:
    """
    Render control panel for graph operations.
    
    Args:
        graph_manager: GraphManager instance to operate on.
    """
    st.sidebar.header("⚙️ Graph Controls")
    
    # Display current graph stats
    st.sidebar.metric("Nodes", graph_manager.graph.number_of_nodes())
    st.sidebar.metric("Edges", graph_manager.graph.number_of_edges())
    
    if graph_manager.graph.number_of_nodes() > 0:
        density = nx.density(graph_manager.graph)
        st.sidebar.metric("Density", f"{density:.3f}")

def display_node_properties(graph: nx.Graph, node: str) -> None:
    """
    Display properties of a specific node.
    
    Args:
        graph: NetworkX graph object.
        node: Node identifier.
    """
    if node in graph.nodes():
        st.write(f"**Node:** {node}")
        attrs = dict(graph.nodes[node])
        if attrs:
            st.json(attrs)
        else:
            st.info("No properties assigned to this node.")


def display_edge_properties(graph: nx.Graph, source: str, target: str) -> None:
    """
    Display properties of a specific edge.
    
    Args:
        graph: NetworkX graph object.
        source: Source node identifier.
        target: Target node identifier.
    """
    if graph.has_edge(source, target):
        st.write(f"**Edge:** {source} → {target}")
        attrs = dict(graph.edges[source, target])
        if attrs:
            st.json(attrs)
        else:
            st.info("No properties assigned to this edge.")


def render_graph_stats(graph: nx.Graph) -> None:
    """
    Render graph statistics and metrics.
    
    Args:
        graph: NetworkX graph object.
    """
    if graph.number_of_nodes() == 0:
        st.info("Add nodes to the graph to see statistics.")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Nodes", graph.number_of_nodes())
    
    with col2:
        st.metric("Edges", graph.number_of_edges())
    
    with col3:
        density = nx.density(graph)
        st.metric("Density", f"{density:.3f}")
    
    with col4:
        if isinstance(graph, nx.DiGraph):
            st.metric("Type", "Directed")
        else:
            st.metric("Type", "Undirected")