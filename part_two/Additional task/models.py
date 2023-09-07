from mongoengine import *

connect(db="dz_8", host='mongodb+srv://Bogdan:gypsy_king21@bogdan.qbagtab.mongodb.net/?retryWrites=true&w=majority')


class Model(Document):
    fullname = StringField(required=True)
    email = StringField()
    boolean = BooleanField(default=False)
    phone = StringField()
    sms_or_email = StringField(choices=["sms", "email"])
    meta = {"collection": 'email'}
