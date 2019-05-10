from django.conf import settings
from rest_framework import serializers


def validate_estimated_points(value):
    """
    Check that the entered estimated point is one of valid choices.
    """
    if value not in settings.STORY_POINT_CHOICES_LIST:
        raise serializers.ValidationError(["\"{}\" is not a valid choice.".format(value)])
    return value
