import django.test
from projtrack.models import Client, Project, Type, User, Department
import re


class DepartmentTestCase(django.test.TestCase):
    def setUp(self):
        Department.objects.create(name="A")
        Department.objects.create(name="B")

    def test_departments(self):
        a = Department.objects.get(name="A")
        b = Department.objects.get(name="B")
        self.assertEqual(a.name, "A")
        self.assertEqual(b.name, "B")


class ClientTestCase(django.test.TestCase):
    def setUp(self):
        Client.objects.create(first_name="Ralph",
                last_name="Smith",
                email="rsmith@email.com",
                department=Department.objects.create(name="Literature"))
        Client.objects.create(first_name="Jill",
                last_name="Jackson",
                email="jjackson@email.com",
                department=Department.objects.create(name="Science"))
        c = Client()
        c.first_name = "Jeff"
        c.last_name = "Guy"
        c.email = "jguy@email.com"
        c.department = Department.objects.create(name="Math")
        c.save()

    def test_check_objects_email(self):
        ralph = Client.objects.get(first_name="Ralph")
        jill = Client.objects.get(first_name="Jill")
        jeff = Client.objects.get(first_name="Jeff")
        self.assertEqual(ralph.email, "rsmith@email.com")
        self.assertEqual(jill.email, "jjackson@email.com")
        self.assertEqual(jeff.email, "jguy@email.com")

    def test_check_objects_last_name(self):
        ralph = Client.objects.get(first_name="Ralph")
        jill = Client.objects.get(first_name="Jill")
        jeff = Client.objects.get(first_name="Jeff")
        self.assertEqual(ralph.last_name, "Smith")
        self.assertEqual(jill.last_name, "Jackson")
        self.assertEqual(jeff.last_name, "Guy")


class ProjectTestCase(django.test.TestCase):
    def setUp(self):
        u = User()
        u.username = "techconbob"
        u.save()
        Type.objects.create(name="Test")
        Department.objects.create(name="Science")
        Client.objects.create(first_name="Ralph", last_name="Smith",
                              email="rsmith@email.com",
                              department=Department.objects.get(name="Science"))
        Project.objects.create(title="Test Project",
                               description="A project to test the application.",
                               type=Type.objects.get(name="Test"),
                               walk_in=False,
                               client=Client.objects.get(first_name="Ralph"),
                               users=User.objects.get(username="techconbob"))

    def test_user(self):
        p = Project.objects.get(title="Test Project")
        self.assertEqual(p.users.username, "techconbob")

    def test_department(self):
        p = Project.objects.get(title="Test Project")
        self.assertEqual(p.client.department.name, "Science")

    def test_description(self):
        p = Project.objects.get(title="Test Project")
        self.assertEqual(p.description, "A project to test the application.")

    def test_type(self):
        p = Project.objects.get(title="Test Project")
        self.assertEqual(p.type.name, "Test")

    def test_client(self):
        p = Project.objects.get(title="Test Project")
        self.assertEqual(p.client.email, "rsmith@email.com")


class TestDepartmentForm(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()
        self.client.login(username="test", password="techcon589")

    def test_department_form(self):
        self.client.post("/add_department/", {'name': 'test'})
        dept = Department.objects.get(name='test')
        self.assertEqual(dept.name, 'test')

    def test_redirect(self):
        response = self.client.post("/add_department/", {'name': 'test'},
                                    follow=True)
        self.assertContains(response, "Add Department", status_code=200)


class TestClientForm(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()
        self.client.login(username="test", password="techcon589")

    def test_client_form(self):
        Department.objects.create(name="Test")
        self.client.post("/add_client/", {'first_name': "Bob",
                                          'last_name': "Roberts",
                                          'email': "roberts@email.com",
                                          'department': Department.objects.get(name="Test")})

    def test_redirect(self):
        response = self.client.post("/add_client/", {'first_name': "Bob",
                                    'last_name': "Roberts",
                                                     'email': "roberts@email.com",
                                                     'department': Department.objects.get(name="Test")})
        self.assertContains(response, "Add Client", status_code=200)
