from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

class CreditGroupAPI(http.Controller):

    @http.route('/api/create_or_update_credit_group', type='json', auth='public', methods=['POST'], csrf=False)
    def create_or_update_credit_group(self, **params):
        try:
            credit_group_data = params.get('grupo_credititos')
            if not credit_group_data:
                return {"status": 400, "message": "No se proporcionaron datos válidos."}

            for group_data in credit_group_data:
                code = group_data.get('codigo')
                channel_code = group_data.get('canal')

                channel = request.env['sale.channel'].search([('code', '=', channel_code)])
                if not channel:
                    return {"status": 400, "message": f"No se encontró el canal {channel_code}"}
                
                credit_group = request.env['credit.group'].search([('code', '=', code)])

                if credit_group:
                    credit_group.write({
                        'name': group_data.get('name'),
                        'sale_channel_id': channel.id,
                        'credit_global': group_data.get('credito_global')
                    })
                else:
                    request.env['credit.group'].create({
                        'name': group_data.get('name'),
                        'code': code,
                        'credit_global': channel.id,
                        'credit_global': group_data.get('credito_global')
                    })

            return {"status": 200, "message": "OK"}

        except Exception as e:
            return {"status": 500, "message": str(e)}
