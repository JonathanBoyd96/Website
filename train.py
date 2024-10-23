import json
import random
import spacy
from spacy.training import Example
from spacy.training import offsets_to_biluo_tags
from spacy.util import minibatch

# Load a base model
nlp = spacy.load("en_core_web_sm")  # Load a pre-trained model

# If the model already has an NER component, remove it to add a new one
if "ner" in nlp.pipe_names:
    ner = nlp.get_pipe("ner")
else:
    ner = nlp.add_pipe("ner", last=True)

# Load your training data
with open("data/address_data.json", "r") as f:
    training_data = json.load(f)

# Debugging: Check the structure of your training data
print(f"Training data loaded: {training_data}")

# Add labels to the NER
for item in training_data:  # Iterate over each item
    annotations = item  # Directly use item as annotations
    for ent in annotations.get("entities", []):  # Use .get with a default to avoid errors
        ner.add_label(ent[2])  # Add entity label

# Debugging: Check alignment
for item in training_data:
    text = item["text"]  # Access text
    annotations = item  # Use item as annotations
    biluo_tags = offsets_to_biluo_tags(nlp.make_doc(text), annotations["entities"])
    print(f"Text: {text}")
    print(f"Entities: {annotations['entities']}")
    print(f"BILUO Tags: {biluo_tags}")
    print("----------")

# Prepare the data for training
train_data = []
for item in training_data:
    text = item["text"]
    annotations = {"entities": item["entities"]}  # Create annotations dict
    train_data.append((text, annotations))

# Training loop
n_iter = 20
for itn in range(n_iter):
    random.shuffle(train_data)
    losses = {}
    for batch in minibatch(train_data, size=8):
        for text, annotations in batch:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update([example], drop=0.5, losses=losses)
    print(f"Iteration {itn}: Losses {losses}")

# Save the trained model
nlp.to_disk("address_model")