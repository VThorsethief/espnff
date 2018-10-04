from bin import (league, graphs)
import browser_cookie3 as bc
import datetime
from flask import request
try:
    cookie_data = bc.load(domain_name='espn.com')
    swid = cookie_data._cookies['.espn.com']['/']['SWID'].value
    espn2 = cookie_data._cookies['.espn.com']['/']['espn_s2'].value
except KeyError:
    swid = request.cookies.get('SWID')
    espn2 = request.cookies.get('espn_s2')
year = datetime.datetime.today().year
myLeague = league.League(year,espn_s2=espn2,swid=swid)

board = graphs.DashBoard(myLeague)