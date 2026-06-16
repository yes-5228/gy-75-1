from app.extensions import db
from app.models import InspectionRecord, MaintenancePlan, parse_date
from app.repositories.base import commit


def list_plans():
    plans = MaintenancePlan.query.order_by(MaintenancePlan.scheduled_date.asc()).all()
    return [item.to_dict() for item in plans]


def create_plan(payload):
    plan = MaintenancePlan(
        title=payload["title"],
        plan_type=payload["planType"],
        scheduled_date=parse_date(payload["scheduledDate"]),
        assignee=payload["assignee"],
        status=payload.get("status", "Pending"),
        notes=payload.get("notes", ""),
        elevator_id=payload["elevatorId"],
    )
    return commit(plan).to_dict()


def update_plan(plan_id, payload):
    plan = MaintenancePlan.query.get_or_404(plan_id)
    for field, attr in {
        "title": "title",
        "planType": "plan_type",
        "scheduledDate": "scheduled_date",
        "assignee": "assignee",
        "status": "status",
        "notes": "notes",
        "elevatorId": "elevator_id",
    }.items():
        if field in payload:
            value = parse_date(payload[field]) if field == "scheduledDate" else payload[field]
            setattr(plan, attr, value)
    db.session.commit()
    return plan.to_dict()


def list_inspections():
    records = InspectionRecord.query.order_by(InspectionRecord.inspected_at.desc()).all()
    return [item.to_dict() for item in records]


def create_inspection(payload):
    record = InspectionRecord(
        inspector=payload["inspector"],
        result=payload["result"],
        checklist=payload["checklist"],
        attachment_url=payload.get("attachmentUrl", ""),
        elevator_id=payload["elevatorId"],
    )
    return commit(record).to_dict()
