from ultralytics import YOLO
import cv2
from collections import Counter
import requests
import time

# Load YOLO model
model = YOLO(r"E:\_clgproject\flask\best_19_classes.pt")

# Initialize webcam
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Word tracking
word_counter = Counter()
last_detection_time = time.time()
pause_threshold = 2.5  # in seconds

# Groq API Key
GROQ_API_KEY = "*"

# Global variable for live sentence UI
current_sentence = "Waiting for signs..."

# ---- Sentence & Enhancement Logic ----

def filter_and_generate_sentence(counter):
    words = [word for word, count in counter.items() if count > 1]
    return " ".join(words).capitalize() if words else None

def enhance_sentence_with_groq(sentence):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"Improve the grammar and structure of this sentence, but respond ONLY with the improved sentence. No explanations: \"{sentence}\""

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 60,
        "temperature": 0.5
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        print(f"\n❌ API Request failed: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        return sentence  # fallback to raw sentence

# ---- Main generator for Flask/Web ----

def generate_frames():
    global word_counter, last_detection_time, current_sentence

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)
        current_frame_words = []

        for box in results[0].boxes:
            class_index = int(box.cls)
            word = model.names[class_index].lower()
            current_frame_words.append(word)

        if current_frame_words:
            last_detection_time = time.time()
            word_counter.update(current_frame_words)

        if time.time() - last_detection_time > pause_threshold and len(word_counter) > 0:
            rough_sentence = filter_and_generate_sentence(word_counter)
            if rough_sentence:
                print(f"\n📝 Raw Sentence: {rough_sentence}")
                refined = enhance_sentence_with_groq(rough_sentence)
                if refined:
                    current_sentence = refined
                    print(f"✨ Enhanced Sentence: {refined}")
            word_counter.clear()
            last_detection_time = time.time()

        # Annotate and encode frame
        annotated = results[0].plot()
        ret, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# ---- Optional: Get latest sentence for frontend display ----

def get_current_sentence():
    print("🔍 Fetching current sentence:", current_sentence)
    return current_sentence
