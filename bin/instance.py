from flask import Flask
from flask import request
from dash import Dash
from flask import request

server = Flask('pilot')
# @server.route('/', methods = ['GET', 'POST'])
# def index():
#     # request.cookies.get("swid")
#     cookies = request.cookies
#     if 'espn.com' in request.cookies:
#         message = request.cookies.get('espn.com')
#     else:
#         message = 'None Found'
#     return message
app = Dash(server=server)

app.config['suppress_callback_exceptions']=True
