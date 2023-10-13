from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
import re
import os

# 플라스크 서버
app = Flask(__name__)

# form key
app.config['SECRET_KEY'] = 'flask'

# db 생성
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relay.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# db 테이블 생성
# User db
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    # Contents의 author에 접근한다.
    posts = relationship("Content", back_populates="author")

    # Comment의 comment author에 접근한다.
    comments = relationship("Comment", back_populates="comment_author")

# Content
class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key를 users.id로 지정한다. users는 User 테이블을 참조한다.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # User를 참조하는 관계를 지정한다.
    author = relationship("User", back_populates="posts")

    title = db.Column(db.String(250), unique=True, nullable=False)
    # date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # Comment와의 관계 지정
    comments = relationship("Comment", back_populates="parent_post")

    def __repr__(self):
        return f'{self.title} {self.body} {self.author}'


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key를 User 테이블의 users id로 생성한다.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # User를 를 참조하는 관계를 지정한다.
    comment_author = relationship("User", back_populates="comments")

    # Foreign Key = Content.id
    post_id = db.Column(db.Integer, db.ForeignKey("contents.id"))
    # Contents와 관계
    parent_post = relationship("Content", back_populates="comments")
    likes = db.Column(db.Integer)
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

# 회원가입 페이지
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
        if User.query.filter_by(id_user=request.form.get('id_user')).first():
            flash("존재하는 아이디입니다. 로그인으로 이동합니다.")  # 에러 메세지 (임시)
            return redirect(url_for('login'))  # 로그인 페이지로 이동

        # 새로운 유저일경우 등록
        else:
            db.session.add(new_user)  # db 추가
            db.session.commit()  # db에 커밋
            login_user(new_user)  # flask login - 로그인 실행
            # 회원가입 완료 시 로그인되어 메인페이지로 이동
            return redirect(url_for('contents'))
    return render_template('register.html')

# 로그인 페이지
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
        
        # user정보가 없는 경우
        if not user:
            flash("등록된 아이디가 존재하지 않습니다.")
              # 에러메세지
            return redirect(url_for('login'))  # 로그인 페이지로 이동
        
        # check_password_hash : 입력한 패스워드를 해싱한 후 db에 저장되어있는 해싱된 패스워드와 비교
        # 비밀번호가 일치하지 않는 경우
        elif not check_password_hash(user.password, password):
            flash("비밀번호가 일치하지 않습니다.")
        
        # 로그인
        else:
            login_user(user)
            return redirect(url_for('contents'))

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
@app.route('/contents')
def contents():
    if not current_user.is_authenticated :
        redirect(url_for('login'))
    contents_list = Content.query.all()
    return render_template('contents.html', data=contents_list, logged_in=current_user.is_authenticated)

# 새 이야기 만들기
@app.route("/contents/create/", methods=["GET", "POST"])
def contents_create():
        # form get 받아오기
        title_receive = request.form.get("title")
        body_receive = request.form.get("body")
        image_receive = request.form.get("img_url")
        # db 생성
        new_contents = Content(
            title = title_receive,
            body = body_receive,
            img_url = image_receive,
            author = current_user
        )
        
        # 데이터를 DB에 저장하기
        # contents = Content(title=title_receive, body=body_receive, img_url=image_receive)
        db.session.add(new_contents)
        db.session.commit()
        return redirect(url_for('contents'))

# 이야기 지우기
@app.route('/contents/delete/<int:contents_id>', methods=['POST'])
def delete_contents(contents_id):
    contents = Content.query.get(contents_id)
    if contents:
        db.session.delete(contents)
        db.session.commit()
    return redirect(url_for('contents'))


# comment 페이지
@app.route("/comments/<int:contents_id>", methods=['GET', 'POST']) # url 이게 맞나 ??
def comments(contents_id):
    if request.method == 'POST':
        # form에서 보낸 데이터 받아오기
        # username_receive = request.form["username"]
        requested_content = Content.query.get(contents_id)
        title_receive = request.form("title")
        new_comments = Comment(
            parent_post = requested_content,
            comments_author = current_user,
            text = title_receive,
            likes = 0
        )
        # data = Comment(username=username_receive, title=title_receive)
        db.session.add(new_comments)
        db.session.commit()
        # likes = db.Column(db.Integer, default=0)  # 좋아요 수를 저장하는 필드 추가
        return redirect(url_for('comments/<int:contents_id>'))

    comments_list = Comment.query.all()
    return render_template('conmments.html', comments_list=comments_list)

@app.route("/edit/<int:contents_id>", methods=['POST'])
def edit_comments(contents_id):
    if request.method == 'POST':
        comments = Comment.query.get(contents_id)
        if comments:
            comments.title = request.form["title"]
            comments.username = request.form["username"]
            db.session.commit()
    return redirect(url_for('comments'))

@app.route("/delete/<int:contents_id>", methods=['POST'])
def delete_comments(contents_id):
    comments = Comment.query.get(contents_id)
    if comments:
        db.session.delete(comments)
        db.session.commit()
    return redirect(url_for('comments'))

@app.route("/like/<int:contents_id>", methods=["POST"])
def like(contents_id):
    comments = Comment.query.get(contents_id)
    if comments:
        liked = request.json.get('liked')  # 클라이언트에서 보낸 현재 클릭 상태를 가져옵니다

        # 이전 클릭 상태가 좋아요이고, 현재 클릭 상태가 좋아요 취소이면 좋아요 수를 -1
        if not liked and comments.likes > 0:
            comments.likes -= 1
        # 이전 클릭 상태가 좋아요 취소이고, 현재 클릭 상태가 좋아요이면 좋아요 수를 +1
        elif liked:
            comments.likes += 1

        db.session.commit()
        return jsonify(success=True, likes=comments.likes)
    return jsonify(success=False)


if __name__ == '__main__':
    app.run(port=3000, debug=True)