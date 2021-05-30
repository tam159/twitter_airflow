from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.city import CityModel


class CitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CityModel
        include_relationships = True
        include_fk = True
        load_instance = True
