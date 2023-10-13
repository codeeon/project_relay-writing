from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
import re

# 플라스크 서버
app = Flask(__name__)

# form key
app.config['SECRET_KEY'] = 'flask'

# db 생성
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relay.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# db 테이블 생성
# User


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    # Contents의 author에 접근한다.
    posts = relationship("Contents", back_populates="author")

    # Comment의 comment author에 접근한다.
    comments = relationship("Comment", back_populates="comment_author")

# Contents


class Contents(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key를 users.id로 지정한다. users는 User 테이블을 참조한다.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # User를 참조하는 관계를 지정한다.
    author = relationship("User", back_populates="posts")

    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # Comment와의 관계 지정
    comments = relationship("Comment", back_populates="parent_post")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key를 User 테이블의 users id로 생성한다.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # User를 를 참조하는 관계를 지정한다.
    comment_author = relationship("User", back_populates="comments")

    # Foreign Key = Contents.id
    post_id = db.Column(db.Integer, db.ForeignKey("contents.id"))
    # Contents와 관계
    parent_post = relationship("Contents", back_populates="comments")

    text = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()

# flask 로그인 매니저 생성
login_manager = LoginManager()
login_manager.init_app(app)

# key를 기반으로 로그인


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
@app.route('/register', methods=["GET", "POST"])
def register():
    # POST 요청일 경우 새로운 회원으로 등록
    if request.method == "POST":
        new_user = User(
            id_user=request.form.get('id_user'),
            name=request.form.get('name'),
            # password 해싱하기
            # hashing 함수 : pbkdf2:sha256
            # salt 길이 : 8
            password=generate_password_hash(password=request.form.get(
                'password'), method='pbkdf2:sha256', salt_length=8)
        )

        # db에 이미 등록된 아이디인 경우 로그인 페이지로 이동하기
        # filter_by로 아이디을 찾기
        # first() : 첫번째로 매칭되는 값 가져오기
        if len(new_user.name) == 0:
            print('힝')
        if User.query.filter_by(id_user=request.form.get('id_user')).first():
            flash("존재하는 아이디입니다. 로그인으로 이동합니다.")  # 에러 메세지 (임시)
            return redirect(url_for('login'))  # 로그인 페이지로 이동

        # 새로운 유저일경우 등록
        else:
            db.session.add(new_user)  # db 추가
            db.session.commit()  # db에 커밋

            # 새로운 유저 로그인 검증
            login_user(new_user)  # flask login - 로그인 실행

            # 회원가입 완료 시 로그인되어 메인페이지로 이동
            return redirect(url_for('main'))
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    # POST 요청 시 로그인 시작
    if request.method == "POST":
        id_user = request.form.get('id_user')
        password = request.form.get('password')
        # 등록되어 있는 아이디로 db찾기
        # filter_by로 아이디을 찾기
        # first() : 첫번째로 매칭되는 값 가져오기
        user = User.query.filter_by(id_user=id_user).first()
        print(user)
        # user정보가 없는 경우
        if not user:
            flash("등록된 아이디가 존재하지 않습니다.")  # 에러메세지
            return redirect(url_for('login'))  # 로그인 페이지로 이동
        # 비밀번호가 일치하지 않는 경우
        elif not check_password_hash(user.password, password):
            flash("비밀번호가 일치하지 않습니다.")
        # 로그인
        else:
            login_user(user)
            return redirect(url_for('main'))

    return render_template('login.html')

# 로그아웃


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# 나중에 인증할때 사용 가능


@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)
    return render_template("secrets.html", name=current_user.name)

# 메인페이지


@app.route('/')
def main():
    return render_template('main.html', logged_in=current_user.is_authenticated)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
