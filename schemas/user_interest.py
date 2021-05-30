from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.user_interest import UserInterestModel


class UserInterestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserInterestModel
        include_relationships = True
        include_fk = True
        load_instance = True
