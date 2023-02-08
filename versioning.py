from resources.book import blp_v1 as BookBlueprint_v1
from resources.book import blp_v2 as BookBlueprint_v2

from resources.author import blp_v1 as AuthorBlueprint_v1
from resources.work import blp_v1 as WorkBlueprint_v1
from resources.olib_book import blp_v1 as OlibBlueprint_v1
from resources.user import blp_v1 as UserBlueprint_v1

from resources.rules import blp_rules



def register_blueprints(api):
    api.register_blueprint(blp_rules)

    api.register_blueprint(BookBlueprint_v1, url_prefix='/v1')
    api.register_blueprint(BookBlueprint_v2, url_prefix='/v2')
    api.register_blueprint(BookBlueprint_v2, url_prefix='/', name='Books-latest')


    api.register_blueprint(AuthorBlueprint_v1, url_prefix='/v1')
    api.register_blueprint(AuthorBlueprint_v1, url_prefix='/', name='Authors-latest')

    api.register_blueprint(WorkBlueprint_v1, url_prefix='/v1')
    api.register_blueprint(WorkBlueprint_v1, url_prefix='/', name='Works-latest')

    api.register_blueprint(OlibBlueprint_v1, url_prefix='/v1')
    api.register_blueprint(OlibBlueprint_v1, url_prefix='/', name='OlibBooks-latest')

    api.register_blueprint(UserBlueprint_v1, url_prefix='/v1')
    api.register_blueprint(UserBlueprint_v1, url_prefix='/', name='UserBlueprint-latest')
