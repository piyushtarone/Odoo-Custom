from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    facebook_lead_id = fields.Char(
        string='Facebook Lead ID',
        copy=False,
        index=True,
        help="The unique ID of the lead from Facebook"
    )
