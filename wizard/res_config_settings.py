from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    alicuotaonline_api_key = fields.Char(
        related='company_id.alicuotaonline_api_key'
    )