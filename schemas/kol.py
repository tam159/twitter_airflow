from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.kol import KolModel


class KolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = KolModel
        include_relationships = True
        include_fk = True
        load_instance = True
