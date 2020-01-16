# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Project(models.Model):

    _name = 'project.project' 
    _inherit = ['project.project', 'mail.thread', 'mail.activity.mixin']
    
    project_budget_hours = fields.Integer(string="Budget Hours",
                                help="agreed number of hours to complete the project.")
    
    task_planned_hours = fields.Integer(compute='_compute_tasks_planned_hours', 
                                string="Planned Hours on tasks",
                                help="number of hours planned on the whole set of tasks.")
    task_active_planned_hours = fields.Integer(compute='_compute_tasks_active_planned_hours', 
                                string="Planned Hours on uncompleted tasks",
                                help="number of hours planned on the tasks yet to be done.")
    
    priority = fields.Integer(string="Priority",
                              help="priority number: higher the number, higher the priority.")
    
    progress = fields.Float(
        compute="_compute_project_progress",
        # store=True,
        help="Percentage of Completed Tasks vs Incomplete Tasks.")

    milestone_count = fields.Integer(compute='_compute_milestone_count', string="Milestones Count")


    
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
                # if you want to open the form in edit mode directly            
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

    # @api.depends('task_ids.stage_id')
    def _compute_project_progress(self):
        for record in self:
            total_tasks_count = record.task_count
            closed_tasks_count = 0.0
            for task_record in record.task_ids:
                # total_tasks_count += 1
                if task_record.stage_id.closed:
                    closed_tasks_count += 1
            if total_tasks_count > 0:
                record.progress = (
                    closed_tasks_count / total_tasks_count) * 100
            else:
                record.progress = 0.0
                
    def _compute_milestone_count(self):
        for rec in self:
            if rec.use_milestones:
                rec.milestone_count = len(rec.milestone_ids)
                # rec.milestone_count = self.env['project.project'].search_count([('project', '=', rec.id)]) 
            else:
                rec.milestone_count = 0


class ProjectMilestone(models.Model):
    _inherit = 'project.milestone'
      

    date_start = fields.Datetime(string='Starting Date',
                                 default=fields.Datetime.now,
                                 index=True, copy=False)
    
    milestone_budget_hours = fields.Integer(string="Budget Hours",
                                help="agreed number of hours to complete the milestone.")
    
    mls_task_planned_hours = fields.Integer(compute='_compute_mls_tasks_planned_hours', 
                                string="Planned Hours on tasks",
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


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # is_blocked = fields.Boolean(compute='_compute_task_is_blocked', 
    #                          string="the task is blocked, and can't be processed at this time.",)

    is_done = fields.Boolean(compute='_compute_task_is_done', 
                             string="the task is in a 'done' stage",)

    @api.multi
    def open_task_view(self):
        self.ensure_one()
        return {
                'name': '%s' % self.name,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'project.task',
                'views': [(False,'form')],
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': self.id,
                # if you want to open the form in edit mode directly
                'flags': {'initial_mode': 'edit'},
                'context': dict(self.env.context),
                }

    # def _compute_task_is_blocked(self):
    #     for rec in self:
    #         rec.is_blocked = rec.kanban_state == 'blocked'

    def _compute_task_is_done(self):
        for rec in self:
            rec.is_done = rec.stage_id.closed

