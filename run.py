from app import create_app, db
from app.models import User
from flask import url_for
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand, upgrade

app = create_app()

Migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:30s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print line

if __name__ == '__main__':
	manager.run()
