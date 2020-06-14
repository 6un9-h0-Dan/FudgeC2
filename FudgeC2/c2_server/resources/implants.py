from flask_restful import Resource, reqparse
from flask import request
from flask_login import current_user, login_required

from Data.Database import Database
db = Database()

class Implants(Resource):
    method_decorators = [login_required]

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('campaign_id', type=int, help='Campaign IDs are numeric.')
        args = parser.parse_args()

        processed_implants = []
        # Return a list of all implants the user has access to.
        a = db.implant.get_all_implants_by_user(current_user.user_email)
        if 'campaign_id' in args:
            for index, value in enumerate(a):
                if value['campaign_id'] == args['campaign_id']:
                    processed_implants.append(value)
        return processed_implants

class ImplantDetails(Resource):
    method_decorators = [login_required]
    # Return the configuration of an implant
    def get(self, implant_id):
        # Take UID and return info on it.

        pass
        return {}


class ImplantRegistered(Resource):
    method_decorators = [login_required]
    def get(self):
        pass

class ImplantResponses(Resource):
    method_decorators = [login_required]
    def get(self, implant_id):
        # get all implant responses (pagination will be implemented later
        response_list = []
        campaign_id = db.campaign.get_campaign_id_from_implant_id(implant_id)
        if db.campaign.Verify_UserCanAccessCampaign(current_user.user_email, campaign_id):
            response_list = db.implant.get_implant_responses(implant_id)

        return {"data": response_list}