from django.conf import settings

_default_conf = {
    "MODSHIB_SP_LOGOUT_URL": "/Shibboleth.sso/Logout",
    "MODSHIB_FORMS_TITLE": "Authentification",
    "MODSHIB_STYLESHEET_URL": None,
}

for k in _default_conf.keys():
    try:
        val = getattr(settings, k)
        _default_conf[k] = val
    except AttributeError:
        continue


def modshib_context(request):
    return _default_conf
