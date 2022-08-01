from django.contrib.auth import authenticate, models
from django.test import Client, TestCase


class ViewPagesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = models.User.objects.create_user(username='testname', password='P@ssw0rd')

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signin(self):
        response = self.client.get('/signin/')
        self.assertEqual(response.status_code, 200)

    def test_signout(self):
        response = self.client.get('/signout/')
        self.assertRedirects(response, '/signin/?next=/signout/')

    def test_profile(self):
        response = self.client.get('/profile/')
        self.assertRedirects(response, '/signin/?next=/profile/')

    def test_login(self):
        response = self.client.post('/signin/', {'username': 'testname', 'password': 'P@aaw0rd'})
        self.assertTrue(models.User.is_authenticated)
        self.client.login()
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/signout/')
        self.assertRedirects(response, '/')
        self.client.logout()

    async def test_wrong_login(self):
        response = self.client.post('/signin/', {'username': 'wrongtest', 'password': 'P@ssw0rd'})
        self.assertFalse(models.User.is_authenticated)
        response = self.client.post('/signin/', {'username': 'testname', 'password': 'incorrect'})
        self.assertEqual(response.status_code, 200)


class AuthTest(TestCase):
    def setUp(self):
        self.user = models.User.objects.create_user(username='testname', password='P@ssw0rd')
        self.client = Client()

    def test_correct(self):
        user = authenticate(username='testname', password='P@ssw0rd')
        self.assertTrue(user is not None and user.is_authenticated)
        response = self.client.get('/signin/')
        self.assertEqual(response.status_code, 200)

    def test_wrong_username(self):
        user = authenticate(username='test', password='testPassword')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='testuser', password='test1234')
        self.assertFalse(user is not None and user.is_authenticated)
