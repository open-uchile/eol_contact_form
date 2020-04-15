# EOL CONTACT FORM

New Page for Open Edx LMS (EOL) with a contact form

# Install

    docker-compose exec lms pip install -e /openedx/requirements/eol_contact_form

# Configuration

To enable [Google ReCAPTCHA v2](https://www.google.com/recaptcha/) Edit *production.py* in *lms settings* and add your own keys.

    EOL_CONTACT_FORM_RECAPTCHA_SITE_KEY = AUTH_TOKENS.get('EOL_CONTACT_FORM_RECAPTCHA_SITE_KEY', '')
    EOL_CONTACT_FORM_RECAPTCHA_SECRET_KEY = AUTH_TOKENS.get('EOL_CONTACT_FORM_RECAPTCHA_SECRET_KEY', '')

# Screenshots
*Last Update 15/04/2020*

<p align="center">
<img width="600" src="examples/lms_form.png">
</p>