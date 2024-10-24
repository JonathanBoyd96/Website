import spacy

# Load a pre-trained model
nlp = spacy.load("model/data_model")
doc = nlp("Erik Adams, 555 Birch Road Suite 404, Columbus, OH 43215")
for ent in doc.ents:
    print(ent.text, ent.label_)