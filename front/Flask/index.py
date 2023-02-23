from pysl import getime
from tables import SQL_Init
from filter import Filter_Init
from utils import html_string as ht
from flask_bootstrap import Bootstrap
from utils import check_exception_time
from flask import request,url_for,render_template,jsonify

class Flask_Init():
    def __init__(self,app):
            
        Filter_Init(app)
        bootstrap=Bootstrap(app)
        
        sql=SQL_Init(app)
        db,tables=sql.db,sql.tables
        t_user,t_article=tables

        @app.route('/')
        def root():
            return ht.h(1,'This is homepage')

        @app.route('/favicon.ico')
        def favicon():
            return render_template('favicon.html')

        @app.route('/user/add')
        def add_user():
            name=request.args.get('name','user')
            pwd=request.args.get('pwd','123456')
            user=t_user(name=name,pwd=pwd)
            db.session.add(user)
            db.session.commit()
            return ht.h(1,'创建成功',"entry-header")

        @app.route('/user/query')
        def query_user():
            kw=request.args.get('kw','')
            # users=t_user.query.get('主键')
            if kw:
                users=t_user.query.filter(t_user.name.like(f'%{kw}%'))
            else:
                users=[]
            us=[]
            for user in users:
                us.append([user.id,user.name,user.pwd])
            return us

        @app.route('/user/update')
        def update_user():
            id=request.args.get('id',None)
            if id:
                try:
                    user=t_user.query.filter(t_user.id==id)[0]
                    user.pwd='11111'
                    db.session.commit()
                    return ht.h(1,'更新成功',"entry-header")
                except:
                    return ht.h(1,'id不存在',"entry-header")

        @app.route('/user/delete')
        def delete_user():
            id=request.args.get('id',None)
            if id:
                user=t_user.query.filter_by(id=id)[0]
                if user:
                    db.session.delete(user)
                    db.session.commit()
                    return ht.h(1,'注销成功',"entry-header")
                else:
                    return ht.h(1,'注销失败，id不存在',"entry-header")
            else:
                return ''

        @app.errorhandler(404)
        def non_existant_route(error):
            return ht.h(1,'No such page',"entry-header")
            # return errtemplate

        @app.route('/index/<int:i>')    
        # int string float path uuid any(a,b,c,d)
        def index(i):
            return f'index: {i}'

        @app.route('/args')
        def args():
            return request.args

        @app.route('/head')
        def head():
            return render_template('head.html',args=request.args,time=getime())


