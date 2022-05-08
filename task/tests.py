from datetime import datetime

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from task.models import Department, Role, Project


class DepartmentRoleModelViewTest(TestCase):
    def setUp(self):
        department = Department.objects.create(id=1, name='test name', description='test desc')
        Role.objects.create(id=1,
                            department=department,
                            name='first role name',
                            is_header=True,
                            is_manager=False)
        Role.objects.create(id=2,
                            department=department,
                            name='second role name',
                            is_header=False,
                            is_manager=True)

    def test_department_model(self):
        dep = Department.objects.get(id=1)
        url_for_dep = reverse('department-detail', kwargs={'pk': dep.pk})
        self.assertTrue(isinstance(dep, Department))
        self.assertEqual(dep.__str__(), dep.name)
        self.assertEqual(dep.get_absolute_url(), url_for_dep)

    def test_role_model(self):
        role = Role.objects.get(id=1)
        self.assertTrue(isinstance(role, Role))
        self.assertTrue(isinstance(role.department, Department))
        self.assertEqual(role.__str__(), role.name)

    def test_department_list_view(self):
        resp = self.client.get('/task/departments/')
        dep = Department.objects
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'task/department_list.html')
        self.assertEqual(len(resp.context['department_list']), dep.count())
        self.assertEqual(resp.context['department_list'][0], dep.get(id=1))

    def test_department_detail_view(self):
        resp = self.client.get('/task/departments/1/')
        dep = Department.objects.get(id=1)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'task/department_detail.html')
        self.assertEqual(resp.context['department'].name, 'test name')
        self.assertEqual(len(resp.context['roles']), dep.roles.count())
        self.assertEqual(resp.context['roles'][0], dep.roles.get(id=1))

    def tearDown(self):
        Role.objects.get(id=1).delete()
        Role.objects.get(id=2).delete()
        Department.objects.get(id=1).delete()


class ProjectModelTest(TestCase):
    def setUp(self):
        planned_date = timezone.now() + timezone.timedelta(days=7)
        user = get_user_model().objects.create(id=1,
                                               email='test@test.ru',
                                               first_name='test name',
                                               last_name='test name')
        Project.objects.create(id=1,
                            manager=user,
                            name='test name',
                            planned_date=planned_date,
                            priority='High'
                            )

    def test_project_model(self):
        project = Project.objects.get(id=1)
        self.assertTrue(isinstance(project, Project))
        self.assertTrue(isinstance(project.manager, get_user_model()))
        self.assertEqual(project.__str__(), f'Project:{project.name}, status: {project.status}')
        self.assertEqual(project.status, 'In work')

    def test_project_change_status(self):
        project = Project.objects.get(id=1)
        project.change_status(new_status='Finished')
        self.assertEqual(project.finish_date.strftime("%Y-%m-%d %H:%M:%S"),
                         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def tearDown(self):
        Project.objects.get(id=1).delete()