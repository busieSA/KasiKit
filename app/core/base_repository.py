from app.core.extensions import db

class BaseRepository:
    model = None

    def __init__(self, model):
        self.model = model

    def get_by_id(self, id):
        return self.model.query.get(id)
    
    def get_all(self):
        return self.model.query.all()
    
    def add(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity
    
    def delete(self, entity):
        db.session.delete(entity)
        db.session.commit()

    def commit(self, entity):
        db.session.commit()

    ## QUERY HELPERS

    def filter_by(self, **kwargs):
        return self.model.query.filter_by(**kwargs).all()
    
    def first_by(self, **kwargs):
        return self.model.query.filter_by(**kwargs).first()



    

        