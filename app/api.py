import json
from openai import OpenAI
from flask import Blueprint, request, jsonify, render_template, session
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

    # Store number in the session for retrieval in subsequent graph creations.
    session['number'] = number

    depth = 0

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
    graph_stack.append({"topic": topic, "tree": tree, "depth": depth, "node_data": response_dictionary})
    fig = plot_tree(tree, response_dictionary)

    return jsonify(fig.to_dict())


@api_bp.route('/explore_node/<node_id>', methods=['POST'])
def explore_node(node_id):
    """
    Explore a specific node and generate a subgraph for it.
    """
    if not node_id:
        return
    if not graph_stack:
        return jsonify({"error": "No graph to explore"}), 400

    if 'number' in session:
        number = session['number']
    else:
        number = 5

    print(node_id)

    # Get the current graph and build a subgraph
    current_state = graph_stack[-1]
    current_depth = current_state["depth"]

    if current_depth >= max_depth:
        return jsonify({"error": "Maximum concept depth exceeded. Make sure you understand "
                                 "the foundations of the original topic before going "
                                 "deeper.".format()}), 400

    response = client.chat.completions.create(
        model=model_choice,
        messages=[
            {"role": "system", "content": create_model_instructions(number)},
            {"role": "user", "content": f"Create a concept tree for: {node_id}"}
        ]
    )

    llm_response = response.choices[0].message.content

    # LLM was including Markdown syntax that needed to be manually removed.
    cleaned_response = llm_response.strip().replace("```json", "").replace("```", "").strip()

    response_dictionary = json.loads(cleaned_response)

    # Parse response and build tree
    # tree = build_subgraph(parent_graph, node_id)
    tree = build_concept_tree(node_id, response_dictionary)

    # Push the new subgraph state onto the stack
    graph_stack.append({"topic": node_id, "tree": tree,
                        "depth": current_depth+1, "node_data": response_dictionary})
    fig = plot_tree(tree, response_dictionary)

    return jsonify(fig.to_dict())


@api_bp.route('/go_back', methods=['POST'])
def go_back():
    """
    Go back to the previous graph in the stack.
    """
    if len(graph_stack) > 1:
        graph_stack.pop()
        parent_state = graph_stack[-1]
        fig = plot_tree(parent_state["tree"], parent_state["node_data"])
        return jsonify(fig.to_dict())
    return jsonify({"error": "No parent graph to return to. Start by entering "
                             "a concept in the topic box above."}), 400
