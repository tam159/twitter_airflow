from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.country import CountryModel


class CountrySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CountryModel
        include_relationships = True
        include_fk = True
        load_instance = True
