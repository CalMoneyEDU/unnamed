from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import prompts
import base64
from werkzeug.utils import secure_filename

load_dotenv()
client = OpenAI(api_key=os.getenv("API_Key_Calv"))

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB limit
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_image_to_base64(filepath):
    with open(filepath, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

@app.route("/api/critique", methods=["POST"])
def critique():
    art = request.form.get("art", "")
    style = request.form.get("style", "surrealism")
    file = request.files.get("file", None)

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "No valid image uploaded"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        base64_image = encode_image_to_base64(filepath)
        user_prompt = prompts.generate_prompt(art, style)

        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": prompts.system_message},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=800
        )

        critique = response.choices[0].message.content
        return jsonify({"critique": critique})

    finally:
        # Always delete the file after processing
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == "__main__":
    app.run(debug=True)
