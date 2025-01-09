from flask import Blueprint, render_template, request, jsonify
import markdown
from flask_login import login_required, current_user
from .models import db, Users
from .robot import check_profile_as_admin
import requests as actual_requests

profile = Blueprint('profile', __name__, template_folder='../frontend')


@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def show():
    rendered_markdown = ""
    if request.method == 'POST' and not current_user.admin:
        markdown_text = request.form['markdown']
        rendered_markdown = markdown.markdown(markdown_text)

        current_user.markdown = markdown_text
        db.session.commit()

    if current_user.markdown:
        rendered_markdown = markdown.markdown(current_user.markdown)

    return render_template('profile.html', rendered_markdown=rendered_markdown, is_admin=current_user.admin)


@profile.route('/profile/<uuid>', methods=['GET'])
@login_required
def view_profile(uuid):
    if not current_user.admin:
        return render_template('404.html')

    user = Users.query.filter_by(uuid=uuid).first_or_404()
    rendered_markdown = markdown.markdown(user.markdown) if user.markdown else ""
    return render_template('profile.html', rendered_markdown=rendered_markdown, username=user.username)


# Add a new route to handle chat messages
@profile.route('/chatbot', methods=['POST'])
@login_required
def chatbot():
    user_message = request.json.get('message', '').lower()

    responses = {
        "hello": "Hello! I am the administrator of this site. How can I assist you today?",
        "help": "Sure! Let me know what you need help with.\n"
                " I can do alot like:\n"
                "Ask me for a joke, or to rate your profile!",
        "joke": actual_requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"}).json().get("joke"),
        "rate my profile": "Wow this profile is amazing!",
    }
    if "flag" in user_message:
        user_message = "joke"

    if "help" in user_message:
        user_message = "help"

    if "joke" in user_message:
        user_message = "joke"

    if "rate my profile" in user_message or "my profile" in user_message:
        check_profile_as_admin(current_user.uuid)
        user_message = "rate my profile"

    robot_response = responses.get(user_message, "I'm sorry, I don't understand that. Ask my for help")

    return jsonify({"response": robot_response})
