from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.age import AgeModel


class AgeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AgeModel
        include_relationships = True
        include_fk = True
        load_instance = True
