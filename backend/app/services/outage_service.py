from datetime import datetime

from app.extensions import db
from app.models import Elevator, OutageRecord
from app.repositories.base import commit


def list_outage_records(elevator_id=None):
    query = OutageRecord.query.order_by(OutageRecord.start_time.desc())
    if elevator_id:
        query = query.filter_by(elevator_id=elevator_id)
    return [item.to_dict() for item in query.all()]


def register_outage(payload):
    elevator = Elevator.query.get_or_404(payload["elevatorId"])
    if elevator.is_out_of_service:
        raise ValueError("Elevator is already out of service")

    record = OutageRecord(
        reason=payload["reason"],
        reason_type=payload.get("reasonType", "Fault"),
        start_time=datetime.fromisoformat(payload["startTime"]) if payload.get("startTime") else datetime.utcnow(),
        expected_recovery_time=datetime.fromisoformat(payload["expectedRecoveryTime"]) if payload.get("expectedRecoveryTime") else None,
        operator=payload["operator"],
        notes=payload.get("notes", ""),
        elevator_id=payload["elevatorId"],
    )

    elevator.is_out_of_service = True
    elevator.status = "Out of Service"

    db.session.add(record)
    db.session.add(elevator)
    db.session.commit()
    return record.to_dict()


def restore_service(outage_id, payload=None):
    record = OutageRecord.query.get_or_404(outage_id)
    if record.end_time is not None:
        raise ValueError("Outage record is already closed")

    record.end_time = datetime.utcnow()
    if payload and payload.get("notes"):
        record.notes = (record.notes + "\n" + payload["notes"]) if record.notes else payload["notes"]

    elevator = Elevator.query.get_or_404(record.elevator_id)
    elevator.is_out_of_service = False
    active_fault_outage = any(
        r.end_time is None and r.reason_type == "Fault"
        for r in elevator.outage_records
    )
    if not active_fault_outage:
        elevator.status = "Normal"

    db.session.add(record)
    db.session.add(elevator)
    db.session.commit()
    return record.to_dict()
