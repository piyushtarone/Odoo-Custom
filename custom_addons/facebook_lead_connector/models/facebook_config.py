from odoo import models, fields


class FacebookConfig(models.Model):
    _name = 'facebook.config'
    _description = 'Facebook Configuration'

    name = fields.Char(
        string="Configuration Name",
        default="Default Config",
        required=True
    )

    app_id = fields.Char(
        string="App ID"
    )

    app_secret = fields.Char(
        string="App Secret"
    )

    access_token = fields.Text(
        string="Access Token"
    )

    verify_token = fields.Char(
        string="Verify Token"
    )

    page_id = fields.Char(
        string="Page ID"
    )

    form_id = fields.Char(
        string="Lead Form ID"
    )
