"""Models for Cupcakes"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# consider a generic image url
GENERIC_URL = 'https://tinyurl.com/demo-cupcake' 

def connect_db(app):
    '''Connect to database '''
    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
    '''Cupcake model'''
    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False) # required
    size = db.Column(db.Text, nullable=False) # required
    rating = db.Column(db.Float, nullable=False) # required
    image = db.Column(db.Text, nullable=False, default=GENERIC_URL) # required
    

    def serialize(self):
        ''' Returns a dict representation of cupcake'''
        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
        }