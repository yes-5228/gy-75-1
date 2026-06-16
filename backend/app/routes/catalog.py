from flask import Blueprint

from app.services.catalog_service import list_communities, list_elevators

bp = Blueprint("catalog", __name__)


@bp.get("/communities")
def communities():
    return {"items": list_communities()}


@bp.get("/elevators")
def elevators():
    return {"items": list_elevators()}
