import os
import asyncio
import edge_tts
from flask import Flask, request, send_file

app = Flask(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))

def convert_text_to_speech(text, voice, output_file):
    """
    Converts the given text to speech and saves it as an MP3 file.

    Args:
        text (str): The text to be converted to speech.
        voice (str): The voice to use for speech synthesis.
        output_file (str): The name of the output MP3 file.
    """
    async def amain() -> None:
        """Main async function"""
        communicate = edge_tts.Communicate(text, voice)

        await communicate.save(output_file)

    try:
        loop = asyncio.get_event_loop_policy().get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        else:
            raise ex

    try:
        loop.run_until_complete(amain())
    finally:
        loop.close()

@app.route('/', methods=['GET', 'POST'])
def web_convert_text_to_speech():
    if request.method == 'POST':
        text = request.form['text'].strip()
        voice = request.form['voice']
        # output_file = 'output.mp3'
        output_file = text[:20].replace(' ', '_') + '.mp3'
        full_path_output_file = os.path.join(current_dir, output_file)
        convert_text_to_speech(text, voice, full_path_output_file)
        return send_file(output_file, as_attachment=True)
    return '''
        <!DOCTYPE html>
<html>
<head>
    <title>Text to Speech Converter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #94a9bf, #623549, #0c8adf);
    background-size: 600% 600%;
    animation: gradientAnimation 25s ease infinite;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    margin: 0;
    overflow-x: hidden;
}

@keyframes gradientAnimation {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

.container {
    background-color: rgba(255, 255, 255, 0.9);
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    text-align: center;
    max-width: 100%;
    width: 90%;
    box-sizing: border-box;
}

.form-group {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 10px;
}

label {
    margin-bottom: 5px;
    font-weight: bold;
}

textarea, select {
    padding: 5px;
    border-radius: 3px;
    border: 1px solid #ccc;
    resize: vertical;
    width: 100%;
}

textarea {
    height: 100px;
    font-family: monospace;
    white-space: pre-wrap;
    overflow: auto;
}

input[type="submit"] {
    padding: 8px 15px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 3px;
    cursor: pointer;
}

.signature {
    position: fixed;
    bottom: 10px;
    right: 10px;
    font-size: 12px;
    color: #666;
}

@media (max-width: 480px) {
    .form-group {
        flex-direction: column;
        align-items: stretch;
    }

    label {
        margin-bottom: 5px;
    }

    textarea, select {
        width: 100%;
    }
}
    </style>
</head>
<body>
    <div class="container">
        <h2>Text to Speech Converter</h2>
        <form method="post">
            <div class="form-group">
                <label for="text">Text:</label>
                <textarea name="text" id="text" rows="5"></textarea>
            </div>
            <div class="form-group">
                <label for="voice">Voice:</label>
                <select name="voice" id="voice">
                    <option value="en-GB-SoniaNeural" selected>en-GB-SoniaNeural</option>
                    <option value="en-US-AndrewMultilingualNeural">en-US-AndrewMultilingualNeural</option>
                    <option value="en-US-AnaNeural">en-US-AnaNeural</option>
                    <option value="en-US-AvaNeural">en-US-AvaNeural</option>
                </select>
            </div>
            <input type="submit" value="Convert to Speech">
        </form>
    </div>
    <div class="signature">by@xiaorik</div>
</body>
</html>
    '''

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)