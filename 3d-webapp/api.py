from flask import Flask, jsonify, make_response, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/score', methods=['POST'])
def score():
    features = request.json['X']
    return make_response(jsonify({'score': features}))

@app.route('/health', methods=['GET'])
def health():
    return make_response(jsonify({'status': 'ok'}))

@app.route('/metadata', methods=['GET'])
def metadata():
    return make_response(jsonify({'name': 'Testing Flask App', 'version': '1.0'}))

@app.route('/docs', methods=['GET'])
def docs():
    return make_response(jsonify({'docs': 'kubernetes.io'}))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)