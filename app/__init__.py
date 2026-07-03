from flask import Flask, jsonify
from app.core.errors import NotFoundError,ConflictError, ValidationError
from app.core.extensions import db , ma



def create_app():
    app = Flask(__name__)

    db.init_app(app)
    ma.init_app(app)

    
    from app.core.error_handlers import register_error_handlers
    register_error_handlers(app)

    
    return app
