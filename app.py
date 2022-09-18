from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime
import numpy as np


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA, dbc.icons.FONT_AWESOME],
)

# Trick to get screen size
app.clientside_callback(
    """
    function(href) {
        var w = window.innerWidth;
        var h = window.innerHeight;
        return {'height': h, 'width': w};
    }
    """,
    Output("viewport_container", "children"),
    Input("url", "href"),
)

def get_bootstrap_breakpoint(width: float) -> str:
    if width < 567:
        return "xs"
    elif width < 768:
        return "sm"
    elif width < 992:
        return "lg"
    else:
        return "xl"

def make_layout():

    date = datetime.utcnow()
    data = pd.DataFrame()

    title = []

    cursive_text = " *Some nice text in cursive to show markdown* "

    for i in range(100):
        n = 5*(i % 2)
        title_i = str(date) + cursive_text + \
                  "\n" + "[" + (n + 5)*"The second lineeeeeeee " + "](https://www.github.com)"

        title.append(title_i)

    data["title"] = title

    main_table = dash_table.DataTable(
        data.to_dict("records"),
        [
            {"name": "Title", "id": "title", "type": "text", "presentation": "markdown"}
        ],
        id="main_table",
        filter_action="native",
        sort_action="native",
        style_cell={
            "padding-left": "10px",
            "whiteSpace": "pre-line",
        },
        style_data={
            "text-align": "left",
            "vertical-align": "middle",
            "text-overflow": "ellipsis",
            "max-width": "0",
        },
        fixed_rows={"headers": True},
        virtualization=True,
        style_as_list_view=True,
    )

    layout = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col([main_table], xs=12, sm=12, md=12, lg=9, xl=10),
                ],
                className="g-0",
            ),
            dcc.Location(id="url"),  # For getting the
            html.Div(id="viewport_container"),  # screensize
        ],
    )

    return layout

app.title = "Dash DataTable Scroll Issue Demonstrator"
app.layout = make_layout
server = app.server

if __name__ == "__main__":
    app.run_server()
