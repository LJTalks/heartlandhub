from django.contrib.auth.models import Group
from django.conf import settings
from .models import LegalDocument


# context_processor to pass legal docs to base footer
def legal_documents(request):
    return {
        'legal_documents': LegalDocument.objects.all()
    }


def add_is_tester(request):
    is_tester = False
    if request.user.is_authenticated:
        is_tester = request.user.groups.filter(name='testers').exists()
    return {'is_tester': is_tester}


def recaptcha_site_key(request):
    return {
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
    }


def support_email(request):
    return {
        'support_email': settings.SUPPORT_EMAIL
    }


# def database_context(request):
#     return {
#         'DATABASE_NAME': settings.DATABASE_NAME,
#         'SHOW_DEV_BANNER': settings.SHOW_DEV_BANNER,
#     }
