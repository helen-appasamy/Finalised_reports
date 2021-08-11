# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo import tools


class UserAccessReport(models.Model):
    _name = "user.access.view"
    _auto = False
    _description = "User Access Report Details"

    login = fields.Char(string='Login')
    user_id = fields.Many2one('res.users', string='Name')
    department_id = fields.Many2one('hr.department', string='Department')
    parent_id = fields.Many2one('hr.employee',string='Manager')
    address_id = fields.Many2one('res.partner', string='Work Address')
    category_id = fields.Many2one('ir.module.category', string='Menu')
    group_id = fields.Char(string='Access Right')


    def _select(self):
        return """
            SELECT
                row_number() over() as id,
                users.id as user_id,
                users.login,
                employee.department_id,
                employee.parent_id,
                employee.address_id,
                groups.category_id,
                groups.name as group_id                   
        """

    def _from(self):
        return """
            FROM res_users as users
        """

    def _join(self):
        return """
            LEFT JOIN hr_employee as employee ON employee.user_id=users.id AND users.active=true
            LEFT JOIN res_groups_users_rel as user_rel ON users.id=user_rel.uid
            LEFT JOIN res_groups as groups ON groups.id=user_rel.gid
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
            )
        """ % (self._table, self._select(), self._from(), self._join())
        )
