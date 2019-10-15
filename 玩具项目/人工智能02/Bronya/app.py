from flask import Flask, render_template
from serv.Content import content
from serv.Users import user
from serv.star_bear import sbe

app = Flask(__name__)
app.debug = True
app.register_blueprint(content)
app.register_blueprint(user)
app.register_blueprint(sbe)


@app.route('/WebToy')
def web():
    return render_template('WebToy.html')


if __name__ == '__main__':
    app.run('0.0.0.0',5000)