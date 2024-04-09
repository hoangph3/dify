from flask_restful import Resource, reqparse

from controllers.console.setup import setup_required
from controllers.inner_api import api
from controllers.inner_api.wraps import inner_api_only
from models.account import Account
from services.account_service import TenantService


class EnterpriseWorkspace(Resource):

    @setup_required
    @inner_api_only
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        parser.add_argument('owner_email', type=str, required=True, location='json')
        args = parser.parse_args()

        account = Account.query.filter_by(email=args['owner_email']).first()
        if account is None:
            return {
                'message': 'owner account not found.'
            }, 404

        tenant = TenantService.create_tenant(args['name'])
        TenantService.create_tenant_member(tenant, account, role='owner')

        return {
            'message': 'enterprise workspace created.'
        }


api.add_resource(EnterpriseWorkspace, '/enterprise/workspace')

