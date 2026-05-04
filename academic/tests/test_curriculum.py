from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from accounts.models import Institution, AcademicYear
from academic.models import Course, Topic, TopicMaterial

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
