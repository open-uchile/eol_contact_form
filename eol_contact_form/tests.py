# -*- coding: utf-8 -*-


from django.urls import reverse
from django.test import TestCase
from mock import patch

from collections import namedtuple
from django.utils.translation import ugettext as _
from openedx.core.djangoapps.site_configuration.tests.test_util import (
    with_site_configuration,
    with_site_configuration_context,
)

from . import views

test_config = {
    'PLATFORM_NAME': 'PLATFORM_NAME',
    'EOL_CONTACT_FORM_HELP_DESK_EMAIL': 'test@test.test'
}


class TestEolContactForm(TestCase):
    def setUp(self):

        super(TestEolContactForm, self).setUp()

    def test_render_page(self):
        """
            Test GET function
        """
        url = reverse('contact_form_view')
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)

    @patch("eol_contact_form.views.EolContactFormView.validate_recaptcha")
    def test_validate_data(self, validate_recaptcha):
        """
            Test data validation at backend
            > Patch validate_recaptcha. It will be tested at test_validate_recaptcha function
            1. Test without error
            2. Test with error in all fields
        """
        validate_recaptcha.side_effect = [True]
        data = {
            'form-name': 'test_name',
            'form-email': 'test_email@email.com',
            'form-type': 'course',
            'form-course': 'course_example',
            'form-message': 'message_text',
            'g-recaptcha-response': 'text_recaptcha'
        }
        result = views.EolContactFormView().validate_data(data)
        self.assertEqual(result['error'], False)

        validate_recaptcha.side_effect = [False]
        result = views.EolContactFormView().validate_data(data)
        self.assertEqual(result['error'], True)
        self.assertEqual(result['error_attr'], 'ReCAPTCHA')

        data['form-message'] = ''
        result = views.EolContactFormView().validate_data(data)
        self.assertEqual(result['error'], True)
        self.assertEqual(result['error_attr'], _('Message'))

        data['form-course'] = ''
        result = views.EolContactFormView().validate_data(data)
        self.assertEqual(result['error'], True)
        self.assertEqual(result['error_attr'], _('Course'))

        data['form-type'] = ''
        result = views.EolContactFormView().validate_data(data)
        self.assertEqual(result['error'], True)
        self.assertEqual(result['error_attr'], _('Category'))

        data['form-email'] = ''
        result = views.EolContactFormView().validate_data(data)
        self.assertEqual(result['error'], True)
        self.assertEqual(result['error_attr'], _('Email'))

        data['form-name'] = ''
        result = views.EolContactFormView().validate_data(data)
        self.assertEqual(result['error'], True)
        self.assertEqual(result['error_attr'], _('Name'))


    @patch("requests.post")
    def test_validate_recaptcha(self, post):
        """
            Test validate recaptcha from Google
            1. Success
            2. Fail
        """
        response = {
            "success": True,
            "challenge_ts": "timestamp",
            "hostname": "string",
        }
        post.side_effect = [
            namedtuple(
                "Request", [
                    "status_code", "json"])(
                200, lambda:response), ]
        result = views.EolContactFormView().validate_recaptcha('recaptcha')
        self.assertEqual(result, True)

        response = {
            "success": False,
            "challenge_ts": "timestamp",
            "hostname": "string",
        }
        post.side_effect = [
            namedtuple(
                "Request", [
                    "status_code", "json"])(
                200, lambda:response), ]
        result = views.EolContactFormView().validate_recaptcha('recaptcha')
        self.assertEqual(result, False)

    @with_site_configuration(configuration=test_config)
    @patch("django.core.mail.EmailMultiAlternatives.send")
    def test_send_contact_mail(self, send):
        """
            Test send contact mail
            1. Success
            2. Fail
        """
        data = {
            'form-name': 'test_name',
            'form-email': 'test_email@email.com',
            'form-type': 'course',
            'form-course': 'course_example',
            'form-message': 'message_text',
            'g-recaptcha-response': 'text_recaptcha'
        }
        send.side_effect = [1]
        result = views.EolContactFormView().send_contact_mail('username', data)
        self.assertEqual(result, True)

        send.side_effect = [0]
        result = views.EolContactFormView().send_contact_mail('username', data)
        self.assertEqual(result, False)

    @with_site_configuration(configuration=test_config)
    @patch("eol_contact_form.views.EolContactFormView.validate_recaptcha")
    @patch("eol_contact_form.views.EolContactFormView.send_contact_mail")
    def test_post(self, validate_recaptcha, send_contact_mail):
        """
            Test POST function
            1. Post success
            2. Validation error
            3. Send email error
            4. Post error (without all attributes)
        """
        validate_recaptcha.side_effect = [True]
        send_contact_mail.side_effect = [True]
        # Make Post
        data = {
            'form-name': 'test_name',
            'form-email': 'test_email@email.com',
            'form-type': 'course',
            'form-course': 'course_example',
            'form-message': 'message_text',
            'g-recaptcha-response': 'text_recaptcha'
        }
        response = self.client.post(reverse('contact_form_view'), data)
        content = response.content
        self.assertEqual(response.status_code, 200)
        self.assertIn('class="alert success"', content.decode('utf-8'))

        send_contact_mail.side_effect = [False]
        response = self.client.post(reverse('contact_form_view'), data)
        content = response.content
        self.assertEqual(response.status_code, 200)
        self.assertIn('class="alert error"', content.decode('utf-8'))