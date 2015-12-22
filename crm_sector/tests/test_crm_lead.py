# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Javier Iniesta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


class TestCrmLead(TransactionCase):

    def test_check_sectors(self):
        sector = self.env['res.partner.sector'].create({'name': 'Test'})
        with self.assertRaises(ValidationError):
            self.env['crm.lead'].create(
                {'name': 'Test', 'sector_id': sector.id,
                 'secondary_sector_ids': [(4, sector.id)]})

    def test_lead_create_contact(self):
        sector_pool = self.env['res.partner.sector']
        sector_1 = sector_pool.create({'name': 'Test 01'})
        sector_2 = sector_pool.create({'name': 'Test 02',
                                       'parent_id': sector_1.id})
        sector_3 = sector_pool.create({'name': 'Test 03',
                                       'parent_id': sector_1.id})
        lead_vals = {
            'name': 'test',
            'partner_name': 'test',
            'sector_id': sector_1.id,
            'secondary_sector_ids': [(4, sector_2.id, 0), (4, sector_3.id, 0)]
        }
        lead = self.env['crm.lead'].create(lead_vals)
        partner_id = self.env['crm.lead']._lead_create_contact(
            lead, lead.partner_name, True)
        partner = self.env['res.partner'].browse(partner_id)
        self.assertEqual(partner.sector_id.id, lead.sector_id.id)
        self.assertListEqual(partner.secondary_sector_ids.ids,
                             lead.secondary_sector_ids.ids)
