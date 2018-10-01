print('instance')
from flask import Flask
from dash import Dash

server = Flask('pilot')
app = Dash(server=server)

app.config['suppress_callback_exceptions']=True
