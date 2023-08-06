import dash_ace
import dash_bootstrap_components as dbc
from dash import html
from dash.development.base_component import Component

from amora.models import Model


def python_component(model: Model) -> Component:
    source_code = model.path().read_text()
    return html.Div(
        [
            dash_ace.DashAceEditor(
                id="input",
                value=source_code,
                theme="github",
                mode="python",
                tabSize=2,
                enableBasicAutocompletion=True,
                enableLiveAutocompletion=True,
                autocompleter="/autocompleter?prefix=",
                placeholder="Python code ...",
            )
        ]
    )


def sql_component(model: Model) -> Component:
    if model.source() is None:
        return html.Div(
            dbc.Alert(
                "Sourceless model",
                color="primary",
                dismissable=True,
                is_open=True,
            )
        )

    try:
        source_code = model.target_path().read_text()
    except FileNotFoundError:
        return dbc.Alert(
            "⚠️ SQL code unavailable. Run `amora compile` to generate SQL files",
            color="warning",
        )
    else:
        return html.Div(
            [
                dash_ace.DashAceEditor(
                    id="input",
                    value=source_code,
                    theme="github",
                    mode="SQL",
                    tabSize=2,
                    enableBasicAutocompletion=True,
                    enableLiveAutocompletion=True,
                    autocompleter="/autocompleter?prefix=",
                    placeholder="SQL code ...",
                )
            ]
        )
