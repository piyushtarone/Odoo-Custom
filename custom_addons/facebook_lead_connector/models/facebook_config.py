from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

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

    def action_fetch_leads(self):
        for config in self:
            if not config.access_token or not config.form_id:
                _logger.warning("Facebook Config: Missing access token or form ID.")
                continue
                
            url = f"https://graph.facebook.com/v19.0/{config.form_id}/leads"
            params = {
                'access_token': config.access_token,
                'fields': 'id,created_time,field_data'
            }
            
            try:
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    leads = data.get('data', [])
                    
                    for lead in leads:
                        lead_id = lead.get('id')
                        
                        # Check if lead already exists
                        existing_lead = self.env['crm.lead'].search([('facebook_lead_id', '=', lead_id)], limit=1)
                        if existing_lead:
                            continue
                            
                        # Parse field_data
                        field_data = lead.get('field_data', [])
                        lead_vals = {
                            'name': f"Facebook Lead - {lead_id}",
                            'facebook_lead_id': lead_id,
                            'description': 'Lead imported from Facebook.\n\n',
                        }
                        
                        for field in field_data:
                            name = field.get('name')
                            values = field.get('values', [])
                            if not values:
                                continue
                                
                            value = values[0]
                            if name in ['email']:
                                lead_vals['email_from'] = value
                            elif name in ['full_name', 'name', 'first_name']:
                                lead_vals['contact_name'] = value
                                lead_vals['name'] = f"Lead: {value}"
                            elif name in ['phone_number', 'phone']:
                                lead_vals['phone'] = value
                            else:
                                lead_vals['description'] += f"{name}: {value}\n"
                                
                        self.env['crm.lead'].create(lead_vals)
                        _logger.info(f"Created new CRM lead from Facebook: {lead_id}")
                else:
                    _logger.error(f"Failed to fetch Facebook leads: {response.text}")
            except Exception as e:
                _logger.error(f"Exception fetching Facebook leads: {str(e)}")

    @api.model
    def cron_fetch_facebook_leads(self):
        configs = self.search([])
        configs.action_fetch_leads()
