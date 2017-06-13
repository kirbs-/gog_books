#!/Users/ckirby/.virtualenvs/gog_books/bin/python
from app import app

if __name__ == 'main':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
