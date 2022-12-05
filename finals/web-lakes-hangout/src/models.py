from . import db

class Post(db.Model):
    post_id = db.Column(db.Text(), primary_key=True)
    author = db.Column(db.Text())
    title = db.Column(db.Text())
    body = db.Column(db.Text())
    deleted = db.Column(db.Text())
    ts = db.Column(db.Text())

