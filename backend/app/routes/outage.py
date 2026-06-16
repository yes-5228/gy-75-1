from flask import Blueprint, jsonify, request

from app.services.outage_service import (
    list_outage_records,
    register_outage,
    restore_service,
)

bp = Blueprint("outage", __name__)


@bp.get("/outage-records")
def outage_records():
    elevator_id = request.args.get("elevatorId", type=int)
    return {"items": list_outage_records(elevator_id)}


@bp.post("/outage-records")
def add_outage_record():
    try:
        return register_outage(request.get_json() or {}), 201
    except ValueError as e:
        return {"error": str(e)}, 400


@bp.post("/outage-records/<int:record_id>/restore")
def restore_outage(record_id):
    try:
        return restore_service(record_id, request.get_json() or {})
    except ValueError as e:
        return {"error": str(e)}, 400
