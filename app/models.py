from . import db


class Site(db.Model):
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(128), unique=True, nullable=False)

    analyses = db.relationship('Analysis', backref='site', lazy='dynamic')
    votes = db.relationship('Vote', backref='site', lazy='dynamic')

    @property
    def average_rating(self):
        votes = self.votes.all()
        if len(votes) > 0:
            return sum([v.rating for v in votes]) / len(votes)
        return 0

    @property
    def number_of_votes(self):
        return len(self.votes.all())


class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Time, nullable=False)

    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))


class Analysis(db.Model):
    __tablename__ = 'analyses'

    id = db.Column(db.Integer, primary_key=True)
    negativity = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Time, nullable=False)

    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
