from app.resources import Resource,reqparse,Authentication,User,RefreshToken,bcrypt,create_access_token,create_refresh_token,jsonify,set_refresh_cookies,as_dict,get_jwt_identity,get_jti,jwt_required,get_jwt,verify_jwt_in_request
class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('login_info',required=True)
    parser.add_argument('password',required=True)
    parser.add_argument('authUpdateRequest',type=str,required=False)
    @jwt_required(optional=True,refresh=True)
    def post(self):
        data = Login.parser.parse_args()
        login_info = data['login_info']
        password = data['password']
        auth = None
        oldToken = get_jwt()
        if oldToken:
            print("Request has oldToken!")
            print(oldToken)
            token = RefreshToken.find_by_jti(oldToken.get("jti"))
            if token:
                token.is_active = False
                token.save_to_db()
        else:
            pass

        if '@' in login_info:
            auth = Authentication.find_by_email(login_info)
        else:
            user = User.find_by_user_id(login_info)
            if user:
                auth = user.auth
        
        if auth and bcrypt.check_password_hash(auth.password, password):
            uuid = auth.account_uuid 
            access_token = None
            if data['authUpdateRequest']:
                access_token = create_access_token(identity=uuid,additional_claims={"credentialUpdatePermission":"True"})
            else:
                access_token = create_access_token(identity=uuid)
            refresh_token = create_refresh_token(identity=uuid)

            save_refresh_token = RefreshToken(get_jti(refresh_token),uuid)
            save_refresh_token.save_to_db()

            user_dict = as_dict(auth.user)

            response = jsonify(message="Logged in successfully.",user=user_dict)
            response.headers['Authorization'] = 'Bearer {}'.format(access_token)

            set_refresh_cookies(response, refresh_token)

            return response
        else:
            return jsonify(message="Loggining info is wrong!")