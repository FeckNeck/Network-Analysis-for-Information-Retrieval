import dash
from dash import html, dcc, dash_table

dash.register_page(__name__, path='/')

from modules.corpus import Corpus

corpus = Corpus()
corpus = corpus.get()
corpus['authors'] = corpus['authors'].apply(lambda x: ', '.join(x))
corpus['references'] = corpus['references'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

layout = html.Div([
    html.H1("Network"),
    html.P("This page will contain a network graph."),
    dash_table.DataTable(
        id='network-table',
        columns=[{"name": i, "id": i} for i in corpus.columns],
        data=corpus.to_dict("records"),
    )
])