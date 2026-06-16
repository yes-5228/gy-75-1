from datetime import date, datetime

from app.extensions import db


class Community(db.Model):
    __tablename__ = "communities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(240), nullable=False)
    manager = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(40), nullable=False)

    elevators = db.relationship("Elevator", back_populates="community", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "manager": self.manager,
            "phone": self.phone,
        }


class Elevator(db.Model):
    __tablename__ = "elevators"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), unique=True, nullable=False)
    building = db.Column(db.String(80), nullable=False)
    unit = db.Column(db.String(80), nullable=False)
    brand = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(40), default="Normal", nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id"), nullable=False)

    community = db.relationship("Community", back_populates="elevators")

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "building": self.building,
            "unit": self.unit,
            "brand": self.brand,
            "status": self.status,
            "communityId": self.community_id,
            "communityName": self.community.name if self.community else "",
        }


class MaintenancePlan(db.Model):
    __tablename__ = "maintenance_plans"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    plan_type = db.Column(db.String(40), nullable=False)
    scheduled_date = db.Column(db.Date, nullable=False)
    assignee = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(40), default="Pending", nullable=False)
    notes = db.Column(db.Text, default="", nullable=False)
    elevator_id = db.Column(db.Integer, db.ForeignKey("elevators.id"), nullable=False)

    elevator = db.relationship("Elevator")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "planType": self.plan_type,
            "scheduledDate": self.scheduled_date.isoformat(),
            "assignee": self.assignee,
            "status": self.status,
            "notes": self.notes,
            "elevatorId": self.elevator_id,
            "elevatorCode": self.elevator.code if self.elevator else "",
            "communityName": self.elevator.community.name if self.elevator and self.elevator.community else "",
        }


class InspectionRecord(db.Model):
    __tablename__ = "inspection_records"

    id = db.Column(db.Integer, primary_key=True)
    inspected_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    inspector = db.Column(db.String(80), nullable=False)
    result = db.Column(db.String(40), nullable=False)
    checklist = db.Column(db.Text, nullable=False)
    attachment_url = db.Column(db.String(240), default="", nullable=False)
    elevator_id = db.Column(db.Integer, db.ForeignKey("elevators.id"), nullable=False)

    elevator = db.relationship("Elevator")

    def to_dict(self):
        return {
            "id": self.id,
            "inspectedAt": self.inspected_at.isoformat(timespec="minutes"),
            "inspector": self.inspector,
            "result": self.result,
            "checklist": self.checklist,
            "attachmentUrl": self.attachment_url,
            "elevatorId": self.elevator_id,
            "elevatorCode": self.elevator.code if self.elevator else "",
        }


class FaultReport(db.Model):
    __tablename__ = "fault_reports"

    id = db.Column(db.Integer, primary_key=True)
    reporter = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    fault_type = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(40), default="Normal", nullable=False)
    status = db.Column(db.String(40), default="Pending", nullable=False)
    reported_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    elevator_id = db.Column(db.Integer, db.ForeignKey("elevators.id"), nullable=False)

    elevator = db.relationship("Elevator")
    tracking_logs = db.relationship(
        "RepairTracking",
        back_populates="fault",
        cascade="all, delete-orphan",
        order_by="RepairTracking.created_at.desc()",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "reporter": self.reporter,
            "phone": self.phone,
            "faultType": self.fault_type,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "reportedAt": self.reported_at.isoformat(timespec="minutes"),
            "elevatorId": self.elevator_id,
            "elevatorCode": self.elevator.code if self.elevator else "",
            "communityName": self.elevator.community.name if self.elevator and self.elevator.community else "",
        }


class RepairTracking(db.Model):
    __tablename__ = "repair_tracking"

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(160), nullable=False)
    handler = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(40), nullable=False)
    cost = db.Column(db.Float, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fault_id = db.Column(db.Integer, db.ForeignKey("fault_reports.id"), nullable=False)

    fault = db.relationship("FaultReport", back_populates="tracking_logs")

    def to_dict(self):
        return {
            "id": self.id,
            "action": self.action,
            "handler": self.handler,
            "status": self.status,
            "cost": self.cost,
            "createdAt": self.created_at.isoformat(timespec="minutes"),
            "faultId": self.fault_id,
        }


def parse_date(value):
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)
