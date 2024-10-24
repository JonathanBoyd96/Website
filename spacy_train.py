import json
import spacy
from spacy.tokens import DocBin
from spacy.tokens import Doc

# Load the training data from the JSON file
with open('data/training_data.json', 'r') as f:
    training_data = json.load(f)

# Initialize a blank spaCy model
nlp = spacy.blank("en")

# Create a DocBin object
doc_bin = DocBin()

# Create Doc objects and add to DocBin
for example in training_data:
    text = example["text"]
    entities = example["entities"]
    
    # Create a Doc object using the nlp tokenizer instead of text.split()
    doc = nlp.make_doc(text)
    
    # Create a list to hold entity spans
    entity_spans = []
    
    for start, end, label in entities:
        # Ensure that the character span is valid and create entity spans
        span = doc.char_span(start, end, label=label)
        if span is not None:
            entity_spans.append(span)
        else:
            print(f"Skipping misaligned entity in text: '{text[start:end]}'")

    # Set the entities for the doc
    doc.ents = entity_spans

    # Add the doc to the DocBin
    doc_bin.add(doc)

# Save the DocBin to a .spacy file
doc_bin.to_disk("data/training_data.spacy")