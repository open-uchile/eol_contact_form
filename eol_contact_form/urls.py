

from django.conf.urls import url
from django.conf import settings

from .views import EolContactFormView


urlpatterns = (
    url(
        r'contact_form$',
        EolContactFormView.as_view(),
        name='contact_form_view',
    ),
)
