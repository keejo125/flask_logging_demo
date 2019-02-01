# -*- coding: utf-8 -*-
# author：zhengk
from app import create_app
from flask_script import Manager, Shell, Server

server = Server(host="0.0.0.0", threaded=True)
app = create_app('default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver", server)


if __name__ == '__main__':
    manager.run()
