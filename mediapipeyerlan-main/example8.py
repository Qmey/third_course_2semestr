import mediapipe as mp

mp_text = mp.solutions.text
text_classifier = mp_text.TextClassifier()

text = "I love using AI for automation!"

results = text_classifier.process(text)

print("Text Classification Results:", results)
