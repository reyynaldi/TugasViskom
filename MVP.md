# Project Specification: YOLOv8 Helmet Detection Web App

## 1. Objective

Create a **Streamlit** web application that uses a custom **YOLOv8** model (`best.pt`) to detect motorcycle riders with and without helmets. The app must be optimized for both desktop and mobile browsers (hosting on Streamlit Cloud) and support three distinct modes of inference.

## 2. Tech Stack

* **Framework:** Streamlit
* **Model:** Ultralytics YOLOv8
* **Real-time Video:** `streamlit-webrtc` (essential for mobile browser camera access)
* **Image Processing:** OpenCV, PIL, and NumPy
* **Hosting Target:** Streamlit Community Cloud (CPU environment)

## 3. Core Features & Functional Requirements

### A. Global Settings (Sidebar)

* **Model Loader:** Load `best.pt` using the `ultralytics` library.
* **Mode Selector:** Radio buttons for: `[🖼️ Image Inference, 🎥 Video File, 🤳 Real-time Webcam]`.
* **Inference Parameters:** * Confidence Threshold slider (0.0 to 1.0).
* IOU Threshold slider (0.0 to 1.0).


* **Model Info:** Display a small summary of the model (classes: `with_helm`, `without_helm`).

### B. Image Inference Mode

* **Input:** File uploader for `.jpg`, `.jpeg`, and `.png`.
* **Action:** Run model inference on the uploaded image.
* **Output:** Display the original image with YOLOv8 bounding boxes and labels overlaid. Show a count of detected objects per class.

### C. Video Inference Mode

* **Input:** File uploader for `.mp4`, `.avi`, or `.mov`.
* **Action:** Process video frame-by-frame. Use a temporary file to store the upload before processing with `cv2.VideoCapture`.
* **Output:** A "live-updating" image container in Streamlit that displays the processed frames with detections.

### D. Real-time Webcam Mode (Mobile Optimized)

* **Implementation:** Use `streamlit-webrtc`.
* **Hardware Control:** * Implement a toggle to switch between `User` (front) and `Environment` (back/rear) cameras.
* Set `media_stream_constraints` to support mobile browser permissions.


* **Processing:** Define a `VideoTransformer` or `callback` function that runs YOLOv8 inference on every incoming frame in real-time.
* **Performance:** Ensure the `imgsz` for real-time inference is adjustable (default to 320 for speed on CPU cloud hosting).

## 4. Performance & Mobile Requirements

* **Latency:** Use `async_processing=True` in the WebRTC streamer to prevent UI lag.
* **Security:** Ensure the app handles HTTPS requirements (necessary for browser camera permissions).
* **Memory:** Optimize for Streamlit Cloud’s 1GB RAM limit—do not keep multiple copies of heavy video files in memory.

## 5. Directory Structure

* `app.py` (Main application logic)
* `weights/best.pt` (Place for the custom model)
* `requirements.txt` (Must include: `streamlit`, `ultralytics`, `streamlit-webrtc`, `opencv-python-headless`, `av`)

---

### Instructions for the Agent:

> *"Please build this app step-by-step. Start with the UI layout and the Image Inference mode. Once that works, move to the Video processing loop, and finally implement the `streamlit-webrtc` logic for the mobile-friendly webcam feed. Make the UI look clean and modern."*

---

### Next Step

Would you like me to generate the **`requirements.txt`** content so you have everything ready for the deployment?