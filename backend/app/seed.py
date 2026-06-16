from datetime import date, timedelta

from app.extensions import db
from app.models import Community, Elevator, FaultReport, InspectionRecord, MaintenancePlan, RepairTracking


def seed_data():
    if Community.query.count():
        return

    community = Community(
        name="Riverside Garden",
        address="88 Lake Road",
        manager="Mia Zhou",
        phone="13800001111",
    )
    elevators = [
        Elevator(code="BJ-A1-01", building="A1", unit="Unit 1", brand="KONE", status="Normal", community=community),
        Elevator(code="BJ-B2-02", building="B2", unit="Unit 2", brand="Hitachi", status="Under Repair", community=community),
        Elevator(code="BJ-C3-01", building="C3", unit="Unit 1", brand="Mitsubishi", status="Normal", community=community),
    ]
    db.session.add(community)
    db.session.add_all(elevators)
    db.session.flush()

    db.session.add_all(
        [
            MaintenancePlan(
                title="Semi-monthly Maintenance",
                plan_type="Semi-monthly",
                scheduled_date=date.today() + timedelta(days=2),
                assignee="Engineer Li",
                status="Pending",
                notes="Check door motor, traction wheel, and emergency intercom.",
                elevator=elevators[0],
            ),
            MaintenancePlan(
                title="Quarterly Safety Review",
                plan_type="Quarterly",
                scheduled_date=date.today() + timedelta(days=9),
                assignee="Engineer Chen",
                status="Scheduled",
                notes="Update offline maintenance archive after inspection.",
                elevator=elevators[1],
            ),
            InspectionRecord(
                inspector="Inspector Wang",
                result="Normal",
                checklist="Machine room temperature, cabin lighting, and door lock circuit are normal.",
                attachment_url="https://example.com/inspection/bj-a1-01.jpg",
                elevator=elevators[0],
            ),
        ]
    )
    fault = FaultReport(
        reporter="Property Desk",
        phone="0571-88889999",
        fault_type="Abnormal Noise",
        description="B2 Unit 2 makes a rubbing noise while moving upward.",
        priority="Urgent",
        status="In Progress",
        elevator=elevators[1],
    )
    db.session.add(fault)
    db.session.flush()
    db.session.add(
        RepairTracking(
            action="Engineer arrived and found likely door slider wear.",
            handler="Engineer Zhao",
            status="In Progress",
            cost=120,
            fault=fault,
        )
    )
    db.session.commit()
