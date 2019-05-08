import shortuuid

from django.conf import settings


def generate_short_uuid():
    shortuuid.set_alphabet(settings.SUID_ALPHABET)
    suid = shortuuid.ShortUUID().random(length=settings.SUID_LENGTH)
    return suid
