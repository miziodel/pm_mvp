# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Project(models.Model):

    _name = 'project.project' 
    _inherit = ['project.project', 'mail.thread', 'mail.activity.mixin']
    
    project_budget_hours = fields.Integer(string="Project Budget Hours",
                                help="agreed number of hours to complete the project.")
    
    task_planned_hours = fields.Integer(compute='_compute_tasks_planned_hours', 
                                string="Planned Hours on total tasks",
                                help="number of hours planned on the whole set of tasks.")
    task_active_planned_hours = fields.Integer(compute='_compute_tasks_active_planned_hours', 
                                string="Planned Hours on uncompleted tasks",
                                help="number of hours planned on the tasks yet to be done.")
    
    priority = fields.Integer(string="Priority",
                              help="priority number: higher the number, higher the priority.")
    
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
                # 'target': 'new',
                'target': 'current',
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
    
    def _compute_tasks_planned_hours(self):
        for project in self:
            project.task_planned_hours = sum(project.task_ids.
                                                mapped('planned_hours'))

    def _compute_tasks_active_planned_hours(self):
        active_tasks = lambda r: not r.stage_id.closed
        for project in self:
            project.task_active_planned_hours = sum(project.task_ids.
                                                      filtered(active_tasks).
                                                      mapped('planned_hours'))


class ProjectMilestone(models.Model):
    _inherit = 'project.milestone'
      

    date_start = fields.Datetime(string='Starting Date',
                                 default=fields.Datetime.now,
                                 index=True, copy=False)
    
    milestone_budget_hours = fields.Integer(string="Milestone Budget Hours",
                                help="agreed number of hours to complete the milestone.")
    
    mls_task_planned_hours = fields.Integer(compute='_compute_mls_tasks_planned_hours', 
                                string="Planned Hours on milestones' total tasks",
                                help="number of hours planned on the whole set of tasks for the milestone.")
    mls_task_active_planned_hours = fields.Integer(compute='_compute_mls_tasks_active_planned_hours', 
                                string="Planned Hours on uncompleted tasks",
                                help="number of hours planned on the tasks yet to be done for the milestone.")

    def _compute_mls_tasks_planned_hours(self):
        for milestone in self:
            milestone.mls_task_planned_hours = sum(milestone.project_task_ids.
                                                    mapped('planned_hours'))

    def _compute_mls_tasks_active_planned_hours(self):
        active_tasks = lambda r: not r.stage_id.closed
        for milestone in self:
            milestone.mls_task_active_planned_hours = sum(milestone.project_task_ids.
                                                            filtered(active_tasks).
                                                            mapped('planned_hours'))

# TODO: mostra tempi pianificati e totali sulla grid delle milestone nella form view del progetto!!