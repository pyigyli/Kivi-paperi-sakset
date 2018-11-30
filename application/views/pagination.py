from application import app
from flask import request, url_for

def url_for_other_page(page):                                       # Used to navigate lists that have
    args = request.view_args.copy()                                 # so many rows that they must be
    args['page'] = page                                             # split into multiple pages
    return url_for(request.endpoint, **args)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page    # Global variable used in hmtl-code