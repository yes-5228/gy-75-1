from app.models import Community, Elevator


def list_communities():
    return [item.to_dict() for item in Community.query.order_by(Community.name).all()]


def list_elevators():
    return [item.to_dict() for item in Elevator.query.order_by(Elevator.code).all()]
