from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.interest import InterestModel


class InterestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InterestModel
        include_relationships = True
        include_fk = True
        load_instance = True
        dump_only = ("id",)
