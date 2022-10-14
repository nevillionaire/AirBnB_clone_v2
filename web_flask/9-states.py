'''Displays the following routes:
/states
/states/<id>
'''
from flask import Flask, render_template
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states')
def states():
    '''returns list of states'''
    states = list(storage.all('State').values())
    return render_template('9-states.html', states=states)

@app.route('/states/<id>')
def state(id):
    '''returns single state'''
    state = None
    for v in storage.all('State').values():
        if v.id == id:
            state = v
    return render_template('9-states.html', state=state)

@app.teardown_appcontext
def teardown(self):
    '''delete sqlalchemy session after each request'''
    storage.close()


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
