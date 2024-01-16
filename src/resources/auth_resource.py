from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token
from schemas.auth_schema import LoginSchema
from controllers.auth_controller import AuthController
from utils.role_mapping import RoleMapping

blp = Blueprint("authentication", __name__, description = "Authentication operations")

@blp.route("/login")
class Login(MethodView):

    @blp.arguments(LoginSchema)
    def post(self, credentials):
        auth_controller_obj = AuthController()
        role = auth_controller_obj.authenticate_user(credentials["username"], credentials["password"]).upper()
        get_mapped_role = RoleMapping.get_mapped_role(role)
        if role:
            access_token = create_access_token(identity=credentials["username"],additional_claims={"role": get_mapped_role})
            return {"message" : "User login successfully", "access_token" : access_token}, 200
        else:
            abort(401, message="Invalid login.")

