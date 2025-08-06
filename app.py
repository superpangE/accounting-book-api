from flask import Flask
from flask_cors import CORS
import re
from config.database import db, init_db
from controllers.accounting_book_controller import accounting_book_bp
from controllers.shared_schedule_controller import shared_schedule_bp
from models.alarm import Alarm # Import Alarm model to ensure table creation

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": re.compile(r"^https?://[^/]+\.dotgae\.com$")}})
# Initialize database
init_db(app)

# Register blueprints
app.register_blueprint(accounting_book_bp)
app.register_blueprint(shared_schedule_bp)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5006)