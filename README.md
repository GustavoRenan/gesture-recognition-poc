# Gesture Recognition API

## Overview

This project is a **computer vision gesture recognition system** implemented with **MediaPipe**, **OpenCV**, and **FastAPI**. It detects hand landmarks from images and classifies simple gestures using a **rule-based approach with temporal smoothing** to reduce noise.

The project exposes the gesture recognition logic as a **REST API**, making it suitable for backend integration with web, mobile, or desktop applications.

---

## Features

* Hand landmark detection using MediaPipe
* Rule-based gesture classification
* Temporal smoothing to reduce flickering classifications
* REST API with automatic documentation (Swagger)
* JSON-based responses

### Supported Gestures

* ✋ Open Hand
* ✊ Fist
* 👍 Thumbs Up
* ❓ Unknown / No Hand Detected

---

## Technologies Used

* **Python 3.12**
* **MediaPipe** – hand landmark detection
* **OpenCV** – image processing
* **FastAPI** – backend API framework
* **Uvicorn** – ASGI server
* **NumPy** – numerical operations

---

## Project Structure

```
gesture-recognition-poc/
│
├── src/
│   ├── main.py        # Real-time gesture recognition (webcam)
│   └── api.py         # REST API for gesture recognition
│
├── requirements.txt   # Project dependencies
├── .gitignore         # Ignored files and folders
└── README.md
```

---

## How It Works

1. An image is uploaded to the API.
2. MediaPipe detects hand landmarks.
3. Finger states are determined using geometric rules.
4. A gesture is classified based on finger configuration.
5. Temporal smoothing selects the most frequent gesture over recent frames.
6. The API returns the detected gesture as JSON.

---

## Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/gesture-recognition-poc.git
cd gesture-recognition-poc
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the API

```bash
uvicorn src.api:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```

---

## Example Request

Upload an image containing a hand to the `/gesture` endpoint.

### Example Response

```json
{
  "gesture": "Mao Aberta"
}
```

If no hand is detected:

```json
{
  "gesture": "Nenhum"
}
```

---

## Notes

* The API processes **static images**, not real-time video streams.
* Image quality, lighting, and hand visibility affect accuracy.
* The rule-based approach was chosen for transparency and explainability.

---

## Future Improvements

* Support for more gestures
* Machine learning–based gesture classification
* Frontend client for real-time camera input
* Multi-hand support

---

## Author

Developed by **Gustavo Renan Campos Serrão**

This project was inspired by academic research in gesture recognition and designed as a practical, production-oriented proof of concept.
