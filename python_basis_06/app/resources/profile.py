from app.resources import Resource,reqparse,Authentication,User,RefreshToken,bcrypt,jsonify,as_dict

class ProfileResource(Resource):
    parser = reqparse.RequestParser()

    def get(self):
        ProfileResource.parser.add_argument('user_id')
        data = ProfileResource.parser.parse_args()
        user_id = data['user_id']
        user = User.find_by_user_id(user_id)
        user_dict = as_dict(user)
        user_dict['profile'] = as_dict(user.prof)
        return jsonify(user_dict)
    
    def post(self):
        ProfileResource.parser.add_argument()