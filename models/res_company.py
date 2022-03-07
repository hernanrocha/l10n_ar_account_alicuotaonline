# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import UserError

import requests
import logging

_logger = logging.getLogger(__name__)

# https://dev.to/katzueno/setting-up-let-s-encrypt-on-amazon-linux-2-57l7

ALICUOTA_ONLINE_HOST = "https://api.alicuotaonline.com"

def query_alicuotaonline(id_jurisdiccion, cuit, api_key):
    resp = requests.get("{}/padron_iibb/jurisdiccion/{}?cuit={}".format(
        ALICUOTA_ONLINE_HOST, id_jurisdiccion, cuit), 
        headers={
            'X-Gravitee-Api-Key': api_key
        })

    if resp.status_code == 401:
        raise UserError("Error consultando AlicuotaOnline - Acceso denegado")

    if resp.status_code == 429:
        raise UserError("Error consultando AlicuotaOnline - Has alcanzado el límite de consultas permitidas")
    
    if resp.status_code != 200:
        raise Exception("Error consultando AlicuotaOnline - Codigo de error {}".format(resp.status_code))

    return resp.json()

class ResCompany(models.Model):
    _inherit = "res.company"

    alicuotaonline_api_key = fields.Char(string="AlicuotaOnline API Key")

    def get_agip_data(self, partner, date):
        self.ensure_one()

        cuit = partner.cuit_required()
        api_key = self.alicuotaonline_api_key

        _logger.info('AlicuotaOnline - Consultando CUIT %s para fecha %s' % (cuit, date))

        if not api_key:
            raise UserError("Para poder utilizar AlicuotaOnline, debes configurar la API Key desde la sección de Ajustes - Contabilidad")

        json_data = query_alicuotaonline('901', cuit, api_key)
        data = {
            'numero_comprobante': 0,
            'codigo_hash': 0,
            'alicuota_percepcion': json_data['alicuota_percepcion'],
            'alicuota_retencion': json_data['alicuota_retencion'],
            'grupo_percepcion': 0,
            'grupo_retencion': 0,
            'from_date': json_data['fecha_desde'],
            'to_date': json_data['fecha_hasta'],
        }
        
        return data