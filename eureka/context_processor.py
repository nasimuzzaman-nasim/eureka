from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


def get_basic_data(request):
    access = None
    if request.user.is_authenticated:
        try:
            access = request.session['access']
        except KeyError:
            refresh = RefreshToken.for_user(request.user)
            access = str(refresh.access_token)
            request.session['access'] = access

    per_page = settings.PER_PAGE
    return {
        'access': access,
        'per_page': per_page
    }