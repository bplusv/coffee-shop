import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))

db = SQLAlchemy()


def setup_db(app):
    """setup_db(app)
    binds a flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    """db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    """
    db.drop_all()
    db.create_all()


class Drink(db.Model):
    """Drink
    a persistent drink entity, extends the base SQLAlchemy Model
    """
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    recipe = Column(String(180), nullable=False)

    def short(self):
        """short form representation of the Drink model"""
        print(json.loads(self.recipe))
        short_recipe = [{'color': r['color'], 'parts': r['parts']}
                        for r in json.loads(self.recipe)]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    def long(self):
        """long()
        long form representation of the Drink model
        """
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    def insert(self):
        """insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """delete()
        deletes a new model into a database
        the model must exist in the database
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """update()
        updates a new model into a database
        the model must exist in the database
        """
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
