from flask import jsonify


class ConflictError(Exception):
    pass

class NotFoundError(Exception):
    pass

class ValidationError(Exception):
    pass


   