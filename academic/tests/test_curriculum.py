import sys
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from accounts.models import Institution, AcademicYear
from academic.models import Course, Topic, TopicMaterial

# Python 3.14 + Django 5.0 compatibility: copy(super()) is broken in Py3.14.
# Patch BaseContext.__copy__ to use object.__new__ instead.
if sys.version_info >= (3, 14):
    from django.template.context import BaseContext

    def _base_context_copy(self):
        duplicate = object.__new__(type(self))
        duplicate.__dict__.update(self.__dict__)
        duplicate.dicts = self.dicts[:]
        return duplicate

    BaseContext.__copy__ = _base_context_copy

User = get_user_model()


def make_teacher(username='teacher1'):
    return User.objects.create_user(
        username=username, email=f'{username}@test.com',
        password='pass123', role='docente',
        first_name='Juan', last_name='Docente',
    )


def make_institution():
    return Institution.objects.create(name='Colegio Test', slug='colegio-test', is_active=True)


def make_academic_year(institution):
    return AcademicYear.objects.create(
        institution=institution, name='2026', year=2026,
        start_date='2026-01-01', end_date='2026-12-31',
    )


def make_course(institution, academic_year, teacher):
    return Course.objects.create(
        institution=institution,
        academic_year=academic_year,
        teacher=teacher,
        name='Matemáticas',
        slug='matematicas',
    )


class TopicModelTest(TestCase):
    def setUp(self):
        self.teacher = make_teacher()
        self.inst = make_institution()
        self.year = make_academic_year(self.inst)
        self.course = make_course(self.inst, self.year, self.teacher)

    def test_create_topic(self):
        topic = Topic.objects.create(
            course=self.course, title='Ecuaciones lineales', order=1,
        )
        self.assertEqual(topic.title, 'Ecuaciones lineales')
        self.assertEqual(topic.course, self.course)
        self.assertFalse(topic.is_published)

    def test_topic_str(self):
        topic = Topic.objects.create(course=self.course, title='Álgebra', order=1)
        self.assertIn('Álgebra', str(topic))

    def test_topic_ordering(self):
        Topic.objects.create(course=self.course, title='B', order=2)
        Topic.objects.create(course=self.course, title='A', order=1)
        titles = list(Topic.objects.filter(course=self.course).values_list('title', flat=True))
        self.assertEqual(titles, ['A', 'B'])

    def test_create_material_with_url(self):
        topic = Topic.objects.create(course=self.course, title='Álgebra', order=1)
        mat = TopicMaterial.objects.create(
            topic=topic, title='Video explicativo',
            material_type='link', url='https://example.com/video',
        )
        self.assertEqual(mat.topic, topic)
        self.assertEqual(mat.material_type, 'link')

    def test_material_file_type_requires_file(self):
        topic = Topic.objects.create(course=self.course, title='Tema', order=1)
        mat = TopicMaterial(topic=topic, title='Sin archivo', material_type='file')
        with self.assertRaises(ValidationError):
            mat.full_clean()

    def test_material_link_type_requires_url(self):
        topic = Topic.objects.create(course=self.course, title='Tema', order=1)
        mat = TopicMaterial(topic=topic, title='Sin URL', material_type='link')
        with self.assertRaises(ValidationError):
            mat.full_clean()


class CourseDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = make_teacher('teacher2')
        self.student = User.objects.create_user(
            username='student1', email='student1@test.com',
            password='pass123', role='estudiante',
            first_name='Ana', last_name='S',
        )
        self.inst = make_institution()
        self.year = make_academic_year(self.inst)
        self.course = make_course(self.inst, self.year, self.teacher)
        from academic.models import Enrollment
        Enrollment.objects.create(course=self.course, student=self.student, status='active')
        Topic.objects.create(course=self.course, title='Tema 1', order=1, is_published=True)
        Topic.objects.create(course=self.course, title='Tema borrador', order=2, is_published=False)

    def test_teacher_sees_all_topics(self):
        self.client.login(username='teacher2', password='pass123')
        response = self.client.get(f'/cursos/{self.course.id}/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('Tema 1', content)
        self.assertIn('Tema borrador', content)

    def test_student_sees_only_published(self):
        self.client.login(username='student1', password='pass123')
        response = self.client.get(f'/cursos/{self.course.id}/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('Tema 1', content)
        self.assertNotIn('Tema borrador', content)

    def test_unenrolled_student_gets_403(self):
        other_student = User.objects.create_user(
            username='student2', email='student2@test.com',
            password='pass123', role='estudiante',
            first_name='Pedro', last_name='O',
        )
        self.client.login(username='student2', password='pass123')
        response = self.client.get(f'/cursos/{self.course.id}/')
        self.assertEqual(response.status_code, 403)


class TopicDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = make_teacher('teacher3')
        self.student = User.objects.create_user(
            username='student3', email='student3@test.com',
            password='pass123', role='estudiante',
            first_name='Luis', last_name='S',
        )
        self.inst = make_institution()
        self.year = make_academic_year(self.inst)
        self.course = make_course(self.inst, self.year, self.teacher)
        from academic.models import Enrollment
        Enrollment.objects.create(course=self.course, student=self.student, status='active')
        self.topic_pub = Topic.objects.create(
            course=self.course, title='Publicado', order=1,
            is_published=True, description='Contenido del tema',
        )
        self.topic_draft = Topic.objects.create(
            course=self.course, title='Borrador', order=2, is_published=False,
        )
        TopicMaterial.objects.create(
            topic=self.topic_pub, title='Doc PDF',
            material_type='link', url='https://example.com/doc.pdf',
        )

    def test_teacher_sees_draft_topic(self):
        self.client.login(username='teacher3', password='pass123')
        response = self.client.get(f'/temas/{self.topic_draft.id}/')
        self.assertEqual(response.status_code, 200)

    def test_student_cannot_see_draft(self):
        self.client.login(username='student3', password='pass123')
        response = self.client.get(f'/temas/{self.topic_draft.id}/')
        self.assertEqual(response.status_code, 403)

    def test_student_sees_published_with_materials(self):
        self.client.login(username='student3', password='pass123')
        response = self.client.get(f'/temas/{self.topic_pub.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Doc PDF')


class TopicCreateEditViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = make_teacher('teacher4')
        self.other_teacher = make_teacher('teacher5')
        self.inst = make_institution()
        self.year = make_academic_year(self.inst)
        self.course = make_course(self.inst, self.year, self.teacher)

    def test_teacher_can_create_topic(self):
        self.client.login(username='teacher4', password='pass123')
        response = self.client.post(f'/cursos/{self.course.id}/temas/nuevo/', {
            'title': 'Nuevo tema',
            'description': 'Desc',
            'order': 1,
            'is_published': False,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Topic.objects.filter(course=self.course, title='Nuevo tema').exists())

    def test_other_teacher_cannot_create(self):
        self.client.login(username='teacher5', password='pass123')
        response = self.client.post(f'/cursos/{self.course.id}/temas/nuevo/', {
            'title': 'Hack', 'order': 1,
        })
        self.assertEqual(response.status_code, 403)

    def test_teacher_can_edit_topic(self):
        topic = Topic.objects.create(course=self.course, title='Original', order=1)
        self.client.login(username='teacher4', password='pass123')
        response = self.client.post(f'/temas/{topic.id}/editar/', {
            'title': 'Editado',
            'description': '',
            'order': 1,
            'is_published': True,
        })
        self.assertEqual(response.status_code, 302)
        topic.refresh_from_db()
        self.assertEqual(topic.title, 'Editado')
        self.assertTrue(topic.is_published)


class MaterialUploadViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = make_teacher('teacher6')
        self.inst = make_institution()
        self.year = make_academic_year(self.inst)
        self.course = make_course(self.inst, self.year, self.teacher)
        self.topic = Topic.objects.create(
            course=self.course, title='Tema con materiales', order=1, is_published=True,
        )

    def test_teacher_can_add_link_material(self):
        self.client.login(username='teacher6', password='pass123')
        response = self.client.post(f'/temas/{self.topic.id}/materiales/subir/', {
            'title': 'Video YouTube',
            'material_type': 'link',
            'url': 'https://youtube.com/watch?v=abc123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            TopicMaterial.objects.filter(topic=self.topic, title='Video YouTube').exists()
        )

    def test_non_teacher_cannot_upload(self):
        student = User.objects.create_user(
            username='student6', email='student6@test.com',
            password='pass123', role='estudiante',
            first_name='X', last_name='Y',
        )
        self.client.login(username='student6', password='pass123')
        response = self.client.post(f'/temas/{self.topic.id}/materiales/subir/', {
            'title': 'Hack', 'material_type': 'link', 'url': 'https://bad.com',
        })
        self.assertEqual(response.status_code, 403)
