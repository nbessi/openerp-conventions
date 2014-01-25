# -*- coding: utf-8 -*-
from openerp.osv import orm, fields
import osv


class correct_model(orm.orm):

    _inherit = "correct.model"


class FaultyName(orm.Model):
    _name = "faulty.name"
    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'description': fields.text('Description'),
    }


class faulty_model(osv.osv):

    _inherit = "faulty.model"
