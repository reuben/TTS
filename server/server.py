#!flask/bin/python
import argparse
import os

from flask import Flask, Response, request, render_template, send_file

from .synthesizer import Synthesizer
from ..utils.generic_utils import load_config

app = Flask(__name__)

if 'TTS_SERVER_CONFIG' in os.environ:
    synthesizer = Synthesizer()
    config_path = os.environ['TTS_SERVER_CONFIG']
    config = load_config(config_path)
    synthesizer.load_model(config_path, config.model_path, config.model_name,
                           config.model_config, config.use_cuda)

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
        '-c', '--config_path', type=str, help='path to server.conf configuration file')
    args = parser.parse_args()

    config = load_config(args.config_path)

    synthesizer = Synthesizer()
    synthesizer.load_model(args.config_path, config.model_path,
                           config.model_name, config.model_config,
                           config.use_cuda)

    app.run(debug=config.debug, host='0.0.0.0', port=config.port)
