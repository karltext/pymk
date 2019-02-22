from flask import Flask 
from flask import render_template

from models import db

from nodes import node_bp
from users import user_bp

app = Flask(__name__)

# add configurations
app.config.from_pyfile('settings.py')

# initialise database
with app.app_context():
    db.init_app(app)
    db.create_all()
    db.session.commit()

# register blueprints
app.register_blueprint(node_bp)
app.register_blueprint(user_bp)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)