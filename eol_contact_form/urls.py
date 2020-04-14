from __future__ import absolute_import

from django.conf.urls import url
from django.conf import settings

from .views import EolContactFormView


urlpatterns = (
    url(
        r'contact_form$'.format(
            settings.COURSE_ID_PATTERN,
        ),
        EolContactFormView.as_view(),
        name='contact_form_view',
    ),
)
