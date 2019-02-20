from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

	def setUp(self): #setUp function runs before every test that we run as sometimes there are setUp tasks that need to be run before running tests.
		self.client = Client() #creating a test Client
		self.admin_user = get_user_model().objects.create_superuser(
				email='admin@gmail.com',
				password='password123'
			) # adding a new admin_user that we can use to test
		self.client.force_login(self.admin_user) #making sure that admin_user is logged into the client using force_login helper function of Client
		self.user = get_user_model().objects.create_user(
				email='test@gmail.com',
				password='password123',
				name='Test user full name'
			) #spare user we can use for testing listing of things in our app


	def test_user_listed(self): #Tests that users are listed on the user page of django admin
		url = reverse('admin:core_user_changelist')
		response = self.client.get(url)

		self.assertContains(response, self.user.name) #assertContains checks that if our response contains a certain item.It also checks actual contents of the response not just as an object but actual data/output,also makes sure that http response was http 200
		self.assertContains(response, self.user.email)


	def test_user_change_page(self): #Test that the user edit page works
		url = reverse('admin:core_user_change', args=[self.user.id]) # /admin/core/user/<id> so anything we pass in args will get assigned to args to user id.
		response = self.client.get(url)

		self.assertEqual(response.status_code, 200) #making sure that response is http 200

	def test_create_user_page(self): #Test that the create user page works
		url = reverse('admin:core_user_add')
		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)