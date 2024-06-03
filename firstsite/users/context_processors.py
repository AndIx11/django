from mysite.utils import menu


def get_mysite_context(request):
    return {'mainmenu': menu}
