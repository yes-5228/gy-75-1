from flask import Blueprint, request

from app.services.maintenance_service import (
    create_inspection,
    create_plan,
    list_inspections,
    list_plans,
    update_plan,
)

bp = Blueprint("maintenance", __name__)


@bp.get("/maintenance-plans")
def maintenance_plans():
    return {"items": list_plans()}


@bp.post("/maintenance-plans")
def add_maintenance_plan():
    return create_plan(request.get_json() or {}), 201


@bp.patch("/maintenance-plans/<int:plan_id>")
def edit_maintenance_plan(plan_id):
    return update_plan(plan_id, request.get_json() or {})


@bp.get("/inspections")
def inspections():
    return {"items": list_inspections()}


@bp.post("/inspections")
def add_inspection():
    return create_inspection(request.get_json() or {}), 201
