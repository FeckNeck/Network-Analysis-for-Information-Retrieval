import dash
from dash import html, dcc, callback
from modules.corpus import Corpus
import networkx as nx
import plotly.graph_objects as go

dash.register_page(__name__, path='/')

corpus = Corpus()
corpus = corpus.get()

G = nx.Graph()

for index, row in corpus.iterrows():
    authors = row['authors']
    if type(authors) == list:
        if len(authors) > 1:
            for i in range(0, len(authors)):
                for j in range(i + 1, len(authors)):
                    G.add_edge(authors[i], authors[j])

# Extract subgraph
nodes = list(G.nodes)[0:50]
subgraph = G.subgraph(nodes)

pos = nx.spring_layout(subgraph)

edge_trace = go.Scatter(
    x=[pos[edge[0]][0] for edge in subgraph.edges()],
    y=[pos[edge[0]][1] for edge in subgraph.edges()],
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines'
)

node_texts = [author for author in subgraph.nodes()]

node_trace = go.Scatter(
    x=[pos[node][0] for node in subgraph.nodes()],
    y=[pos[node][1] for node in subgraph.nodes()],
    mode='markers',
    hoverinfo='text',
    text=node_texts,
    textposition='bottom center',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        )
    )
)

node_adjacencies = [len(adjacencies) for _, adjacencies in subgraph.adjacency()]
node_text = [f'# of connections: {len(adjacencies)}' for adjacencies in subgraph.adjacency()]

node_trace.marker.color = node_adjacencies
node_trace.text = node_text

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    showlegend=True,
                    hovermode='closest',
                    margin=dict(b=0, l=0, r=0, t=0),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=True),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=True)
                )
)

layout = html.Div([
    dcc.Graph(
        id='network-graph',
        figure=fig,
    )
])
