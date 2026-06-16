from sqlalchemy import func

from app.extensions import db
from app.models import FaultReport, RepairTracking
from app.repositories.base import commit


OPEN_STATUSES = {"Pending", "In Progress", "Review", "待受理", "处理中", "待复核"}
DONE_STATUSES = {"Completed", "已完成"}


def list_faults():
    faults = FaultReport.query.order_by(FaultReport.reported_at.desc()).all()
    return [item.to_dict() for item in faults]


def create_fault(payload):
    fault = FaultReport(
        reporter=payload["reporter"],
        phone=payload["phone"],
        fault_type=payload["faultType"],
        description=payload["description"],
        priority=payload.get("priority", "Normal"),
        status=payload.get("status", "Pending"),
        elevator_id=payload["elevatorId"],
    )
    return commit(fault).to_dict()


def list_tracking_logs(fault_id=None):
    query = RepairTracking.query.order_by(RepairTracking.created_at.desc())
    if fault_id:
        query = query.filter_by(fault_id=fault_id)
    return [item.to_dict() for item in query.all()]


def create_tracking_log(payload):
    log = RepairTracking(
        action=payload["action"],
        handler=payload["handler"],
        status=payload["status"],
        cost=float(payload.get("cost", 0) or 0),
        fault_id=payload["faultId"],
    )
    fault = FaultReport.query.get_or_404(payload["faultId"])
    fault.status = payload["status"]
    db.session.add(log)
    db.session.commit()
    return log.to_dict()


def statistics():
    status_counts = dict(
        db.session.query(FaultReport.status, func.count(FaultReport.id))
        .group_by(FaultReport.status)
        .all()
    )
    priority_counts = dict(
        db.session.query(FaultReport.priority, func.count(FaultReport.id))
        .group_by(FaultReport.priority)
        .all()
    )
    total_cost = db.session.query(func.coalesce(func.sum(RepairTracking.cost), 0)).scalar()
    open_faults = sum(count for status, count in status_counts.items() if status in OPEN_STATUSES)
    completed_faults = sum(count for status, count in status_counts.items() if status in DONE_STATUSES)
    return {
        "totalFaults": FaultReport.query.count(),
        "openFaults": open_faults,
        "completedFaults": completed_faults,
        "totalCost": round(float(total_cost), 2),
        "statusCounts": status_counts,
        "priorityCounts": priority_counts,
    }
