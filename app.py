# -*- coding: utf-8 -*-

import click
from flask import Flask
from flask import request
from apps.llm import chat_gpt 
from apps.services import UserService

from apps.model.User import UserModel
from apps.database import db
from apps.config import get_config
from apps.database import init_db

app = Flask(__name__)
cfg = get_config()

app.config["SQLALCHEMY_DATABASE_URI"] = cfg.SQLALCHEMY_DATABASE_URI

init_db(app)

def new_user():
        
    user = UserModel("test","local","skygram@163.com")
    db.session.add(user)
    db.session.commit()
    print("create new user")
    return


#发送消息给openapi
@app.route('/')
def  send_message():

    # new_user()

    response = chat_gpt.send_message("你好啊")
    print("receive response = ",response)
    return '<h1>' +  response + '</h1>'

@app.route('/', methods = ["POST"])
def post_data():
    print("post data")
    #{"obj": [{"name":"John","age":"20"}] }
    
    # 方法一
    data = request.get_json()                # 获取 JSON 数据
    data = pd.DataFrame(data["obj"])   # 获取参数并转变为 DataFrame 结构
    
    # 方法二
    # data = request.json        # 获取 JOSN 数据
    # data = data.get('obj')     #  以字典形式获取参数
    
    # 经过处理之后得到要传回的数据
    res = some_function(data)
    
    # 将 DataFrame  数据再次打包为 JSON 并传回
    # 方法一
    res = '{{"obj": {} }}'.format(res.to_json(orient = "records", force_ascii = False))
    # 方法二
    # res = jsonify({"obj":res.to_json(orient = "records", force_ascii = False)})
    
    return '<h1>post data</h1>'


# bind multiple URL for one view function
@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello, Flask!</h1>'


# dynamic route, URL variable default
@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name

# custom flask cli command
@app.cli.command()
def hello():
    """Just say hello."""
    click.echo('Hello, Human!')


if __name__ == '__main__': 
   app.run()