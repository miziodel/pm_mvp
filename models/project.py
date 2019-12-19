# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Project(models.Model):

    # XXX: _name is mandatory to let activity.mixin bootstrap correctly
    _name = 'project.project' 
    _inherit = ['project.project', 'mail.activity.mixin']
    
    
    @api.multi
    def open_project_view(self):
        self.ensure_one()
        # view = self.env.ref('module.record_form_view')
        # view = self.env.ref('project.view_project')
        return {
                'name': '%s' % self.name,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'project.project',
                'views': [(False,'form')],
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': self.id,
                # if you want to open the form in edit mode direclty            
                'flags': {'initial_mode': 'edit'},
                'context': dict(self.env.context),
                }
    
    @api.multi
    def open_project_kanban(self):
        self.ensure_one()
        # view = self.env.ref('project.view_project')
        return {
                'name': '%s' % self.name,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'project.project',
                'views': [(False,'form')],
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': self.id,
                # 'context': {},
                'context': dict(self.env.context),
                }
    
