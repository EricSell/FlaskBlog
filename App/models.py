# 模型

import datetime

from .exts import db

# 父-子栏目-文章中间表
article_column = db.Table('article_column',
                          db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
                          db.Column('column_id', db.Integer, db.ForeignKey('column.id'), primary_key=True),
                          )


# 栏目
class Column(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    column_name = db.Column(db.String(20))
    column_nickname = db.Column(db.String(20))
    column_content = db.Column(db.TEXT)
    # 子栏目
    c_column = db.Column(db.Integer)



# 文章-类型中间表
article_type = db.Table('article_type',
                        db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
                        db.Column('type_id', db.Integer, db.ForeignKey('type.id'), primary_key=True)
                        )


# 文章类型
class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(20))


# 文章
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_name = db.Column(db.String(25))
    article_content = db.Column(db.TEXT)
    article_time = db.Column(db.Date, default=datetime.datetime.now())
    pict = db.Column(db.String(255))
    readersum = db.Column(db.Integer,default=0)
    intro = db.Column(db.String(255))
    types = db.relationship('Type', backref='articles', secondary=article_type, lazy='dynamic')
    columns = db.relationship('Column', backref='articles', secondary=article_column, lazy='dynamic')
    commands = db.relationship('Command', backref='articles', lazy='dynamic')

# 用户
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(25))
    password = db.Column(db.String(25))
    content = db.Column(db.String(50))
    age = db.Column(db.Integer,default=0)
    icon = db.Column(db.String(255))
    loginsum = db.Column(db.Integer,default=0)
    logindate = db.Column(db.DateTime)
    IP = db.Column(db.String(50))
    is_super = db.Column(db.Boolean,default=False)
    photos = db.relationship('Photo',backref='users',lazy='dynamic')
    commands = db.relationship('Command',backref='user',lazy='dynamic')


# 评论
class Command(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    command = db.Column(db.Text)
    time = db.Column(db.DateTime,default=datetime.datetime.now())
    user_id = db.Column(db.Integer,db.ForeignKey(User.id))
    article_id = db.Column(db.Integer,db.ForeignKey(Article.id))

# 照片
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey(User.id))

