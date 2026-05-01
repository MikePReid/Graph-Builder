import streamlit as st
import networkx as nx
from src.graph_manager import GraphManager
from src.ui_components import render_graph_controls, render_graph_display

st.set_page_config(page_title="Graph Builder", layout="wide")

st.title("🎨 Graph Builder")
st.write("Build, visualize, and manage interactive graphs with custom nodes and edges.")

# Initialize session state
if "graph_manager" not in st.session_state:
    st.session_state.graph_manager = GraphManager()

graph_manager = st.session_state.graph_manager

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Controls")
    
    # Graph type selection
    graph_type = st.radio("Graph Type", ["Undirected", "Directed"])
    if st.button("Create New Graph"):
        graph_manager.create_graph(directed=(graph_type == "Directed"))
        st.success(f"Created new {graph_type} graph!")
    
    st.divider()
    
    # Node operations
    st.subheader("📍 Node Operations")
    with st.expander("Add Node"):
        node_label = st.text_input("Node Label", key="add_node_label")
        node_props = st.text_area("Properties (JSON format)", "{}", key="add_node_props")
        if st.button("Add Node"):
            try:
                import json
                props = json.loads(node_props) if node_props.strip() else {}
                graph_manager.add_node(node_label, props)
                st.success(f"Node '{node_label}' added!")
                st.rerun()
            except json.JSONDecodeError:
                st.error("Invalid JSON format for properties")
    
    # Edge operations
    st.subheader("🔗 Edge Operations")
    with st.expander("Add Edge"):
        nodes = list(graph_manager.graph.nodes())
        if len(nodes) >= 2:
            source = st.selectbox("Source Node", nodes, key="edge_source")
            target = st.selectbox("Target Node", nodes, key="edge_target")
            edge_label = st.text_input("Edge Label", "", key="edge_label")
            edge_props = st.text_area("Edge Properties (JSON)", "{}", key="edge_props")
            if st.button("Add Edge"):
                try:
                    import json
                    props = json.loads(edge_props) if edge_props.strip() else {}
                    graph_manager.add_edge(source, target, edge_label, props)
                    st.success(f"Edge added: {source} → {target}")
                    st.rerun()
                except json.JSONDecodeError:
                    st.error("Invalid JSON format for edge properties")
        else:
            st.info("Add at least 2 nodes to create edges")
    
    st.divider()
    
    # Delete operations
    st.subheader("🗑️ Delete Operations")
    with st.expander("Delete Node"):
        nodes = list(graph_manager.graph.nodes())
        if nodes:
            node_to_delete = st.selectbox("Select Node", nodes, key="delete_node")
            if st.button("Delete Node"):
                graph_manager.delete_node(node_to_delete)
                st.success(f"Node '{node_to_delete}' deleted!")
                st.rerun()
        else:
            st.info("No nodes to delete")
    
    st.divider()
    
    # Graph info
    st.subheader("📊 Graph Info")
    st.write(f"Nodes: {graph_manager.graph.number_of_nodes()}")
    st.write(f"Edges: {graph_manager.graph.number_of_edges()}")
    st.write(f"Type: {'Directed' if isinstance(graph_manager.graph, nx.DiGraph) else 'Undirected'}")

# Main content area
st.subheader("Graph Visualization")
render_graph_display(graph_manager.graph)

# Graph statistics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Nodes", graph_manager.graph.number_of_nodes())
with col2:
    st.metric("Total Edges", graph_manager.graph.number_of_edges())
with col3:
    density = nx.density(graph_manager.graph)
    st.metric("Density", f"{density:.3f}")

# Node and Edge details
if graph_manager.graph.number_of_nodes() > 0:
    st.subheader("📋 Graph Data")
    tab1, tab2 = st.tabs(["Nodes", "Edges"])
    
    with tab1:
        nodes_data = []
        for node, attrs in graph_manager.graph.nodes(data=True):
            nodes_data.append({"Node": node, "Properties": attrs})
        st.dataframe(nodes_data, use_container_width=True)
    
    with tab2:
        if graph_manager.graph.number_of_edges() > 0:
            edges_data = []
            for source, target, attrs in graph_manager.graph.edges(data=True):
                edges_data.append({"Source": source, "Target": target, "Properties": attrs})
            st.dataframe(edges_data, use_container_width=True)
        else:
            st.info("No edges in the graph yet")