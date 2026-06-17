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

    record = OutageRecord(
        reason=payload["reason"],
        reason_type=payload.get("reasonType", "Fault"),
        start_time=datetime.fromisoformat(payload["startTime"]) if payload.get("startTime") else datetime.utcnow(),
        expected_recovery_time=datetime.fromisoformat(payload["expectedRecoveryTime"]) if payload.get("expectedRecoveryTime") else None,
        operator=payload["operator"],
        notes=payload.get("notes", ""),
        previous_status=elevator.status,
        elevator_id=payload["elevatorId"],
    )

    if not elevator.is_out_of_service:
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

    if not payload or not payload.get("notes", "").strip():
        raise ValueError("Recovery notes are required")

    record.end_time = datetime.utcnow()
    record.notes = (record.notes + "\n" + payload["notes"].strip()) if record.notes else payload["notes"].strip()

    elevator = Elevator.query.get_or_404(record.elevator_id)

    remaining_active = any(
        r.end_time is None and r.id != record.id
        for r in elevator.outage_records
    )

    if remaining_active:
        elevator.is_out_of_service = True
        elevator.status = "Out of Service"
    else:
        elevator.is_out_of_service = False
        all_records = sorted(elevator.outage_records, key=lambda r: r.start_time)
        original_status = next(
            (r.previous_status for r in all_records if r.previous_status),
            "Normal",
        )
        elevator.status = original_status

    db.session.add(record)
    db.session.add(elevator)
    db.session.commit()
    return record.to_dict()
