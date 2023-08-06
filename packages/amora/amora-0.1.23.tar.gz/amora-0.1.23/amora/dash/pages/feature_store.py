from typing import Iterable, Union

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.development.base_component import Component
from feast import Feature, FeatureView

from amora.dash.components import (
    materialization_badge,
    model_columns,
    model_datatable,
    model_labels,
    model_summary,
)
from amora.feature_store import fs as store
from amora.feature_store.registry import FEATURE_REGISTRY
from amora.models import Model

dash.register_page(
    __name__, fa_icon="fa-shopping-cart", location="sidebar", name="Feature Store"
)


def entities_list_items(entities: Iterable[str]):
    for entity in entities:
        yield dbc.ListGroupItem(entity, color="primary")


def features_list_items(features: Iterable[Feature]):
    for feature in features:
        yield dbc.ListGroupItem(feature.name)


def icon_for_model(model: Model) -> html.I:
    # fixme: What kind of contract should we expect from the model ?
    icon = getattr(model, "feature_view_fa_icon", None)
    icon = icon() if icon else "fa-square-question"
    return html.I(className=f"fa-solid {icon}")


def card_item(model: Model, fv: Union[FeatureView, None]) -> Component:
    return dbc.Card(
        [
            dbc.CardHeader(
                dbc.Row(
                    [
                        dbc.Col(icon_for_model(model)),
                        dbc.Col(
                            html.H4(model.__tablename__, className="card-title"),
                        ),
                    ],
                    justify="between",
                )
            ),
            dbc.CardBody(
                [
                    model_labels.component(model),
                    materialization_badge.component(
                        fv.last_updated_timestamp if fv else None
                    ),
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                model_summary.component(model),
                                title="📈 Summary",
                            ),
                            dbc.AccordionItem(
                                model_columns.component(model),
                                title="📝 Docs",
                            ),
                            dbc.AccordionItem(
                                model_datatable.component(model),
                                title="🍰 Sample dataset",
                            ),
                        ],
                        start_collapsed=True,
                    ),
                ]
            ),
        ],
    )


def layout() -> Component:
    registry_fvs = {
        fv.name: fv for fv in store.registry.list_feature_views(store.project)
    }

    if registry_fvs:
        id_ = "feature-store-content"
        feature_views = html.Div(
            [
                card_item(model=model, fv=registry_fvs.get(fv.name))
                for (fv, fs, model) in list(FEATURE_REGISTRY.values())
            ]
        )
    else:
        id_ = "feature-views-loading-error"
        feature_views = html.Div([html.H1("Error loading feature view...")])

    return html.Div(
        id=id_,
        children=[
            html.H1("Feature Store"),
            html.Hr(),
            feature_views,
        ],
    )
