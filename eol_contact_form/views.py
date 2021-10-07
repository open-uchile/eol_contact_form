# -*- coding: utf-8 -*-


from django.views.generic.base import View
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from django.conf import settings
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from itertools import cycle
import requests
import json


import logging
logger = logging.getLogger(__name__)

def _default_data():
    return {
        'form-name': '',
        'form-email': '',
        'form-type': '',
        'form-course': '',
        'form-message': '',
    }


class EolContactFormView(View):
    def get(self, request):
        help_desk_email = configuration_helpers.get_value(
            'EOL_CONTACT_FORM_HELP_DESK_EMAIL',
            settings.EOL_CONTACT_FORM_HELP_DESK_EMAIL)
        data = _default_data()

        # Fill course name in the form
        course_name = request.GET.get('course')
        if course_name is not None:
            data['form-type'] = 'course'
            data['form-course'] = course_name

        context = {
            'recaptcha_site_key': settings.EOL_CONTACT_FORM_RECAPTCHA_SITE_KEY,
            'help_desk_email': help_desk_email,
            'data': data,
        }
        return render(request, 'eol_contact_form/contact.html', context)

    def post(self, request):
        # Check method params
        if 'form-name' not in request.POST or 'form-email' not in request.POST or 'form-type' not in request.POST or 'form-course' not in request.POST or 'form-message' not in request.POST or 'g-recaptcha-response' not in request.POST:
            return HttpResponse(status=400)

        # Init with default values
        help_desk_email = configuration_helpers.get_value(
            'EOL_CONTACT_FORM_HELP_DESK_EMAIL',
            settings.EOL_CONTACT_FORM_HELP_DESK_EMAIL)
        context = {
            'recaptcha_site_key': settings.EOL_CONTACT_FORM_RECAPTCHA_SITE_KEY,
            'help_desk_email': help_desk_email,
            'data': _default_data(),
        }
        # Validate user form data
        validation = self.validate_data(request.POST)
        # If data is invalid, send error flag and form data
        if validation['error']:
            context['error'] = validation['error_attr']
            context['data'] = request.POST  # Update data with form values
            return render(request, 'eol_contact_form/contact.html', context)

        # Send success or email_error flag
        if self.send_contact_mail(request.user.username, request.POST):
            context['success'] = True
        else:
            context['send_email_error'] = True
            context['data'] = request.POST  # Update data with form values
        return render(request, 'eol_contact_form/contact.html', context)

    def validate_data(self, data):
        """
            Validate all form data
        """
        if data['form-name'].strip() == '':
            return {
                'error': True,
                'error_attr': _('Name')
            }
        if data['form-email'].strip() == '' or '@' not in data['form-email']:
            return {
                'error': True,
                'error_attr': _('Email')
            }
        if data['form-type'].strip() == '':
            return {
                'error': True,
                'error_attr': _('Category')
            }
        if data['form-course'].strip() == '' and data['form-type'] == 'course':
            return {
                'error': True,
                'error_attr': _('Course')
            }
        if data['form-message'].strip() == '':
            return {
                'error': True,
                'error_attr': _('Message')
            }
        if not self.validate_recaptcha(data['g-recaptcha-response']):
            return {
                'error': True,
                'error_attr': 'ReCAPTCHA'
            }
        return {
            'error': False
        }

    def validate_recaptcha(self, recaptcha):
        """
            Validate Google Recaptcha V2
        """
        url = 'https://www.google.com/recaptcha/api/siteverify'
        body = {
            'secret': settings.EOL_CONTACT_FORM_RECAPTCHA_SECRET_KEY,
            'response': recaptcha
        }
        r = requests.post(url, data=body)
        r_data = r.json()
        return r_data['success']

    def send_contact_mail(self, username, data):
        """
            Send contact mail to help desk
        """
        platform_name = configuration_helpers.get_value(
            'PLATFORM_NAME', settings.PLATFORM_NAME).upper()
        help_desk_email = configuration_helpers.get_value(
            'EOL_CONTACT_FORM_HELP_DESK_EMAIL',
            settings.EOL_CONTACT_FORM_HELP_DESK_EMAIL)
        email_data = {
            "user_name": data['form-name'].strip().upper(),
            "user_username" : username.upper(),
            "user_message": data['form-message'].strip(),
            "user_type_message": data['form-type'].upper(),
            "user_course": data['form-course'].strip().upper(),
            "platform_name": platform_name,
        }
        # Generate HTML Message with help_desk_email template
        html_message = render_to_string(
            'emails/help_desk_email.txt', email_data)
        plain_message = strip_tags(html_message)

        subject = '{} - {}'.format(data['form-type'].upper(), platform_name)
        reply_to = data['form-email']  # User email

        # Send Email with plain message
        email_message = EmailMultiAlternatives(
            subject,
            plain_message,
            from_email=help_desk_email,
            to=[help_desk_email],
            reply_to=[reply_to]
        )
        # Add alternative content type (HTML)
        email_message.attach_alternative(html_message, "text/html")
        # The return value will be the number of successfully delivered
        # messages (1 in this case)
        email = email_message.send()
        return True if email == 1 else False
