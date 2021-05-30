from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.user_stat import UserStatModel


class UserStatSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserStatModel
        include_relationships = True
        include_fk = True
        load_instance = True
