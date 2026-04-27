from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class Course(models.Model):
    _name = "lms.course"
    _description = "LMS Course"
    _rec_name = "name"

    # -------------------------
    # Basic Fields
    # -------------------------
    name = fields.Char(string="Course Name", required=True)

    description = fields.Text(string="Description")

    is_published = fields.Boolean(default=False)
    # -------------------------
    # Relationships
    # -------------------------
    instructor_id = fields.Many2one(
        comodel_name="res.users",
        string="Instructor",
        ondelete="set null"
    )

    enrollment_ids = fields.One2many(
        comodel_name="lms.enrollment",
        inverse_name="course_id",
        string="Enrollments"
    )

    

    def assign_instructor(self, instructor):
        if not instructor or instructor._name != "res.users" or not instructor.exists():
            raise ValidationError("Instructor does not exist.")

        for course in self:
            course.instructor_id = instructor

    def publish_course(self):
        for course in self:
            course.is_published = True

    def unpublish_course(self):
        for course in self:
            course.is_published = False

    def check_user_can_edit(self, user):
        for course in self:
            if course.instructor_id != user:
                raise UserError("Only the assigned instructor can edit this course.")
        return True

    def get_course_structure(self):
        result = []

        for course in self:
            course_data = {
                "id": course.id,
                "name": course.name,
                "modules": []
            }

            for module in course.module_ids:
                module_data = {
                    "id": module.id,
                    "name": module.name,
                    "lessons": []
                }

                for lesson in module.lesson_ids:
                    lesson_data = {
                        "id": lesson.id,
                        "name": lesson.name,
                        "contents": []
                    }

                    for content in lesson.content_ids:
                        lesson_data["contents"].append({
                            "id": content.id,
                            "name": content.name
                        })

                    module_data["lessons"].append(lesson_data)

                course_data["modules"].append(module_data)

            result.append(course_data)

        return result