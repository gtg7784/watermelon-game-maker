from flask import Flask, render_template, request, abort
from utils import save_img, make_game
from vercel import deploy

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uuid = request.headers.get('uuid')
    email = request.form.get('email')
    data = request.files
    path = save_img(uuid, data)
    completed = make_game(path, email)

    if not completed:
        abort(500)
    
    url = deploy(email, uuid)
    return {
        'url': url
    }

if __name__ == '__main__':
    app.run(debug=True)