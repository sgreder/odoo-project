"""
Scrum 34 - Relationships & Constraints tests for the LMS hierarchy.

Covers the course - module relationship owned by lms_course_management.
The module - lesson and lesson - content relationships are validated
by tests in the lms_lesson addon.
"""
from odoo.tests.common import TransactionCase


class TestCourseModuleRelationship(TransactionCase):

    def setUp(self):
        super().setUp()
        self.course = self.env['lms.course'].create({
            'name': 'Test Course',
        })

    # ------------------------------------------------------------------
    # Course - Module relationship
    # ------------------------------------------------------------------

    def test_module_requires_course_id(self):
        """A module cannot be created without a course."""
        with self.assertRaises(Exception):
            self.env['lms.course.module'].create({'name': 'Orphan Module'})

    def test_module_course_id_returns_correct_record(self):
        module = self.env['lms.course.module'].create({
            'name': 'Module A',
            'course_id': self.course.id,
        })
        self.assertEqual(module.course_id, self.course)

    def test_course_module_ids_inverse(self):
        """course.module_ids returns all modules of the course."""
        m1 = self.env['lms.course.module'].create({
            'name': 'M1',
            'course_id': self.course.id,
        })
        m2 = self.env['lms.course.module'].create({
            'name': 'M2',
            'course_id': self.course.id,
        })
        self.assertIn(m1, self.course.module_ids)
        self.assertIn(m2, self.course.module_ids)

    def test_module_name_required(self):
        with self.assertRaises(Exception):
            self.env['lms.course.module'].create({
                'course_id': self.course.id,
            })

    # ------------------------------------------------------------------
    # Cascade behavior
    # ------------------------------------------------------------------

    def test_cascade_delete_modules_on_course_delete(self):
        """Deleting a course removes all its modules."""
        module = self.env['lms.course.module'].create({
            'name': 'To Be Deleted',
            'course_id': self.course.id,
        })
        module_id = module.id
        self.course.unlink()
        self.assertFalse(
            self.env['lms.course.module'].browse(module_id).exists()
        )

    def test_cascade_delete_multiple_modules_on_course_delete(self):
        m1 = self.env['lms.course.module'].create({
            'name': 'M1',
            'course_id': self.course.id,
        })
        m2 = self.env['lms.course.module'].create({
            'name': 'M2',
            'course_id': self.course.id,
        })
        ids = [m1.id, m2.id]
        self.course.unlink()
        remaining = self.env['lms.course.module'].search(
            [('id', 'in', ids)]
        )
        self.assertFalse(remaining)

    # ------------------------------------------------------------------
    # Ordering
    # ------------------------------------------------------------------

    def test_default_module_sequence_is_1(self):
        module = self.env['lms.course.module'].create({
            'name': 'Default Seq',
            'course_id': self.course.id,
        })
        self.assertEqual(module.sequence, 1)

    def test_modules_ordered_by_sequence_asc(self):
        m3 = self.env['lms.course.module'].create({
            'name': 'M3', 'course_id': self.course.id, 'sequence': 3,
        })
        m1 = self.env['lms.course.module'].create({
            'name': 'M1', 'course_id': self.course.id, 'sequence': 1,
        })
        m2 = self.env['lms.course.module'].create({
            'name': 'M2', 'course_id': self.course.id, 'sequence': 2,
        })
        modules = self.env['lms.course.module'].search(
            [('course_id', '=', self.course.id)]
        )
        self.assertEqual(list(modules), [m1, m2, m3])

    def test_update_sequence_changes_module_ordering(self):
        m1 = self.env['lms.course.module'].create({
            'name': 'M1', 'course_id': self.course.id, 'sequence': 1,
        })
        m2 = self.env['lms.course.module'].create({
            'name': 'M2', 'course_id': self.course.id, 'sequence': 2,
        })
        m1.sequence = 10
        modules = self.env['lms.course.module'].search(
            [('course_id', '=', self.course.id)]
        )
        self.assertEqual(modules[0], m2)

    # ------------------------------------------------------------------
    # Foreign key validity
    # ------------------------------------------------------------------

    def test_invalid_course_id_rejected(self):
        """Creating a module pointing at a non-existent course is rejected."""
        with self.assertRaises(Exception):
            self.env['lms.course.module'].create({
                'name': 'Bad FK',
                'course_id': 999999999,
            })
