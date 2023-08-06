from flask import Blueprint, render_template, request, redirect, session, url_for
from utah.arches.webtools import validate_field
from datetime import datetime
from utah.core.utilities import get_service_object, string_to_date
from utah.core.utilities import date_to_string
from utah.core.authentication import BaseAuthenticationService
from utah.core.authentication import AuthenticationInfo
from utah.core.utilities import Sendmail
from utah.core.authentication import AuthenticationInfo
from utah.core.authentication import AuthenticationToken
from utah.core.profile import BaseProfileService
from utah.core.profile import ProfileInfo
from utah.core.authorize import Group
from utah.core.authorize import BaseGroupService
from utah.core.authorize import DuplicateGroupException
from utah.core.authorize import NoSuchGroupException
from utah.core.authorize import BaseURIAuthorizationService
from utah.core.authorize import URIAccessRight
from utah.core.authorize import DuplicateRight
from utah.arches.webtools import uri_authorized
from utah.arches.webtools import get_user_id
from flask_restful import Resource, Api
from flask_babel import gettext
import json
import pytz

from utah.arches.webtools import URIUSE_ANY
from utah.arches.webtools import URIUSE_SESSION_ONLY
from utah.arches.webtools import URIUSE_TOKEN_ONLY


errors = {
    'UnauthorizedException': {
        'message': gettext("User Not logged in"),
        'status': 401
    },
    'ForbiddenException': {
        'message': gettext("Authorization Error"),
        'status': 403
    }
}

app = Blueprint('login', __name__, url_prefix="/security")
api = Api(app, errors=errors)


authentication_service:BaseAuthenticationService = get_service_object("authentication")
profile_service:BaseProfileService = get_service_object("profile")
group_service:BaseGroupService = get_service_object("group_service")
uri_access_rights_service:BaseURIAuthorizationService = get_service_object("uri_authorization")

account_verify_sendmail = None
if authentication_service.is_account_verification_required():
    account_verify_sendmail:Sendmail = get_service_object("account_verify_sendmail")



class Profile(Resource):
    @uri_authorized(URIUSE_ANY)
    def get(self):
        profile = profile_service.get_profile_info(get_user_id())
        ret_dict = {"user_id" : profile.user_id,
                    "first_name" : profile.first_name,
                    "last_name" : profile.last_name,
                    "timezone" : profile.timezone
                    }
        return ret_dict
    @uri_authorized(URIUSE_ANY)
    def post(self):
        posted_profile = json.loads(request.data)

        profile = profile_service.get_profile_info(get_user_id())
        profile.last_name = posted_profile["last_name"]
        profile.first_name = posted_profile["first_name"]
        profile.timezone = posted_profile["timezone"]
        profile_service.update_profile_info(profile)

        session["timezone"] = profile.timezone

        return {"status" : "OK"}


class AuthenticationTokens(Resource):
    @uri_authorized(URIUSE_ANY)
    def get(self):
        at_results = []
        ai:AuthenticationInfo = authentication_service.get_authentication_info(get_user_id())
        for at in ai.authentication_tokens:
            at_results.append( { "description": at.description, "key": at.key, "expire_date": date_to_string(at.expire_date) } )

        return at_results


    @uri_authorized(URIUSE_ANY)
    def post(self):
        posted_token_info = json.loads(request.data)
        ai:AuthenticationInfo = authentication_service.get_authentication_info(get_user_id())
        new_token:AuthenticationToken = ai.create_token(posted_token_info["description"], string_to_date(posted_token_info["expire_date"]))
        authentication_service.write_authentication_info(ai)

        return {"description": new_token.description, "expire_date": date_to_string(new_token.expire_date), "key": new_token.key}



class AuthenticationToken(Resource):
    @uri_authorized(URIUSE_ANY)
    def get(self, key):
        ret_value = None
        ai:AuthenticationInfo = authentication_service.get_authentication_info(get_user_id())
        for at in ai.authentication_tokens:
            if at.key == key:
                ret_value = { "description": at.description, "key": at.key, "expire_date": date_to_string(at.expire_date) }

        return ret_value


    @uri_authorized(URIUSE_ANY)
    def delete(self, key):
        ret_value = None
        ai:AuthenticationInfo = authentication_service.get_authentication_info(get_user_id())
        i=0
        for at in ai.authentication_tokens:
            if at.key == key:
                del ai.authentication_tokens[i]
                authentication_service.write_authentication_info(ai)

            i=i+1

        return ret_value


    @uri_authorized(URIUSE_ANY)
    def put(self, key):
        put_token_info = json.loads(request.data)

        ai:AuthenticationInfo = authentication_service.get_authentication_info(get_user_id())
        i=0
        for at in ai.authentication_tokens:
            if at.key == key:
                at.description = put_token_info["description"]
                at.expire_date =  string_to_date(put_token_info["expire_date"])
                authentication_service.write_authentication_info(ai)
                break

            i=i+1


class Timezones(Resource):
    @uri_authorized(URIUSE_ANY)
    def get(self):
        return pytz.all_timezones



api.add_resource(Profile, '/api/profile')
api.add_resource(Timezones, '/api/timezones')
api.add_resource(AuthenticationTokens, '/api/authentication_tokens')
api.add_resource(AuthenticationToken, '/api/authentication_tokens/<key>')


class SelectedGroup(Group):
    def __init__(self, group:Group, selected:bool):
        super().__init__(group.name, group.description)
        self.selected = selected

class EnrolledProfileInfo(ProfileInfo):
    def __init__(self, profile:ProfileInfo, groups:list):
        super().__init__(profile.user_id, profile.email_address, profile.first_name, profile.last_name)
        self.groups = groups

class SelectableItem():
    def __init__(self, value, description, selected):
        self.value = value
        self.description = description
        self.selected = selected

class AccessRightBean():
    raw_methods = ["GET","POST","PUT","DELETE"]
    def __init__(self, uri_access_right, available_groups, available_filter_uris):
        self.right_name = uri_access_right.right_name
        self.uri = uri_access_right.uri
        self.methods = self.build_selectable_list(uri_access_right.methods, AccessRightBean.raw_methods)
        self.filters = self.build_selectable_list(uri_access_right.filters, available_filter_uris)
        self.groups = self.build_selectable_list(uri_access_right.authorized_groups, available_groups)


    def build_selectable_list(self, selected_items, all_items):
        ret_list = []
        for raw_item in all_items:
            selected = False
            if raw_item in selected_items:
                selected = True

            ret_list.append(SelectableItem(raw_item, raw_item, selected))

        return ret_list



@app.after_request
def after_request_func(response):
    response.headers["Cache-Control"] = "no-cache"
    return response



@app.route("/login/form", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def login_form():
    go_back = request.args.get("go_back")

    if not go_back:
        go_back = "/"

    return render_template('login/login_form.html', go_back=go_back)


@app.route("/register/form", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def register_form():
    return render_template('login/register_form.html', field_errors={}, message=gettext("Please enter your registration information"), admin_register=False)


@app.route("/admin_register/form", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def admin_register_form():
    return render_template('login/register_form.html', field_errors={}, message=gettext("Please enter new user registration information"), admin_register=True)


@app.route("/admin_register", methods=["POST"])
@uri_authorized(URIUSE_SESSION_ONLY)
def admin_register():
    return generic_register(True)


@app.route("/register", methods=["POST"])
@uri_authorized(URIUSE_SESSION_ONLY)
def register():
    return generic_register()


def generic_register(admin_register=False):
    user_id = request.form["user_id"]
    password = request.form["password"]
    repeat_password = request.form["repeat_password"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]

    rendering = None


    field_errors = {}

    validate_field(field_errors, "user_id", user_id, True, gettext("User ID is required"))
    validate_field(field_errors, "password", password, True, gettext("Password is required"))
    validate_field(field_errors, "repeat_password", repeat_password, True, gettext("Repeat password is required"))
    validate_field(field_errors, "first_name", first_name, True, gettext("First name is required"))
    validate_field(field_errors, "last_name", last_name, True, gettext("Last name is required"))

    if not "password" in field_errors and not "repeat_password" in field_errors and not password == repeat_password:
        field_errors["repeat_password"] = gettext("Password and repeat password do not match")

    if not "password" in field_errors and not authentication_service.is_password_complex_enough(password):
        field_errors["password"] = gettext("Password does not meet minimum complexity requirements")

    if len(field_errors) > 0:
        rendering = render_template('login/register_form.html', 
            message=gettext("Issues were found with this registration"), 
            user_id=user_id, 
            password=password, 
            repeat_password=repeat_password, 
            first_name=first_name, 
            last_name=last_name,
            field_errors=field_errors,
            error=True,
            admin_register=admin_register)

    else:
        ai:AuthenticationInfo  = authentication_service.add_authentication_info(user_id, password, no_verify=admin_register)
        if ai:
            profile_info = ProfileInfo(user_id, user_id, first_name, last_name)

            profile_service.add_profile_info(profile_info)

            if authentication_service.is_account_verification_required() and not admin_register:
                account_verify_sendmail.send_message(profile_info.email_address, {"verification_code":ai.verification_code})

                rendering = render_template('login/verify.html', message=gettext("Verification code was sent to your email address. Please enter for verification."), error=False, user_id=user_id, field_errors={})
            else:
                if not admin_register:
                    rendering = redirect("/")
                else:
                    rendering = redirect("/security/users")

        else:
            rendering = render_template('login/register_form.html', 
                message=gettext("Registration failed, email address may already be registered"), 
                user_id=user_id, 
                password=password, 
                repeat_password=repeat_password, 
                first_name=first_name, 
                last_name=last_name,
                field_errors=field_errors,
                error=True,
                admin_register=admin_register)

    return rendering


@app.route("/verify/resend", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def resend_verification_code():
    user_id = request.args.get("user_id")
    ai = authentication_service.new_verification(user_id)

    account_verify_sendmail.send_message(user_id, {"verification_code":ai.verification_code})

    return render_template('login/verify.html', message=gettext("A new verification code was sent to your email address. Please enter for verification."), error=False, user_id=user_id, field_errors={})


@app.route("/verify", methods=["POST"])
@uri_authorized(URIUSE_SESSION_ONLY)
def verify_account():
    user_id = request.form["user_id"]
    verification_code = request.form["verification_code"]

    if authentication_service.verify(user_id, verification_code):
        rendering = render_template('login/login_form.html', go_back="/", user_id=user_id, message=gettext("Your account is now verified. You may log in."), error=False)
    else:
        field_errors = {"verification_code" : gettext("An incorrect verification code was entred") }
        rendering = render_template('login/verify.html', message=gettext("The verification code entered was incorrect"), error=True, user_id=user_id, field_errors=field_errors)

    return rendering


@app.route("/login", methods=["POST"])
@uri_authorized(URIUSE_SESSION_ONLY)
def login():
    go_back = request.form.get("go_back")

    user_id = request.form["user_id"]
    password = request.form["password"]
    rendering = None

    if authentication_service.authenticate(user_id, password):
        ai = authentication_service.get_authentication_info(user_id)
        if not ai.verification_code:
            profile_info:ProfileInfo = profile_service.get_profile_info(user_id)

            session["user_id"] = user_id
            session["name"] = "%s %s" % (profile_info.first_name, profile_info.last_name)
            session["timezone"] = profile_info.timezone

            rendering = redirect(go_back)
        else:
            rendering = render_template('login/verify.html', message=gettext("This account is unverified. Please enter the verification code that was send to your registered email address."), error=True, user_id=user_id, field_errors={})

    else:
        rendering = render_template('login/login_form.html', go_back=go_back, user_id=user_id, message=gettext("Login Failure"), error=True)

    return rendering


@app.route("/logout", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def logout():
    if "user_id" in session:
        del session["user_id"]

    if "name" in session:
        del session["name"]

    return redirect("/")


@app.route("/profile/form", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def profile_form():
    profile = profile_service.get_profile_info(session["user_id"])

    return render_template('login/update_profile.html', profile=profile, field_errors={})



@app.route("/profile", methods=["POST"])
@uri_authorized(URIUSE_SESSION_ONLY)
def update_profile():
    rendering = None

    profile = profile_service.get_profile_info(session["user_id"])

    profile.last_name = request.form["last_name"]
    profile.first_name = request.form["first_name"]

    field_errors = {}

    validate_field(field_errors, "first_name", profile.first_name, True, gettext("First name is required"))
    validate_field(field_errors, "last_name", profile.last_name, True, gettext("Last name is required"))

    if len(field_errors) == 0:
        profile_service.update_profile_info(profile)
        session["name"] = "%s %s" % (profile.first_name, profile.last_name)
        rendering = render_template('login/update_profile.html', profile=profile, field_errors={}, error=False, message=gettext("Profile was updated sucessfully"))
    else:
        rendering = render_template('login/update_profile.html', profile=profile, field_errors=field_errors, error=True, message=gettext("Error updating profile"))

    return rendering


@app.route("/groups", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def list_groups():
    groups = group_service.get_groups()
    return render_template('application_admin/group_list.html', groups=groups)



@app.route("/groups/__new", methods=["POST"])
@uri_authorized(URIUSE_SESSION_ONLY)
def add_group():
    rendering = None

    group = Group(request.form["name"], request.form["description"])

    field_errors = {}

    validate_field(field_errors, "name", group.description, True, gettext("Name is required"))
    validate_field(field_errors, "description", group.description, True, gettext("Description is required"))

    if len(field_errors) == 0:
        try:
            group_service.add_group(group)
            groups = group_service.get_groups()
            rendering = redirect("/security/groups")
        except DuplicateGroupException as e:
            field_errors["name"] = gettext("This name already exists")

    if not rendering:
        rendering = render_template('application_admin/group_edit.html', function="add", group=group, field_errors=field_errors, error=True, message=gettext("Error adding group"))

    return rendering

def get_group_members(group_name):
    member_user_ids = group_service.get_group_members(group_name)

    members = []
    for user_id in member_user_ids:
        profile = profile_service.get_profile_info(user_id)
        if profile:
            members.append(profile)

    return members


@app.route("/groups/<group_name>", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def display_group_update(group_name):
    group = group_service.get_group(group_name)
    members = get_group_members(group_name)
    return render_template('application_admin/group_edit.html', function="update", members=members, group=group, field_errors={}, error=False, message="")
    

@app.route("/groups/__new", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def display_group_add():
    group = Group("","")
    return render_template('application_admin/group_edit.html', function="add", members=None, group=group, field_errors={}, error=False, message="")
    

@app.route("/groups/<group_name>/__delete", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def delete_group(group_name):
    try:
        group_service.delete_group(group_name)
        
    except NoSuchGroupException as e:
        pass

    return redirect("/security/groups")
    

@app.route("/groups/<group_name>", methods=["POST"])
@uri_authorized(URIUSE_SESSION_ONLY)
def update_group(group_name):
    rendering = None

    group = Group(group_name, request.form["description"])

    field_errors = {}

    validate_field(field_errors, "description", group.description, True, gettext("Description is required"))

    if len(field_errors) == 0:
        group_service.update_group(group)
        rendering = redirect("/security/groups")
    else:
        members = get_group_members(group_name)
        rendering = render_template('login/group_edit.html', function="update", members=members, group=group, field_errors=field_errors, error=True, message=gettext("Error updating group"))

    return rendering


@app.route("/users", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def get_users():
    raw_profiles = profile_service.get_all_profiles()
    profiles = []
    for raw_profile in raw_profiles:
        profile = EnrolledProfileInfo(raw_profile, group_service.get_group_names_for_user(raw_profile.user_id))
        profiles.append(profile)

    return render_template('application_admin/user_list.html', profiles=profiles)


           
@app.route("/users/<user_id>/group_enrollments", methods=["POST"])
@uri_authorized(URIUSE_SESSION_ONLY)
def update_group_enrollments(user_id):

    all_groups = group_service.get_groups()

    update_groups = []

    for group in all_groups:

        key = "group_%s" % group.name

        if key in request.form:
            update_groups.append(group.name)

    group_service.update_groups_for_user(user_id, update_groups)

    return redirect("/security/users")



@app.route("/users/<user_id>/group_enrollments", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def get_group_enrollments(user_id):

    profile = profile_service.get_profile_info(user_id)

    groups = []
    all_groups = group_service.get_groups()
    users_groups = group_service.get_group_names_for_user(user_id)

    for raw_group in all_groups:
        selected = False
        if raw_group.name in users_groups:
            selected = True

        group = SelectedGroup(raw_group, selected)

        groups.append(group)

    return render_template('application_admin/group_enrollments.html', profile=profile, groups=groups)


@app.route("/uri_access_rights", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def get_uriaccess_rights():
    uri_access_rights = uri_access_rights_service.get_all_authorizations()
    uri_access_rights.sort(key=lambda e: e.right_name)
    return render_template('application_admin/rights_list.html', uri_access_rights=uri_access_rights)



@app.route("/uri_access_rights/<right_name>", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def edit_uriaccess_rights(right_name:str):
    uri_access_right = uri_access_rights_service.get_authorization(right_name)

    if uri_access_right:
        uri_access_right_bean = build_access_right_bean(uri_access_right)

        return render_template('application_admin/right_form.html', uri_access_right=uri_access_right_bean, field_errors={}, function="update")
    else:
        return redirect("/security/uri_access_rights")




@app.route("/uri_access_rights/<right_name>", methods=["POST"])
@uri_authorized(URIUSE_SESSION_ONLY)
def update_uriaccess_rights(right_name:str):
    uri_access_right = uri_access_rights_service.get_authorization(right_name)
    uri_access_right.uri = request.form["uri"]
    uri_access_right.methods = request.form.getlist("methods")
    uri_access_right.filters = request.form.getlist("filters")
    uri_access_right.authorized_groups = request.form.getlist("authorized_groups")

    field_errors = {}

    validate_field(field_errors, "uri", uri_access_right.uri, True, gettext("URI is required"))
    validate_field(field_errors, "methods", uri_access_right.methods, True, gettext("At least one method must be selected"))

    if len(field_errors) == 0:
        uri_access_rights_service.update_authorization(uri_access_right)

        return redirect("/security/uri_access_rights")
    else:
        uri_access_right_bean = build_access_right_bean(uri_access_right)

        return render_template('application_admin/right_form.html', uri_access_right=uri_access_right_bean, field_errors=field_errors, function="update")





@app.route("/uri_access_rights/__new", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def add_uriaccess_rights_form():
    uri_access_right_bean = init_access_right_bean()
    return render_template('application_admin/right_form.html', uri_access_right=uri_access_right_bean, field_errors={}, function="add")



@app.route("/uri_access_rights/__new", methods=["POST"])
@uri_authorized(URIUSE_SESSION_ONLY)
def add_uriaccess_rights():
    uri_access_right = URIAccessRight(request.form["right_name"], request.form["uri"], request.form.getlist("methods"), request.form.getlist("filters"), request.form.getlist("authorized_groups"))

    field_errors = {}

    validate_field(field_errors, "uri", uri_access_right.uri, True, gettext("URI is required"))
    validate_field(field_errors, "methods", uri_access_right.methods, True, gettext("At least one method must be selected"))

    rendering = None

    if len(field_errors) == 0:
        try:
            uri_access_rights_service.add_authorization(uri_access_right)
            rendering = redirect("/security/uri_access_rights")

        except DuplicateRight as e:
            field_errors["right_name"] = gettext("Different access rights cannot share the same name")
            uri_access_right_bean = build_access_right_bean(uri_access_right)

            rendering = render_template('application_admin/right_form.html', uri_access_right=uri_access_right_bean, field_errors=field_errors, function="add")
    else:
            uri_access_right_bean = build_access_right_bean(uri_access_right)

            rendering =  render_template('application_admin/right_form.html', uri_access_right=uri_access_right_bean, field_errors=field_errors, function="add")


    return rendering



def init_access_right_bean():
    uri_access_right = URIAccessRight("", "", [], [], [])
    return build_access_right_bean(uri_access_right) 


def build_access_right_bean(uri_access_right:URIAccessRight):
    available_filters_uris = []
    all_uri_access_rights = uri_access_rights_service.get_all_authorizations()
    for uar in all_uri_access_rights:
        available_filters_uris.append(uar.uri)

    available_filters_uris = list(dict.fromkeys(available_filters_uris))
    available_filters_uris.sort()

    available_groups = group_service.get_groups()
    group_list = group_service.get_default_group_names()
    for ag in available_groups:
        group_list.append(ag.name)

    group_list.sort()

    uri_access_right_bean = AccessRightBean(uri_access_right, group_list, available_filters_uris)

    return uri_access_right_bean



@app.route("/uri_access_rights/<right_name>/__delete", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def delete_access_right(right_name):
    uri_access_rights_service.delete_authorization(right_name)
    return redirect("/security/uri_access_rights")



@app.route("/password_change/form", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def change_password_form():
    return render_template("/login/password_change_form.html")


@app.route("/password_change", methods=["POST"])
@uri_authorized(URIUSE_SESSION_ONLY)
def change_password():
    current_password = request.form["current_password"]
    new_password = request.form["new_password"]
    repeat_new_password = request.form["repeat_new_password"]
    user_id = session["user_id"]
    field_errors = {}

    validate_field(field_errors, "current_password", current_password, True, gettext("Current password is required"))
    validate_field(field_errors, "new_password", new_password, True, gettext("New password is required"))
    validate_field(field_errors, "repeat_new_password", repeat_new_password, True, gettext("Repeat new password is required"))
    
    if new_password == current_password:
        field_errors["new_password"] = gettext("Current password and new password are the same")

    if not new_password == repeat_new_password:
        field_errors["repeat_new_password"] = gettext("New password and repeat new password are different")

    if not "new_password" in field_errors and not authentication_service.is_password_complex_enough(new_password):
        field_errors["new_password"] = gettext("New password does not meet minimum complexity requirements")

    if len(field_errors) == 0:
        if not authentication_service.change_password(user_id, current_password, new_password):
            field_errors["current_password"] = "Incorrect password"

    if len(field_errors) > 0:
        rendering = render_template("/login/password_change_form.html", message=gettext("Change password failure"), error=True, field_errors=field_errors)
    else:
        rendering = render_template("/login/message.html", message=gettext("Password change was sucessful"))

    return rendering



@app.route("/delete_user", methods=["GET"])
@uri_authorized(URIUSE_SESSION_ONLY)
def delete_user():
    user_id = request.args["user_id"]
    group_service.update_groups_for_user(user_id, [])
    profile_service.delete_profile_info(user_id)
    authentication_service.delete_authentication_info(user_id)
    return redirect("/security/users")

