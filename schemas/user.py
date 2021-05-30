from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.user import UserModel


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        include_relationships = True
        include_fk = True
        load_instance = True
        dump_only = ("friends", "followers")
        load_only = ("friends", "followers")
