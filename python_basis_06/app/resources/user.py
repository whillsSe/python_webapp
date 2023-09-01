from app.resources import Resource,reqparse,Authentication,User,jwt_required,get_jwt_identity,jsonify

class UserResource(Resource):
    parser = reqparse.RequestParser()
    def get(self):
        UserResource.parser.add_argument('user_id',type='str')

    @jwt_required()
    def post(self):
        UserResource.parser.add_argument('username',type='str',required=True)
        UserResource.parser.add_argument('user_id',type='str',required=True)
        current_user = get_jwt_identity()
        data = UserResource.parser.parse_args()

        if not Authentication.find_by_uuid(current_user):
            return jsonify(message="Something wrong in registering your account."),400
        
        if User.find_by_user_id(data['user_id']):
            return jsonify(message="Id you entered is already registered!"),400
        
        user = User(current_user,data['user_id'],data['username'])
        user.save_to_db()

        return jsonify(message="User-Info registered successfully!")