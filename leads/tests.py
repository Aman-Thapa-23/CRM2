from django.test import TestCase
from django.shortcuts import reverse
# Create your tests here.

class LandingPageTest(TestCase):

    def Test_status_code(self):
        #TODO some sord of test
        response=self.client.get(reverse("landing_page"))
        self.assertEqual(response.status_code, 200)

    # def Test_template_name(self):
    #     #TODO some sord of test
    #     pass