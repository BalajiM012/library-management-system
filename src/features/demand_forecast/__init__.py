from flask import Blueprint

from .api import demand_forecast_bp

def register_blueprints(app):
    app.register_blueprint(demand_forecast_bp)
