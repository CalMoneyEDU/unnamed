from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import prompts
import base64
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("API_Key_Calv"))

# Flask app config
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
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
    try:
        # Grab form data
        art = request.form.get("art", "")
        style = request.form.get("style", "surrealism")
        file = request.files.get("file", None)

        print("✅ Form data received:", art[:100], style)

        # Validate file
        if not file or not allowed_file(file.filename):
            print("❌ Invalid or missing file.")
            return jsonify({"error": "No valid image uploaded"}), 400

        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        print("✅ File saved at:", filepath)

        # Convert image to base64
        base64_image = encode_image_to_base64(filepath)
        print("✅ Image encoded to base64")

        # Generate prompt
        user_prompt = prompts.generate_prompt(art, style)
        print("🧠 Prompt generated.")

        # Call OpenAI Vision API
        response = client.chat.completions.create(
            model="gpt-4-turbo",
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
            max_tokens=800,
            timeout=60  # seconds
        )

        # Extract critique and return
        critique = response.choices[0].message.content
        print("✅ Critique generated successfully.")
        return jsonify({"critique": critique})

    except Exception as e:
        print("❌ Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500

    finally:
        # Clean up the uploaded file
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
            print("🧹 File deleted:", filepath)

if __name__ == "__main__":
    app.run(debug=True)
