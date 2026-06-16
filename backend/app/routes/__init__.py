from app.routes.catalog import bp as catalog_bp
from app.routes.maintenance import bp as maintenance_bp
from app.routes.repair import bp as repair_bp


def register_blueprints(app):
    app.register_blueprint(catalog_bp, url_prefix="/api")
    app.register_blueprint(maintenance_bp, url_prefix="/api")
    app.register_blueprint(repair_bp, url_prefix="/api")
