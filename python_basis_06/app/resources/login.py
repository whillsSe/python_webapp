from app.resources import Resource,reqparse,Authentication,User,RefreshToken,bcrypt,create_access_token,create_refresh_token,jsonify,set_refresh_cookies,as_dict
class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('login_info')
    parser.add_argument('password')
    def post(self):
        data = Login.parser.parse_args()
        login_info = data['login_info']
        password = data['password']
        auth = None
        if '@' in login_info:
            auth = Authentication.find_by_email(login_info)
        else:
            user = User.find_by_user_id(login_info)
            if user:
                auth = user.auth
        
        if auth and bcrypt.check_password_hash(auth.password, password):
            uuid = auth.id#改めてdbに読み込みに行ってくれるのか、変数内に確保されてるものが返されるのか知りたい
            access_token = create_access_token(identity=uuid)
            refresh_token = create_refresh_token(identity=uuid)

            save_refresh_token = RefreshToken(refresh_token,uuid)
            save_refresh_token.save_to_db()

            user_dict = as_dict(auth.user)

            response = jsonify(message="Logged in successfully.",user=user_dict)
            response.headers['Authorization'] = 'Bearer {}'.format(access_token)

            set_refresh_cookies(response, refresh_token)

            return response