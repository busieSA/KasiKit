from flask import jsonify
from app.core.errors import (
    NotFoundError,
    ConflictError,
    ValidationError
)


def register_error_handlers(app):

    @app.errorhandler(ConflictError)
    def handle_coflict(error):
        return jsonify({
            'success' : False,
            'message' : str(error)
        }),409
    
    @app.errorhandler(NotFoundError)
    def handle_not_found(error):
        return jsonify({
            'success' : False,
            'message' : str(error)
        }),404
    
    @app.errorhandler(Exception)
    def handle_generic(error):
        return jsonify({
            'success' : False,
            'message' : "Internal Error"
        }), 500
    
