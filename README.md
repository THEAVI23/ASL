This final year project focuses on converting American Sign Language (ASL) gestures into meaningful English sentences using YOLOv11 for gesture detection and the Gork API for natural language generation. Unlike basic alphabet detection, this system works with predefined word gestures and intelligently forms grammatically correct sentences.

🔍 Key Features
Real-time ASL word recognition using webcam input

Fast and accurate gesture detection with YOLOv11

Integration with Gork API for converting recognized words into meaningful sentences

Seamless text output display of final sentence

Highly scalable for future vocabulary expansion

🛠️ Tech Stack
Python

YOLOv11 (Deep Learning-based gesture detection)

Gork API (Natural Language Processing & Sentence Structuring)

OpenCV (Image processing)

Flask (for UI or API deployment – if used)

🧠 How It Works
Capture hand gesture via webcam

Use YOLOv11 to detect the corresponding ASL word

Collect a sequence of words

Send recognized word list to Gork API

Gork returns a coherent English sentence

Final sentence is displayed to the user

📁 Dataset
Custom dataset of ASL gestures representing words

Manually annotated for YOLOv11 training

📌 Future Scope
Support for dynamic gestures and full sentence signing

Integration with TTS (Text-to-Speech) for speech output

Android/iOS deployment for accessibility

Add voice-to-sign support for two-way communication

