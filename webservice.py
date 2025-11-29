from flask import Flask, request, jsonify
from models.Qwen3_VL_8B_Instruct import qwen_chat  # or same file

app = Flask(__name__)

MODEL_ROUTER = {
    "qwen": qwen_chat,
    # later: "llama": llama_chat, etc.
}

@app.route("/run", methods=["POST"])
def run_model():
    data = request.get_json() or {}
    model_name = data.get("model")
    text = data.get("text")

    if not model_name or not text:
        return jsonify({"error": "JSON must include 'model' and 'text'"}), 400

    if model_name not in MODEL_ROUTER:
        return jsonify({"error": f"Unknown model '{model_name}'"}), 400

    try:
        output = MODEL_ROUTER[model_name](text)
        return jsonify({"model": model_name, "input": text, "output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
