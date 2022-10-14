'''Displays list of states'''
from flask import Flask, render_template
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list')
def states_list():
    '''returns list of states'''
    states = list(storage.all('State').values())
    return render_template('7-states_list.html', states=states)

@app.teardown_appcontext
def teardown(self):
    '''delete sqlalchemy session after each request'''
    storage.close()


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
