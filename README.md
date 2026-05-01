# Graph Builder

A Streamlit application for building, visualizing, and managing interactive graphs with nodes and edges that have customizable labels and properties.

## Features

- ✨ **Interactive Graph Visualization** - Real-time graph visualization using Plotly
- ➕ **Add Nodes** - Create nodes with custom labels and properties
- ✏️ **Edit Nodes & Edges** - Update labels and properties on existing elements
- 🗑️ **Delete Elements** - Remove nodes and edges from your graph
- 🔀 **Graph Types** - Support for both directed and undirected graphs
- 💾 **Persistence** - Save and load graphs as JSON files
- 🏷️ **Custom Properties** - Add arbitrary key-value properties to nodes and edges
- 🎨 **Clean UI** - User-friendly Streamlit interface

## Project Structure

```
Graph-Builder/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── src/
    ├── graph_manager.py  # NetworkX graph operations
    └── ui_components.py  # Reusable Streamlit UI elements
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MikePReid/Graph-Builder.git
cd Graph-Builder
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Start the Streamlit application:
```bash
streamlit run app.py
```

The app will open in your default browser. Use the sidebar to:
- Select between directed and undirected graphs
- Add new nodes with labels and properties
- Add edges between nodes
- Edit or delete existing nodes and edges
- Visualize the graph in real-time
- Save/load graphs

## Dependencies

- **streamlit** - Web app framework
- **networkx** - Graph data structure and algorithms
- **plotly** - Interactive visualizations

See `requirements.txt` for specific versions.

## Getting Started

1. Create a new graph (directed or undirected)
2. Add nodes using the "Add Node" form
3. Add edges by selecting source and target nodes
4. Add properties to nodes and edges as needed
5. Visualize your graph in the main display area
6. Save your work using the export functionality

## Future Enhancements

- Graph algorithms (shortest path, centrality, etc.)
- Multiple graph layouts
- Import from various formats (GML, GraphML, etc.)
- Collaborative editing
- Advanced filtering and search
- Custom styling options

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is private. All rights reserved.
