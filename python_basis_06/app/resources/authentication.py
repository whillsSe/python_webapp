from app.resources import Resource,reqparse,Authentication,User,RefreshToken,bcrypt,create_access_token,create_refresh_token,jsonify,set_refresh_cookies

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

        save_refresh_token = RefreshToken(refresh_token,uuid)
        save_refresh_token.save_to_db()

        response = jsonify(message="User created successfully.")
        response.headers['Authorization'] = 'Bearer {}'.format(access_token)

        set_refresh_cookies(response, refresh_token)

        return response