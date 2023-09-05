from app.resources import Resource,reqparse,Authentication,User,RefreshToken,bcrypt,create_access_token,create_refresh_token,jsonify,set_refresh_cookies,get_jti,jwt_required,get_jwt,get_jwt_identity

class AuthenticationResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',type=str,required=True,help="This field cannnot be blank.")
    parser.add_argument('password',type=str,required=True,help="This field cannnot be blank.")

    def post(self):
        data = AuthenticationResource.parser.parse_args()
        if Authentication.find_by_email(data['email']):
            return {"message":"A user with that email already exists"},400

        auth = Authentication(data["email"],bcrypt.generate_password_hash(data["password"]).decode("utf-8"))
        auth.save_to_db()

        uuid = auth.account_uuid #改めてdbに読み込みに行ってくれるのか、変数内に確保されてるものが返されるのか知りたい
        access_token = create_access_token(identity=uuid)
        refresh_token = create_refresh_token(identity=uuid)

        save_refresh_token = RefreshToken(get_jti(refresh_token),uuid)
        save_refresh_token.save_to_db()

        response = jsonify(message="User created successfully.")
        response.headers['Authorization'] = 'Bearer {}'.format(access_token)

        set_refresh_cookies(response, refresh_token)

        return response
    
    @jwt_required(refresh=False)
    def put(self):
        data = AuthenticationResource.parser.parse_args()
        token = get_jwt()
        print(token)
        auth = Authentication.find_by_uuid(get_jwt_identity())
        if not token['credentialUpdatePermission']:
            return {"message":"Invalid Access!"},400

        if Authentication.find_by_email(data['email']) and auth.email != data['email']:
            return {"message":"A user with that email already exists"},400

        auth.email = data["email"]
        auth.password = data["password"]
        auth.save_to_db()

        uuid = auth.account_uuid #改めてdbに読み込みに行ってくれるのか、変数内に確保されてるものが返されるのか知りたい
        access_token = create_access_token(identity=uuid)
        refresh_token = create_refresh_token(identity=uuid)

        RefreshToken.disable_tokens_by_uuid(uuid)

        save_refresh_token = RefreshToken(get_jti(refresh_token),uuid)
        save_refresh_token.save_to_db()

        response = jsonify(message="Authentication Info is updated successfully.")
        response.headers['Authorization'] = 'Bearer {}'.format(access_token)

        set_refresh_cookies(response, refresh_token)

        return response

