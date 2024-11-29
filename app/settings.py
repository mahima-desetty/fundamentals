import os

# Enter the model you'd like to use. OpenAI's library
# supports openai, gemini, and grok models to name a few.
model_choice = "grok-beta"

# Set your api key as an env variable, API_KEY.
API_KEY = os.getenv("API_KEY")

# Replace 'your-base-url' with the base_url for the
# chosen model.
base_url = "https://api.x.ai/v1"


def create_model_instructions(number_of_concepts):
    """Provide high-level guidelines to the model, telling it how to behave throughout the conversation."""
    model_instructions = "A user will present you with a topic and your," \
                         "responsibility is to provide them with the prerequisite" \
                         "knowledge on that topic that will help them learn" \
                         "the original topic better. It's important to have the" \
                         "fundamentals of a concept understood before moving on to" \
                         "more complex topics. This will help the user check any" \
                         "blind spots in their knowledge so they can thoroughly" \
                         "learn a new topic. For example, if they ask you about" \
                         "'gravitational lensing', provide them with a list of" \
                         "important prior topics that would make understanding" \
                         "gravitational lensing easier. Some examples are Einstein's" \
                         "theory of relativity, Newtonian physics, how light can bend, etc." \
                         "When including a prerequisite, state why it is a prerequisite for" \
                         "understanding the desired topic. Return a max number of {} concepts." \
                         "Present the prerequisites as a dictionary so that my application can" \
                         "parse it. The key in the dictionary should be the name of the" \
                         "prerequisite and the value should be why it is a prerequisite." \
                         "An example of the formatting is: 'Einstein's theory of relativity':" \
                         "'This is a prerequisite because...'. Just return the dictionary, no" \
                         "intro text or any characters before the dictionary.".format(number_of_concepts)
    return model_instructions
