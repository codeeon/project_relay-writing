# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
# DB 기본 코드
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class Main(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    first_text = db.Column(db.String(1000), nullable=False)
    image_url = db.Column(db.String(10000), nullable=False)
    username = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'{self.title} {self.first_text}' # {self.username}

with app.app_context():
    db.create_all()


@app.route("/main/")
def main():
    main_list = Main.query.all()
    return render_template('main.html', data=main_list)

@app.route("/main/<username>/")
def render_main_filter(username):
    filter_list = Main.query.filter_by(username=username).all()
    return render_template('main.html', data=filter_list)

@app.route("/main/create/")
def main_create():
    #form에서 보낸 데이터 받아오기
    username_receive = request.args.get("username")
    title_receive = request.args.get("title")
    first_text_receive = request.args.get("first_text")
    image_receive = request.args.get("image_url")

    # 데이터를 DB에 저장하기
    main = Main(username=username_receive, title=title_receive, first_text=first_text_receive, image_url=image_receive)
    db.session.add(main)
    db.session.commit()
    return redirect(url_for('render_main_filter', username=username_receive))

@app.route('/main/delete/<int:main_id>', methods=['POST'])
def delete_main(main_id):
    main = Main.query.get(main_id)
    if main:
        db.session.delete(main)
        db.session.commit()
    return redirect(url_for('main'))

if __name__ == "__main__":
    app.run(debug=True)