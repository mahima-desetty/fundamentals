import networkx as nx
import plotly.graph_objects as go


def build_concept_tree(topic, llm_response):
    """Convert LLM output into a tree structure."""
    tree = nx.DiGraph()
    tree.add_node(topic)

    for index, (concept, reasoning) in enumerate(llm_response.items()):
        tree.add_node(concept)
        tree.add_edge(topic, concept)
    return tree


# def build_subgraph(parent_graph, node):
#     """Create a subgraph centered on the clicked node."""
#     sub_nodes = list(nx.descendants(parent_graph, node))
#     sub_nodes.append(node)  # Include the clicked node
#     return parent_graph.subgraph(sub_nodes)


def plot_tree(tree, node_data):
    """Create a Plotly figure for the NetworkX tree."""
    pos = nx.spring_layout(tree, scale=3)  # Generate positions for nodes
    edges = list(tree.edges())
    nodes = list(tree.nodes())

    # Extract x, y positions for nodes
    x_nodes = [pos[node][0] for node in nodes]
    y_nodes = [pos[node][1] for node in nodes]

    # Extract x, y positions for edges
    x_edges = []
    y_edges = []
    for edge in edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    # Create edge trace
    edge_trace = go.Scatter(
        x=x_edges,
        y=y_edges,
        line=dict(width=2, color='#ccc'),
        hoverinfo='none',
        mode='lines'
    )

    node_hovertext = [node_data.get(node, f"{node}") for node in tree.nodes()]

    # Create node trace
    node_trace = go.Scatter(
        x=x_nodes,
        y=y_nodes,
        mode='markers+text',
        text=[node for node in tree.nodes()],  # Use node ID as text
        textfont=dict(size=14, color="black"),  # Inside node labels
        textposition="top center",
        marker=dict(
            size=30,  # Bigger nodes
            color="#007aff",  # Sleek blue nodes
            line=dict(width=2, color="white"),  # White border for contrast
            opacity=0.9  # Slight transparency
        ),
        hovertext=node_hovertext,
        hoverinfo='text'
    )

    # Combine traces into a figure
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False,),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black", size=18, family="Times New Roman"),
        margin=dict(l=50, r=50, t=50, b=50),  # Slim margins
        autosize=True,  # Ensure responsiveness,
        hovermode="closest",
        clickmode="select+event"
    )
    return fig
