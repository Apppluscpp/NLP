from flask import Flask, render_template, redirect, url_for, request
from views import views
import os
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # Use the appropriate port for your mail server
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'ykpang-wp21@student.tarc.edu.my'
app.config['MAIL_PASSWORD'] = 'Pang1248757##'
app.config['MAIL_DEFAULT_SENDER'] = 'ykpang-wp21@student.tarc.edu.my'  # Set a default sender

# Initialize the Mail object
mail = Mail()
mail.init_app(app)

app.register_blueprint(views, url_prefix="/views")

app.secret_key = "123"

if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact_us", methods=["GET", "POST"])
def contact_us():
    if request.method == "POST":
        # Process the form data and send email
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        feedback = request.form.get("feedback")

        # Send email
        send_email(name, email, phone, feedback)

        return "Feedback sent successfully!"

    return render_template("contact_us.html")

def send_email(name, email, phone, feedback):
    # Create a Message object
    subject = 'New Feedback'
    body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nFeedback: {feedback}"
    recipients = ['ykpang-wp21@student.tarc.edu.my']

    message = Message(subject=subject, body=body, recipients=recipients)

    try:
        # Send the message using the 'mail' object
        mail.send(message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
