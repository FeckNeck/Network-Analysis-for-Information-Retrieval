import dash
from dash import Dash, html, dcc
from modules.corpus import Corpus

corpus = Corpus()
corpus.load()
corpus = corpus.get()

app = Dash(__name__, suppress_callback_exceptions=True, use_pages=True)

app.layout = html.Div([

    html.Header(
        html.Div(
            html.Nav([
                html.Img(id="logo", src="assets/book.png", alt="Book Icon"),
                html.Ul([
                    html.Li(
                        dcc.Link(
                            f"{page['name']}", href=page["relative_path"],
                        ),
                    ) for page in dash.page_registry.values()
                ]),
                html.P("Welcome to the Bookstore!")
            ]), className="container"
        ),   
    ),
    html.Section(
        html.Div(
            dash.page_container,
            className="container",
        ),
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)