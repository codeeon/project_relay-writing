from flask_sqlalchemy import SQLAlchemy

import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, default=0)
    # artist = db.Column(db.String(100), nullable=False)
    # imag_url = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f'{self.username}'


# app.app_context()를 사용하여 애플리케이션 컨텍스트 설정
with app.app_context():
    db.create_all()


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # form에서 보낸 데이터 받아오기
        username_receive = request.form["username"]
        title_receive = request.form["title"]
        # artist_receive = request.form["artist"]
        # imag_url_receive = request.form["imag_url"]

        # 데이터를 DB에 저장하기
        # title=title_receive, artist=artist_receive, imag_url=imag_url_receive
        data = Song(username=username_receive, title=title_receive)
        db.session.add(data)
        db.session.commit()
        likes = db.Column(db.Integer, default=0)  # 좋아요 수를 저장하는 필드 추가
        # return redirect(url_for('/'))  # 저장 후 음악 목록 페이지로 이동

    song_list = Song.query.all()
    return render_template('index.html', song_list=song_list)


# @app.route('/')
# def music():
#     # 음악 목록 페이지 내용
#     song_list = Song.query.all()
#     return render_template('index.html', song_list=song_list)
@app.route("/edit/<int:song_id>", methods=['POST'])
def edit_song(song_id):
    if request.method == 'POST':
        song = Song.query.get(song_id)
        if song:
            song.title = request.form["title"]
            song.username = request.form["username"]
            db.session.commit()
    return redirect(url_for('home'))

@app.route("/delete/<int:song_id>", methods=['POST'])
def delete_song(song_id):
    song = Song.query.get(song_id)
    if song:
        db.session.delete(song)
        db.session.commit()
    return redirect(url_for('home'))

@app.route("/like/<int:song_id>", methods=["POST"])
def like(song_id):
    song = Song.query.get(song_id)
    if song:
        liked = request.json.get('liked')  # 클라이언트에서 보낸 현재 클릭 상태를 가져옵니다


        # 이전 클릭 상태가 좋아요이고, 현재 클릭 상태가 좋아요 취소이면 좋아요 수를 -1
        if not liked and song.likes > 0:
            song.likes -= 1
        # 이전 클릭 상태가 좋아요 취소이고, 현재 클릭 상태가 좋아요이면 좋아요 수를 +1
        elif liked:
            song.likes += 1

        db.session.commit()
        return jsonify(success=True, likes=song.likes)
    return jsonify(success=False)

if __name__ == "__main__":
    app.run(debug=True)
