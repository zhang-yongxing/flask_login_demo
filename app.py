from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from util import uuid_32
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@127.0.0.1:5432/flask_login_user_demo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = '123456'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'
login_manager.init_app(app)


class User(db.Model, UserMixin):

    __tablename__ = 'user'

    # id
    id = db.Column(db.String(32), primary_key=True, default=uuid_32)
    # 用户账号
    username = db.Column(db.String(20), index=True)
    # 密码
    password = db.Column(db.String(20))
    # 被删除
    is_deleted = db.Column(db.Boolean, default=False)


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    user = User.query.get(user_id)
    print(user)
    if user:
        return user


@app.route('/registered', methods=['POST'])
def registered():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User(username=username,
                password=password)
    db.session.add(user)
    db.session.commit()
    return 'ok'


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter(User.username == username).first()
    if user is None:
        return 'error', 403
    if user.password != password:
        return 'error', 403
    login_user(user)
    return 'ok', 201


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return 'ok', 201


@app.route('/test')
@login_required
def test():
    print(22222)
    return 'ok', 200


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True, host='0.0.0.0')


