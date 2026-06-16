from app.extensions import db


def commit(instance):
    db.session.add(instance)
    db.session.commit()
    return instance


def commit_all(instances):
    db.session.add_all(instances)
    db.session.commit()
    return instances
