import json
from openai import OpenAI
from flask import Blueprint, request, jsonify, render_template
from app.tree import build_concept_tree, plot_tree
from app.settings import model_choice, API_KEY, base_url, create_model_instructions

api_bp = Blueprint('api', __name__)

client = OpenAI(
    api_key=API_KEY,
    base_url=base_url
)

# In-memory stack to store graph states
graph_stack = []
max_depth = 5


@api_bp.route('/index')
def index():
    return render_template('index.html')


@api_bp.route('/generate_tree', methods=['POST'])
def generate_tree():
    data = request.json
    topic = data.get("topic", "")
    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    number = int(data.get("number", ""))
    if not number:
        number = 5

    depth = data.get("depth", 0)
    if depth > max_depth:
        return jsonify({"error": "Max depth exceeded"}), 400

    response = client.chat.completions.create(
        model=model_choice,
        messages=[
            {"role": "system", "content": create_model_instructions(number)},
            {"role": "user", "content": f"Create a concept tree for: {topic}"}
        ]
    )

    llm_response = response.choices[0].message.content

    # LLM was including Markdown syntax that needed to be manually removed.
    cleaned_response = llm_response.strip().replace("```json", "").replace("```", "").strip()

    response_dictionary = json.loads(cleaned_response)

    # Parse response and build tree
    tree = build_concept_tree(topic, response_dictionary)
    graph_stack.append({"topic": topic, "tree": tree, "depth": depth})
    fig = plot_tree(tree, response_dictionary)

    return jsonify(fig.to_dict())
