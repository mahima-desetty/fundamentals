New knowledge builds off of prior knowledge (whether the prior knowledge is accepted as true or not).

This application uses an LLM to generate a set of fundamentals, or prerequisite knowledge, to
understand a  given topic.

**Instructions**

1. Add a string to `app.secret_key=` in the `app/__init__.py` file.
1. Retrieve an api key for the Grok API and set it as an environment variable called `API_KEY`.
   1. This app uses the [Grok API](https://docs.x.ai/docs). If you'd like to use a different API, update the fields in `app/settings.py`
1. Command line prompts:
    ```shell
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python3 run.py
    ```
1. Access the UI at `http://127.0.0.1:5000/api/index`. 

![image1](img/one.png)
![image2](img/two.png)
![image3](img/three.png)

Future TODOs
* overall aesthetics and responsiveness improvements. sometimes the graph nodes are not super responsive.
* include an overview of the main topic under the concept graph.
* ability to click on a node and have it generate practice problems for you to better understand the concept.
