

def register_jinja(app, has_menu=False):
    result = {}
    result['static'] = static
    result['enumerate'] = enumerate
    result['len'] = len
    show_anaytics_script = True
    if app.debug or app.testing:
        show_anaytics_script = False
    result['show_anaytics_script'] = show_anaytics_script
    if has_menu:
        result['permission'] = permission
        result['menus'] = menus

    @app.context_processor
    def register_context():
        return result


def static(fa_folder, filename: str, is_default=False):
    if filename.startswith('/'):
        return filename
    return '/' + filename


def menus():
    return ""


def permission(endpoint):

    return ""


def register_data(app):
    with app.app_context() as c:
        print('register_data')
