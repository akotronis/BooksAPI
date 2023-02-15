from flask import current_app as app
from flask_smorest import Blueprint


blp_rules = Blueprint("Rules", __name__)

@blp_rules.route('/rules')
def root():
    # expose rule, endpoint, methods attributes
    rules = [repr(rules) for rules in app.url_map.iter_rules()]
    return rules