from flask import Flask, request, jsonify
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import os
import io

# initialise app
app = Flask(__name__)

# load model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

# ping API
@app.route('/ping', methods=['GET'])
def ping():
    return "pong", 200

# run
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)