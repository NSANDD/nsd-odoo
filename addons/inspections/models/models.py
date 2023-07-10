# -*- coding: utf-8 -*-

from odoo import models, fields, api

class inspection(models.Model):
    _name = 'inspection.inspection'

    name = fields.Char('Inspection Contract Name', required=True)
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    active = fields.Boolean('Active', default=True, tracking=True)
    description = fields.Text('Description')
    building_name = fields.Char('Building Name')
    customer = fields.Many2one('res.partner', string='Customer', index=True, tracking=True)
    
    total_doors= fields.Integer(compute="_calc_total_doors")

    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)

    entryways = fields.One2many(
        comodel_name='inspection.entryway',
        inverse_name='inspection_id',
        string="Entry",
        copy=True, auto_join=True)
    stage_id = fields.Many2one(
        'inspection.stages', string='Stage', index=True, tracking=True,
        readonly=False, store=True, copy=False, ondelete='restrict')


    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100
    
    def _calc_total_doors(self):
        self.total_doors = 1

    def _stage_find(self, domain=None, order='sequence'):
        search_domain = domain
        return self.env['inspection.stages'].search(search_domain, order=order, limit=1)


    def toggle_closed_stage(self):
        for lead in self:
            stage_id = inspection._stage_find(domain=[('is_closed','=', True)])
            lead.write({'stage_id': stage_id.id})
        return True


class entryway(models.Model):
    _name = 'inspection.entryway'
    _order = 'inspection_id, sequence, id'

    name = fields.Char('Opening ID')
    sequence = fields.Integer(string="Sequence", default=10)
    entry_label = fields.Char('NSD Label Number')
    nominal_opening = fields.Char('Nominal Opening (height x width)')
    opening_type = fields.Selection([( 'single_door', 'Single'),( 'double_door', 'Double'),( 'other_door', 'Other')], string='Opening Type', required=True)
    opening_description = fields.Text('Opening description')

    inspection_id = fields.Many2one(
        comodel_name='inspection.inspection',
        string="Inspection Reference",
        required=True, ondelete='cascade', index=True, copy=False)