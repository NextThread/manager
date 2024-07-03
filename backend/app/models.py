from app import db

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    date = db.Column(db.DateTime, index=True)
    transcription = db.Column(db.Text)

    def __repr__(self):
        return f'<Meeting {self.title}>'
