from flask import Flask, render_template
import os
from views.alerts import alert_blueprint
from views.stores import store_blueprint
from views.users import user_blueprint
from dotenv import load_dotenv
from lib.mailgun import Mailgun

app = Flask(__name__)
app.secret_key = os.urandom(64)

app.config.update(
    ADMIN=os.getenv('ADMIN')
)
load_dotenv()


@app.route('/')
def home():
    return render_template("home.html")


print(Mailgun.send_mail(['r_deeksha@gmail.com'],
                        'Hello',
                        "this is a test.",
                        '<p>This is a html test.</p>'
                        ))
# flask will automatically read the .env final
app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix='/users')
if __name__ == "__main__":
    app.run(debug=True)
