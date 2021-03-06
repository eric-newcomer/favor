from django.test import TestCase
from tests.factories import *
from django.urls import reverse

class GiveOnHomeViewTests(TestCase):
   @classmethod
   def setUpTestData(cls):
      print("Running FavorGiveViewTest...")
      cls.url = "/"
      user = UserFactory()
      user.save()
      favor = FavorFactory(owner=user)
      favor.save()
      cls.user = user
      cls.favor = favor


   def setUp(self):
      self.client.login(
         username=self.user.username, password='password'
      )
      
   
   def test_view_url_exists(self):
      expected_status_code = 200

      response = self.client.get(self.url)

      self.assertEqual(expected_status_code, response.status_code)


   def test_view_redirects_on_not_logged_in(self):
      expected_status_code = 302
      expected_redirect_url = reverse('login') + "?next=/"

      self.client.logout()
      response = self.client.get(self.url)

      self.assertEqual(expected_status_code, response.status_code)
      self.assertEqual(expected_redirect_url, response.url)


   def test_view_uses_base_template(self):
      expected_status_code = 200
      expected_template = "base.html"

      response = self.client.get(self.url)

      self.assertEqual(expected_status_code, response.status_code)
      self.assertTemplateUsed(response, expected_template)


   def test_view_uses_own_template(self):
      expected_status_code = 200
      expected_template = "home.html"

      response = self.client.get(self.url)

      self.assertEqual(expected_status_code, response.status_code)
      self.assertTemplateUsed(response, expected_template)


   def test_view_can_signup_for_favor(self):
      expected_status_code = 200
      expected_template = "home.html"

      response = self.client.post(self.url, {
         'card_id' : self.favor.id
      })

      self.assertEqual(expected_status_code, response.status_code)
      self.assertTemplateUsed(response, expected_template)