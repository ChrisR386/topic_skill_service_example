from db import db

class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    skills = db.relationship("Skill", backref="topic", lazy=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name}

class Skill(db.Model):
    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "topic_id": self.topic_id}