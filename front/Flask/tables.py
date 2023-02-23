import typing
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


class SQL_Init():
    def __init__(self,app):

        db=SQLAlchemy(app)
        self.db=db
        migrate=Migrate(app,db)
        # flask db init
        # flask db migrate
        # flask db update 

        class t_user(db.Model):
            __tablename__='user'
            id=db.Column(db.Integer,primary_key=True,autoincrement=True)
            # varchar
            name=db.Column(db.String(100),nullable=False)
            pwd=db.Column(db.String(100),nullable=False)

            #articles backref feom table article

        class t_article(db.Model):
            __tablename__='article'
            id=db.Column(db.Integer,primary_key=True,autoincrement=True)
            title=db.Column(db.String(100),nullable=False)
            content=db.Column(db.Text,nullable=False)

            author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
            author=db.relationship('t_user',backref='articles')
            #                               back_ref='articles'

        # with app.app_context():
        #     # db.delete(table_user)
        #     db.create_all()

        self.tables=[t_user,t_article]

    def db(self) -> SQLAlchemy:
        return self.db

