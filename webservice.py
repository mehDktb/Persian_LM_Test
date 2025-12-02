from flask import Flask, request, jsonify
from models.Qwen3_VL_8B_Instruct import qwen_chat, qwen_sql_from_nl
from models.Llama_31_8B_Instruct import llama_chat
from models.gpt_oss_20B import gpt_oss_chat

app = Flask(__name__)

MODEL_ROUTER = {
    "qwen": qwen_sql_from_nl,
    "llama_3.1_8B" : llama_chat,
    "gpt_oss": gpt_oss_chat,
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

if __name__ == "__main__":
    # listen on all IPs, port 5000
    app.run(host="0.0.0.0", port=5000)
