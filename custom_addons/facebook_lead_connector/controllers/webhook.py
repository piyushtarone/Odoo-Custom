from odoo import http
from odoo.http import request


class FacebookWebhook(http.Controller):

    @http.route(
        '/facebook/test',
        auth='public',
        website=True
    )
    def test_route(self, **kwargs):

        request.env['crm.lead'].sudo().create({
            'name': 'Facebook Test Lead',
            'contact_name': 'Piyush',
            'email_from': 'test@gmail.com',
            'phone': '9999999999'
        })

        return "Lead Created Successfully"
