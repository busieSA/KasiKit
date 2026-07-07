from flask import Flask, jsonify
from app.core.errors import NotFoundError,ConflictError, ValidationError
from app.core.extensions import db , ma
from app.core.config import Config, DevelopmentConfig




def create_app():
    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    ma.init_app(app)

    
    from app.core.error_handlers import register_error_handlers
    register_error_handlers(app)

    with app.app_context():

        from app.website.routes import website_bp
        from app.portfolio.routes import portfolio_bp
        from app.dashboard.routes import dashboard_bp


        app.register_blueprint(website_bp)
        app.register_blueprint(portfolio_bp)
        app.register_blueprint(dashboard_bp)
        
    
    return app
