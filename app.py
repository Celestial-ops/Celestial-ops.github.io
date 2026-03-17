from flask import Flask, request, send_file, render_template_string
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# THE HTML FRONTEND (Embedded for simplicity)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>VR APK Patcher</title>
    <style>
        body { font-family: sans-serif; background: #121212; color: white; text-align: center; padding: 50px; }
        #drop-zone { border: 2px dashed #444; padding: 100px; border-radius: 20px; cursor: pointer; transition: 0.3s; }
        #drop-zone:hover { border-color: #007bff; background: #1a1a1a; }
        .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; display: none; margin-top: 20px;}
    </style>
</head>
<body>
    <h1>VR Tracer Injector</h1>
    <div id="drop-zone">Drag & Drop APK Here or Click to Upload</div>
    <input type="file" id="fileInput" style="display:none">
    <div id="status"></div>
    <a id="downloadLink" class="btn">Download Patched APK</a>

    <script>
        const dropZone = document.getElementById('drop-zone');
        const fileInput = document.getElementById('fileInput');
        const status = document.getElementById('status');
        const dlBtn = document.getElementById('downloadLink');

        dropZone.onclick = () => fileInput.click();
        
        fileInput.onchange = (e) => handleFile(e.target.files[0]);

        async function handleFile(file) {
            status.innerText = "Processing... this may take a minute.";
            const formData = new FormData();
            formData.append('apk', file);

            const response = await fetch('/upload', { method: 'POST', body: formData });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                dlBtn.href = url;
                dlBtn.download = "patched_tracer_game.apk";
                dlBtn.style.display = "inline-block";
                status.innerText = "Injection & Signing Complete!";
            } else {
                status.innerText = "Error patching file.";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['apk']
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    # --- STEP 1: Decompile/Patch (Simplified for this example) ---
    # In a real setup, you'd run your patching script here.
    
    # --- STEP 2: Sign using uber-apk-signer ---
    # Make sure uber-apk-signer.jar is in the same folder!
    signed_name = file.filename.replace(".apk", "-aligned-debugSigned.apk")
    subprocess.run(["java", "-jar", "uber-apk-signer.jar", "--apk", path])

    # Send the signed file back to the browser
    return send_file(os.path.join(UPLOAD_FOLDER, signed_name), as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000)
