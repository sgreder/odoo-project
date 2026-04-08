from odoo import models, fields

class LMSUserRating(models.Model):
    _name = 'lms.user.rating'
    _description = 'User Rating'

    rater_id = fields.Many2one('res.users', required=True, ondelete='cascade')
    rated_user_id = fields.Many2one('res.users', required=True, ondelete='cascade')
    rating = fields.Integer(required=True)

    _sql_constraints = [
        ('unique_rating', 'unique(rater_id, rated_user_id)',
         'You have already rated this user.')
    ]