from app.extensions import marshmallow as ma
from app.models import Person, Address

class AddressessSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Address
        include_fk = True

class PersonsSchema(ma.SQLAlchemyAutoSchema):

    addresses = ma.Nested(AddressessSchema, many=True)

    class Meta:
        model = Person
        include_fk = True

class MunicipeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Address
        fields = ("municipe",)
        include_fk = False