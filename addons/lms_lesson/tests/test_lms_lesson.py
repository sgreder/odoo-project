"""
Tests for lms.lesson and lms.lesson.content models.
Covers all acceptance criteria from the spec.
"""
from odoo.tests.common import TransactionCase


class TestLmsLesson(TransactionCase):

    def setUp(self):
        super().setUp()
        # Requires lms.course.module to exist (provided by lms_course addon)
        self.course = self.env['lms.course'].create({'name': 'Test Course'})
        self.module = self.env['lms.course.module'].create({
            'course_id': self.course.id,
            'name': 'Test Module',
        })

    # ------------------------------------------------------------------
    # 1. Lesson-Module Relationship
    # ------------------------------------------------------------------

    def test_lesson_requires_module_id(self):
        """module_id is required."""
        with self.assertRaises(Exception):
            self.env['lms.lesson'].create({'name': 'No Module'})

    def test_lesson_module_id_returns_correct_record(self):
        lesson = self.env['lms.lesson'].create({
            'name': 'Lesson A',
            'module_id': self.module.id,
        })
        self.assertEqual(lesson.module_id, self.module)

    def test_module_lesson_ids_inverse(self):
        """module.lesson_ids returns all lessons of the module."""
        l1 = self.env['lms.lesson'].create({'name': 'L1', 'module_id': self.module.id})
        l2 = self.env['lms.lesson'].create({'name': 'L2', 'module_id': self.module.id})
        self.assertIn(l1, self.module.lesson_ids)
        self.assertIn(l2, self.module.lesson_ids)

    def test_cascade_delete_lessons_on_module_delete(self):
        """Deleting a module cascades to its lessons."""
        lesson = self.env['lms.lesson'].create({
            'name': 'To Be Deleted',
            'module_id': self.module.id,
        })
        lesson_id = lesson.id
        self.module.unlink()
        self.assertFalse(self.env['lms.lesson'].browse(lesson_id).exists())

    # ------------------------------------------------------------------
    # 2. Lesson Ordering
    # ------------------------------------------------------------------

    def test_default_sequence_is_1(self):
        lesson = self.env['lms.lesson'].create({
            'name': 'Default Seq',
            'module_id': self.module.id,
        })
        self.assertEqual(lesson.sequence, 1)

    def test_lessons_ordered_by_sequence_asc(self):
        l3 = self.env['lms.lesson'].create({'name': 'L3', 'module_id': self.module.id, 'sequence': 3})
        l1 = self.env['lms.lesson'].create({'name': 'L1', 'module_id': self.module.id, 'sequence': 1})
        l2 = self.env['lms.lesson'].create({'name': 'L2', 'module_id': self.module.id, 'sequence': 2})
        lessons = self.env['lms.lesson'].search([('module_id', '=', self.module.id)])
        self.assertEqual(list(lessons), [l1, l2, l3])

    def test_update_sequence_changes_ordering(self):
        l1 = self.env['lms.lesson'].create({'name': 'L1', 'module_id': self.module.id, 'sequence': 1})
        l2 = self.env['lms.lesson'].create({'name': 'L2', 'module_id': self.module.id, 'sequence': 2})
        l1.sequence = 10
        lessons = self.env['lms.lesson'].search([('module_id', '=', self.module.id)])
        self.assertEqual(lessons[0], l2)

    # ------------------------------------------------------------------
    # 3. Content Support
    # ------------------------------------------------------------------

    def test_lesson_can_have_multiple_content_items(self):
        lesson = self.env['lms.lesson'].create({
            'name': 'Rich Lesson',
            'module_id': self.module.id,
            'content_ids': [
                (0, 0, {'type': 'text', 'text_content': '<p>Hello</p>'}),
                (0, 0, {'type': 'video', 'url': 'https://youtube.com/watch?v=abc'}),
                (0, 0, {'type': 'link', 'url': 'https://example.com'}),
            ],
        })
        self.assertEqual(len(lesson.content_ids), 3)

    def test_content_ids_returns_associated_content(self):
        lesson = self.env['lms.lesson'].create({
            'name': 'Lesson With Content',
            'module_id': self.module.id,
        })
        content = self.env['lms.lesson.content'].create({
            'lesson_id': lesson.id,
            'type': 'text',
            'text_content': '<p>Body</p>',
        })
        self.assertIn(content, lesson.content_ids)

    def test_multiple_content_types_coexist(self):
        lesson = self.env['lms.lesson'].create({
            'name': 'Multi-type',
            'module_id': self.module.id,
            'content_ids': [
                (0, 0, {'type': 'text'}),
                (0, 0, {'type': 'video'}),
                (0, 0, {'type': 'image'}),
                (0, 0, {'type': 'file'}),
                (0, 0, {'type': 'link'}),
            ],
        })
        types = set(lesson.content_ids.mapped('type'))
        self.assertEqual(types, {'text', 'video', 'image', 'file', 'link'})

    def test_content_ordered_by_sequence(self):
        lesson = self.env['lms.lesson'].create({
            'name': 'Ordered Content',
            'module_id': self.module.id,
            'content_ids': [
                (0, 0, {'type': 'text', 'sequence': 3}),
                (0, 0, {'type': 'video', 'sequence': 1}),
                (0, 0, {'type': 'link', 'sequence': 2}),
            ],
        })
        contents = self.env['lms.lesson.content'].search([('lesson_id', '=', lesson.id)])
        sequences = contents.mapped('sequence')
        self.assertEqual(sequences, [1, 2, 3])

    # ------------------------------------------------------------------
    # 4. Data Integrity
    # ------------------------------------------------------------------

    def test_name_required(self):
        with self.assertRaises(Exception):
            self.env['lms.lesson'].create({'module_id': self.module.id})

    def test_cascade_delete_content_on_lesson_delete(self):
        lesson = self.env['lms.lesson'].create({
            'name': 'Lesson',
            'module_id': self.module.id,
            'content_ids': [(0, 0, {'type': 'text'})],
        })
        content_id = lesson.content_ids[0].id
        lesson.unlink()
        self.assertFalse(self.env['lms.lesson.content'].browse(content_id).exists())

    # ------------------------------------------------------------------
    # 5. Field Behaviour
    # ------------------------------------------------------------------

    def test_description_is_optional(self):
        lesson = self.env['lms.lesson'].create({
            'name': 'No Desc',
            'module_id': self.module.id,
        })
        self.assertFalse(lesson.description)

    def test_sequence_defaults_to_1_when_omitted(self):
        lesson = self.env['lms.lesson'].create({
            'name': 'Seq Default',
            'module_id': self.module.id,
        })
        self.assertEqual(lesson.sequence, 1)
