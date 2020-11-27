from app import db, login, Config
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import jwt
from time import time


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


user_tag = db.Table('user_tag',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                    )


group_moderators = db.Table('group_moderators',
                              db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
                              db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                              )


invited_users = db.Table('invited_users',
                         db.Column('inviter', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                         db.Column('invited', db.Integer, db.ForeignKey('user.id'), primary_key=True))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tg_id = db.Column(db.Integer, index=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(100), index=True)
    phone = db.Column(db.String(18), index=True, unique=True)
    is_bot = db.Column(db.Boolean, index=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    additional_code = db.Column(db.String(64), index=True)
    language_code = db.Column(db.String(5), index=True, default='ru')
    password_hash = db.Column(db.String(128))
    status = db.Column(db.String(30), index=True, default='')
    role = db.Column(db.String(12), index=True)
    group = db.Column(db.Integer, db.ForeignKey('group.id'), index=True, default=1)
    registered = db.Column(db.DateTime, index=True, nullable=True, default=datetime.now())
    unsubscribed = db.Column(db.Boolean, default=False)
    available_tickets = db.Column(db.Integer, default=0)
    promo_codes = db.Column(db.JSON)
    his_invited_users = db.relationship('User',
                                        secondary=invited_users,
                                        primaryjoin=(invited_users.c.inviter == id),
                                        secondaryjoin=(invited_users.c.invited == id),
                                        backref=db.backref('inviter', lazy=True),
                                        lazy='dynamic')
    tags = db.relationship('Tag',
                           secondary=user_tag,
                           lazy='subquery',
                           backref=db.backref('tags', lazy=True))
    moderation_groups = db.relationship('Group',
                                        secondary=group_moderators,
                                        lazy='subquery',
                                        backref=db.backref('moderation_groups', lazy=True))
    user_moderators = db.relationship('User',
                                      secondary=group_moderators,
                                      lazy='subquery',
                                      backref=db.backref('my_moderators', lazy=True))

    def set_unsubscribed(self):
        self.unsubscribed = True
        db.session.commit()

    def set_subscribed(self):
        self.unsubscribed = False
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_group(self):
        if self.group:
            return Group.query.filter_by(id=self.group).first()

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {
                'reset_password': self.id,
                'exp': time() + expires_in
            },
            Config.SECRET_KEY,
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def set_item(self, item, value):
        if item in self.__dict__:
            setattr(self, item, value)
            db.session.commit()
        else:
            raise Exception('WrongItem')


    def __repr__(self):
        return f'{self.first_name}'


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), index=True)
    time_zone = db.Column(db.Integer, default=9)
    moderators = db.relationship('User',
                                 secondary=group_moderators,
                                 lazy='subquery',
                                 backref=db.backref('moderators', lazy=True))
    users = db.relationship('User', backref='users', lazy=True)

    def __repr__(self):
        return self.name


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), index=True)
    description = db.Column(db.String(128), index=True)
    users = db.relationship('User',
                              secondary=user_tag,
                              lazy='subquery',
                              backref=db.backref('tag_users', lazy=True))


class MainMenuItems(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(30))
    callback = db.Column(db.String(30))
    enabled = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, unique=True)
