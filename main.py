import asyncio
import edge_tts
from flask import Flask, request, send_file

app = Flask(__name__)

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
        convert_text_to_speech(text, voice, output_file)
        return send_file(output_file, as_attachment=True)
    return '''
        <!DOCTYPE html>
<html>
<head>
    <title>Text to Speech Converter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="favicon.svg" type="image/svg+xml">
    <svg t="1711679917707" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4245" width="200" height="200"><path d="M512.000213 1023.998293a508.627426 508.627426 0 0 1-362.025309-149.930104A508.627426 508.627426 0 0 1 0.002133 512.000213a508.627426 508.627426 0 0 1 149.930105-362.025309A508.627426 508.627426 0 0 1 512.000213 0.002133a508.712759 508.712759 0 0 1 362.067976 149.930105A508.670092 508.670092 0 0 1 1023.998293 512.000213a508.670092 508.670092 0 0 1-149.972771 362.025309A508.712759 508.712759 0 0 1 512.000213 1023.998293z m-153.258092-416.041106l171.818023 137.855483a23.466579 23.466579 0 0 0 14.335946 4.863982 22.10125 22.10125 0 0 0 22.698582-21.887918l3.711986-433.918373a22.058584 22.058584 0 0 0-22.058584-21.333253 21.333253 21.333253 0 0 0-13.141284 4.522649L345.68617 410.069929h-59.733109a22.783915 22.783915 0 0 0-22.22925 22.655915v154.708753a22.741248 22.741248 0 0 0 22.22925 22.613249h62.975764a23.637245 23.637245 0 0 0 9.64263-2.005326z m331.134759-247.039074a17.621267 17.621267 0 0 0-12.799952 5.674646 18.431931 18.431931 0 0 0-5.546646 13.18395 18.346598 18.346598 0 0 0 5.546646 13.226617 163.455387 163.455387 0 0 1 46.335826 115.199568 164.479383 164.479383 0 0 1-57.386452 124.543533 18.517264 18.517264 0 0 0-1.877326 26.367901 20.778589 20.778589 0 0 0 14.207947 5.631979h0.554664a17.493268 17.493268 0 0 0 12.799952-3.754652 206.420559 206.420559 0 0 0 68.52241-152.788761 200.532581 200.532581 0 0 0-57.386451-141.482136 17.578601 17.578601 0 0 0-13.013285-5.802645z m-53.802465 68.991742a17.578601 17.578601 0 0 0-9.173299 2.687989 15.786607 15.786607 0 0 0-9.173299 9.727964 17.877266 17.877266 0 0 0 1.70666 14.762611 92.287654 92.287654 0 0 1 12.799952 49.066483 108.415593 108.415593 0 0 1-20.39459 62.250433 20.565256 20.565256 0 0 0 3.711986 26.410568 26.282568 26.282568 0 0 0 11.135958 3.754652c5.589312 0 11.093292-3.754653 11.093292-7.551971a127.316856 127.316856 0 0 0 29.653222-84.863682 139.690143 139.690143 0 0 0-16.682604-66.005086 15.957273 15.957273 0 0 0-14.677278-10.197295z" fill="#FD5218" p-id="4246"></path></svg>
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
    app.run(debug=False)