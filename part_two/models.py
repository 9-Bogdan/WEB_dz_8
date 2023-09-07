from mongoengine import *

connect(db="dz_8", host='mongodb+srv://Bogdan:gypsy_king21@bogdan.qbagtab.mongodb.net/?retryWrites=true&w=majority')


class Model(Document):
    fullname = StringField()
    email = StringField()
    boolean = BooleanField(default=False)
    meta = {"collection": 'email'}
