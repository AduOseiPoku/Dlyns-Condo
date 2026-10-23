from .models import PropertySetting


def property_settings(request):
    """
    Makes property contact info and branding available in every template.
    """
    settings = PropertySetting.get_settings()
    return {
        'property': settings,
    }
