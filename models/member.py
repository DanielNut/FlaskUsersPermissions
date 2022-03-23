from shared.models import db
from werkzeug.security import generate_password_hash, check_password_hash


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    psw_hash = db.Column(db.String(500), nullable=True)

    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))

    # def __repr__(self):
    #     return {"id": self.id, "name": self.name, "psw_hash": self.psw_hash}

    def set_password(self, password):
        self.psw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.psw_hash, password)
