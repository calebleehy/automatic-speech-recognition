from flask import Flask, request, jsonify
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from pydub import AudioSegment
import torch
import tempfile
import numpy as np
import soundfile as sf
import io

# initialise app
app = Flask(__name__)

# load model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
model.eval()

# ping API
@app.route('/ping', methods=['GET'])
def ping():
    return "pong", 200

# asr API
@app.route('/asr', methods=['POST'])
def asr():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if not file.filename.endswith('.mp3'):
        return jsonify({"error": "Only mp3 files are supported"}), 400

    try:
        # read and convert mp3 to binary
        contents = file.read()
        mp3_audio = AudioSegment.from_file(io.BytesIO(contents), format="mp3")
        wav_audio = mp3_audio.set_frame_rate(16000).set_channels(1)

        with io.BytesIO() as wav_io:
            wav_audio.export(wav_io, format="wav")
            wav_io.seek(0)
            audio_data, sr = sf.read(wav_io)

        input_values = processor(audio_data, return_tensors="pt", sampling_rate=16000).input_values
        with torch.no_grad():
            logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)[0]

        duration = round(len(audio_data) / sr, 2)

        return jsonify({
            "transcription": transcription,
            "duration": f"{duration:.2f}"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # command for transcribing
    # curl.exe -F "file=@C:/Users/caleb/cv-valid-dev/sample-000000.mp3" http://localhost:8001/asr

# run
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)