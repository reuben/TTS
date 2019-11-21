#!flask/bin/python
import argparse
import os

from .synthesizer import Synthesizer
from ..utils.generic_utils import load_config

from flask import Flask, Response, request, render_template, send_file

app = Flask(__name__)

if 'TTS_SERVER_CONFIG' in os.environ:
    synthesizer = Synthesizer(os.environ['TTS_SERVER_CONFIG'])

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/tts', methods=['GET'])
def tts():
    text = request.args.get('text')
    print(" > Model input: {}".format(text))
    data = synthesizer.tts(text)
    return send_file(data, mimetype='audio/wav')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config_path', required=True, type=str, help='path to server.json config file for training')
    args = parser.parse_args()

    config = load_config(args.config_path)
    synthesizer = Synthesizer(args.config_path)
    app.run(debug=config.debug, host='0.0.0.0', port=config.port)
