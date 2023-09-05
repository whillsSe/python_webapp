from app.resources import Resource,reqparse,Authentication,User,jwt_required,get_jwt_identity,jsonify,as_dict

class UserResource(Resource):
    parser = reqparse.RequestParser()
    def get(self):
        UserResource.parser.add_argument('user_id',type=str,location='args')
        data = UserResource.parser.parse_args()
        target_id = data['user_id']
        user = User.find_by_user_id(target_id)
        user_dict = as_dict(user)
        return jsonify(message="Target user is found!",user=user_dict)

    @jwt_required()
    def post(self):
        UserResource.parser.add_argument('username',type=str,required=True)
        UserResource.parser.add_argument('user_id',type=str,required=True)
        current_user = get_jwt_identity()
        data = UserResource.parser.parse_args()

        if not Authentication.find_by_uuid(current_user):
            return jsonify(message="Something wrong in registering your account."),400
        
        if User.find_by_user_id(data['user_id']):
            return jsonify(message="Id you entered is already registered!"),400
        
        user = User(current_user,data['user_id'],data['username'])
        user.save_to_db()

        return jsonify(message="User-Info registered successfully!")
    
    @jwt_required()
    def put(self):
        UserResource.parser.add_argument('username',type=str,required=True)
        UserResource.parser.add_argument('user_id',type=str,required=True)
        current_user = get_jwt_identity()
        data = UserResource.parser.parse_args()
        auth = Authentication.find_by_uuid(current_user)

        if not auth:
            return jsonify(message=""),400
        
        if User.find_by_user_id(data['user_id']) and auth.user.user_id != data['user_id']:
            return jsonify(message="Id you entered is already registered!"),400
        
        user = Authentication.find_by_uuid(current_user).user
        user.user_id = data['user_id']
        user.username = data['username']
        user.save_to_db()

        return jsonify(message="User-Info updated successfully!")