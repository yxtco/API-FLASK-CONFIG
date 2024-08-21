from flask import Flask, request, jsonify, make_response
from datetime import datetime, timedelta
from functools import wraps
import jwt
from flask import Flask, jsonify, make_response, request
from data import verify_password, read_user_from_config, write_users_to_config, hash_password

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Jerry322123'


# 生成 JWT Token
def create_token(username):
    """
    为给定的用户名生成 JWT Token。

    参数:
        username (str): 用户名。

    返回:
        str: 生成的 JWT Token。
    """
    payload = {
        'name': username,
        'exp': datetime.utcnow() + timedelta(minutes = 30)
        }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm = "HS256")
    return token


# 装饰器用于验证 Token
def token_required(f):
    """
    用于保护路由的装饰器，验证 JWT Token 的有效性。
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return jsonify({'message': 'Token 缺失！'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms = ["HS256"])
            current_user = data['name']
        except:
            return jsonify({'message': 'Token 无效！'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# 注册端点
@app.route('/register', methods = ['POST'])
def register():
    """
    注册新用户。

    检查请求数据中的邮箱、密码和用户名是否有效。
    对密码进行哈希处理，并将用户添加到 users_data 字典中。
    返回成功消息及生成的 Token。
    """
    data = request.get_json()
    name = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # 验证邮箱
    if not email or '@' not in email:
        return jsonify({'message': '无效的邮箱'}), 400

    # 验证密码
    if not (6 <= len(password) <= 12) or not any(c.isupper() for c in password) or not any(
            c.isdigit() for c in password
            ):
        return jsonify({'message': '无效的密码'}), 400

    # 检查用户名是否已存在

    if read_user_from_config(name) is not None:  # 检查 user_data 是否为 None
        return jsonify({'message': '用户名已存在'}), 400
    # 对密码进行哈希处理

    # 更新 users_data 字典

    users_data = {
        'username': name,
        'password': hash_password(password),
        'email': email
        }
    users_data = {users_data['username']: users_data}
    print(users_data)

    # 将更新后的 users_data 字典保存回 data.py 文件
    write_users_to_config(users_data)

    # 生成并返回 Token
    token = create_token(name)
    response = make_response(jsonify({'message': '注册成功'}))
    response.headers['Authorization'] = token
    return response


# 登录端点
@app.route('/login', methods = ['POST'])
def login():
    """
    用户登录。

    验证用户提供的凭据或 Token 是否有效。
    成功后返回 Token 或者错误消息。
    """
    auth = request.authorization
    post_data = request.json
    print(post_data.get('username'), post_data.get('password'))

    # 首先检查请求头中是否有 Token
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        parts = auth_header.split(' ')
        if len(parts) == 2:
            token = parts[1]
        else:
            return jsonify({'message': '授权头格式不正确'}), 401

    if token:
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms = ["HS256"])
            current_user = data['name']

            # 如果 Token 有效，返回其过期时间及用户名
            expiration_time = data['exp']
            response = make_response(
                jsonify(
                    {
                        'message': 'Token 有效',
                        'username': current_user,
                        'expiration_time': expiration_time
                        }
                    )
                )
            response.headers['Authorization'] = token
            return response
        except:
            # 如果 Token 无效，继续验证用户名和密码
            pass
    # 检查用户是否存在
    name = post_data.get('username')
    user_data = read_user_from_config(name)
    print(user_data)
    if not user_data:
        return make_response('无法验证', 401, {'Authenticate': 'Basic realm="需要登录!"'})

    # 验证密码哈希
    if verify_password(post_data.get('password'), user_data['password']):
        token = create_token(name)

        # 创建带有新 Token 的响应
        response = make_response(
            jsonify(
                {
                    'message': '登录成功',
                    'username': name,
                    'token': token
                    }
                )
            )
        response.headers['Authorization'] = token
        return response
    else:
        return make_response('账户密码验证错误', 401, {'password': '密码错误'})


# Douyin 端点
@app.route('/douyin', methods = ['GET'])
@token_required
def douyin(current_user):
    """
    Douyin 端点，仅允许通过验证的用户访问。

    参数:
        current_user (str): 当前用户的用户名。

    返回:
        Response: 包含授权信息的响应。
    """
    token = create_token(current_user)
    response = make_response(jsonify({'message': '访问被授予'}))
    response.headers['Authorization'] = token
    return response


if __name__ == '__main__':
    app.run(debug = True)
