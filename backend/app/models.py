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
    is_out_of_service = db.Column(db.Boolean, default=False, nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id"), nullable=False)

    community = db.relationship("Community", back_populates="elevators")
    outage_records = db.relationship(
        "OutageRecord",
        back_populates="elevator",
        cascade="all, delete-orphan",
        order_by="OutageRecord.start_time.desc()",
    )

    @property
    def active_outage(self):
        return next(
            (record for record in self.outage_records if record.end_time is None),
            None,
        )

    def to_dict(self):
        active_outage = self.active_outage
        return {
            "id": self.id,
            "code": self.code,
            "building": self.building,
            "unit": self.unit,
            "brand": self.brand,
            "status": self.status,
            "isOutOfService": self.is_out_of_service,
            "communityId": self.community_id,
            "communityName": self.community.name if self.community else "",
            "activeOutage": active_outage.to_dict() if active_outage else None,
        }


class OutageRecord(db.Model):
    __tablename__ = "outage_records"

    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(200), nullable=False)
    reason_type = db.Column(db.String(40), default="Fault", nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expected_recovery_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    operator = db.Column(db.String(80), nullable=False)
    notes = db.Column(db.Text, default="", nullable=False)
    previous_status = db.Column(db.String(40), nullable=True)
    elevator_id = db.Column(db.Integer, db.ForeignKey("elevators.id"), nullable=False)

    elevator = db.relationship("Elevator", back_populates="outage_records")

    def to_dict(self):
        return {
            "id": self.id,
            "reason": self.reason,
            "reasonType": self.reason_type,
            "startTime": self.start_time.isoformat(timespec="minutes") if self.start_time else None,
            "expectedRecoveryTime": self.expected_recovery_time.isoformat(timespec="minutes") if self.expected_recovery_time else None,
            "endTime": self.end_time.isoformat(timespec="minutes") if self.end_time else None,
            "operator": self.operator,
            "notes": self.notes,
            "previousStatus": self.previous_status,
            "elevatorId": self.elevator_id,
            "elevatorCode": self.elevator.code if self.elevator else "",
            "communityName": self.elevator.community.name if self.elevator and self.elevator.community else "",
            "isActive": self.end_time is None,
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
            "elevatorOutOfService": self.elevator.is_out_of_service if self.elevator else False,
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
            "elevatorOutOfService": self.elevator.is_out_of_service if self.elevator else False,
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
            "elevatorOutOfService": self.elevator.is_out_of_service if self.elevator else False,
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
