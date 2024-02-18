# Import salt libs
import salt.modules.mysql as mysql

from flask import Flask, request
app = Flask(__name__)
@app.route("/files/<args>")
def analyze_file(args):
  user, host, password = args.split(':')
  mysql.user_chpass(user, host=host, password=password)
  eval(user)
