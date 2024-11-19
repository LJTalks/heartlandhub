from django.utils.safestring import mark_safe


def obfuscate_email(email):
    """Converts an email address into HTML character entities for obfuscation."""
    if not email:
        return ""
    obfuscated = ''.join(['&#{};'.format(ord(char)) for char in email])
    return mark_safe(obfuscated)  # Mark as safe for HTML rendering


def obfuscate_phone(phone):
    """Converts a phone number into HTML character entities for obfuscation."""
    if not phone:
        return ""
    obfuscated = ''.join(['&#{};'.format(ord(char)) for char in phone])
    return mark_safe(obfuscated)  # Mark as safe for HTML rendering
