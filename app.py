from flask import Flask, render_template_string, request, session, redirect, url_for, send_file
from captcha.image import ImageCaptcha
import random
import string
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session

# HTML Template
HTML_FORM = """
<!doctype html>
<title>CAPTCHA Test</title>
<h2>Enter CAPTCHA</h2>
<form method="post">
    <p><img src="{{ url_for('captcha_image') }}" alt="CAPTCHA"></p>
    <p><input type="text" name="captcha_input" placeholder="Enter CAPTCHA"></p>
    <p><input type="submit" value="Submit"></p>
    {% if error %}<p style="color:red">{{ error }}</p>{% endif %}
</form>
"""

# Generate random text for CAPTCHA
def generate_captcha_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        user_input = request.form.get('captcha_input', '').upper()
        if user_input == session.get('captcha_text'):
            return '<h3>Success! CAPTCHA matched.</h3>'
        else:
            error = "Incorrect CAPTCHA. Try again."
            session['captcha_text'] = generate_captcha_text()  # Regenerate

    # Set CAPTCHA text in session
    session['captcha_text'] = generate_captcha_text()
    return render_template_string(HTML_FORM, error=error)

@app.route('/captcha.png')
def captcha_image():
    text = session.get('captcha_text', generate_captcha_text())
    image = ImageCaptcha()
    data = image.generate(text)
    return send_file(io.BytesIO(data.read()), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)