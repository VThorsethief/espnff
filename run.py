from bin.startup import app
# Runs the application and attaches the stylesheet.

server = app.server
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/brPBPO.css 39'})

if __name__ == '__main__':
    app.run_server()
