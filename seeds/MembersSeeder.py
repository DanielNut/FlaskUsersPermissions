from flask_seeder import Seeder, Faker, generator
from shared.models import db
from models.member import Member

# SQLAlchemy database model
# class Member(db.Model):
#     def __init__(self, id=None, name=None, permission_id=None):
#         self.id = id
#         self.name = name
#         self.permission_id = permission_id
#
#     def __str__(self):
#         return "ID=%d, Name=%s, Permission_id=%d" % (self.id, self.name, self.permission_id)


# All seeders inherit from Seeder
class DemoSeeder(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):
        # Create a new Faker and tell it how to create User objects
        faker = Faker(
            cls=Member,
            init={
                "id": generator.Sequence(),
                "name": generator.Name(),
                "permission_id": 1
                # generator.Integer(start=20, end=100)
            }
        )

        # Create 1 user
        for user in faker.create(1):
            print("Adding user: %s" % user)
            user.set_password('1234')
            self.db.session.add(user)
