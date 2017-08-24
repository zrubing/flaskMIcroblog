from app import db
from hashlib import md5


followers=db.Table('followers',
                   db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),
                   db.Column('followed_id',db.Integer,db.ForeignKey('user.id'))
)


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nickname=db.Column(db.String(64),index=True,unique=True)
    email=db.Column(db.String(120),index=True,unique=True)
    posts=db.relationship('Post',backref='author',lazy='dynamic')

    about_me=db.Column(db.String(140))
    last_seen=db.Column(db.DateTime)

    followed=db.relationship('User',
                             secondary=followers,
                             primaryjoin=(followers.c.follower_id==id),
                             secondaryjoin=(followers.c.followed_id==id),
                             backref=db.backref('followers',lazy='dynamic'),
                             lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def is_active(self):
        return True
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        try:
            return unicode(self.id) #python 2
        except NameError:
            return str(self.id) #python3
    def avatar(self,size):
        return 'http://www.gravatar.com/avatar/'\
            +md5(self.email.encode('utf-8')).hexdigest()+'?d=mm&s='+str(size)

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first()==None:
            return nickname
        else:
            version=2
            while True:
                new_nickname=nickname+str(version)
                hasName=User.query.filter_by\
                         (nickname=new_nickname).first()!=None
                if not hasName:
                    return new_nickname
                else:
                    version+=1
    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)
            return self
    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id==user.id).count()>0

    def followed_posts(self):
        return Post.query.join(followers,\
                               (followers.c.followed_id==Post.user_id))\
                         .filter(followers.c.follower_id==self.id)\
                         .order_by(Post.timestamp.desc())

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.String(140),index=True,unique=True)
    timestamp=db.Column(db.DateTime)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body + '-'+str(self.id))
