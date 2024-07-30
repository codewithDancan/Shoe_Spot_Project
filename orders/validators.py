from django.core.exceptions import ValidationError


def validate_unique_country_name(value):
    from .models import Country

    if Country.objects.filter(name__iexact=value).exists():
        raise ValidationError("A country with this name already exists.")


def validate_unique_city_name(value, country=None):
    from .models import City

    if country is None:
        return  # Skip validation if country_id is not set
    if City.objects.filter(name__iexact=value, country=country).exists():
        raise ValidationError("A city with this name already exists in this country.")
