# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.test import TestCase


class TestEolContactForm(TestCase):
    def setUp(self):

        super(TestEolContactForm, self).setUp()

    def test_render_page(self):
        url = reverse('contact_form_view')
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)