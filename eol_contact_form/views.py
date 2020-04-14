# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import View
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.conf import settings

import logging
logger = logging.getLogger(__name__)


class EolContactFormView(View):
    def get(self, request):
        context = {}
        return render(request, 'eol_contact_form/contact.html', context)
