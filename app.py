import streamlit as st
import cv2
import tempfile
import numpy as np
from ultralytics import YOLO
from PIL import Image
import av
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

st.set_page_config(
    page_title="Helmet Detection App",
    page_icon="⛑️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("Configuration")

@st.cache_resource
def load_model(model_path):
    return YOLO(model_path)

try:
    model = load_model("weights/best.pt")
    st.sidebar.success("Model Loaded Successfully!")
except Exception as e:
    st.sidebar.error(f"Error loading model: {e}")

mode = st.sidebar.radio(
    "Select Mode",
    ["🖼️ Image Inference", "🎥 Video Inference", "🤳 Real-time Webcam"],
    index=0
)

conf_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.4, 0.05)
iou_threshold = st.sidebar.slider("IOU Threshold", 0.0, 1.0, 0.5, 0.05)
img_size = st.sidebar.slider("Inference Image Size", 320, 1024, 320, 32)

if 'model' in locals():
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Model Info")
    st.sidebar.write(f"Classes: {model.names}")

st.title(f"⛑️ YOLOv8 Helmet Detection - {mode}")

def predict_image(image, conf, iou, imgsz):
    results = model.predict(image, conf=conf, iou=iou, imgsz=imgsz)
    return results


if mode == "🖼️ Image Inference":
    st.header("Upload an Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Uploaded Image", use_container_width=True)
        
        if st.button("Detect"):
            results = predict_image(image, conf_threshold, iou_threshold, img_size)
            res_plotted = results[0].plot()
            res_image = Image.fromarray(res_plotted[..., ::-1])
            
            with col2:
                st.image(res_image, caption="Detected Image", use_container_width=True)

            st.markdown("### Detection Results")
            boxes = results[0].boxes
            cls_ids = boxes.cls.cpu().numpy()
            class_counts = {}
            
            for cls_id in cls_ids:
                class_name = model.names[int(cls_id)]
                class_counts[class_name] = class_counts.get(class_name, 0) + 1
            
            for name, count in class_counts.items():
                st.success(f"**{name}**: {count}")

elif mode == "🎥 Video Inference":
    st.header("Upload a Video")
    uploaded_video = st.file_uploader("Choose a video...", type=['mp4', 'avi', 'mov'])
    
    if uploaded_video is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())
        video_path = tfile.name
        
        st_frame = st.empty()
        cap = cv2.VideoCapture(video_path)
        
        if st.button("Start Processing"):
            stop_button = st.button("Stop Processing")
            while cap.isOpened():
                if stop_button:
                    break
                ret, frame = cap.read()
                if not ret:
                    break

                results = model.predict(frame, conf=conf_threshold, iou=iou_threshold, imgsz=img_size)
                res_plotted = results[0].plot()

                res_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
                st_frame.image(res_rgb, caption="Processing Video", use_container_width=True)
            
            cap.release()

elif mode == "🤳 Real-time Webcam":
    st.header("Real-time Detection")
    st.markdown("Use the Start/Stop buttons below to control the webcam.")

    camera_type = st.radio("Select Camera", ["User (Front)", "Environment (Back)"], horizontal=True)
    video_mode = {"User (Front)": "user", "Environment (Back)": "environment"}[camera_type]

    def video_frame_callback(frame):
        img = frame.to_ndarray(format="bgr24")
        
        results = model.predict(img, conf=conf_threshold, iou=iou_threshold, imgsz=img_size)
        annotated_frame = results[0].plot()
        
        return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")



    webrtc_streamer(
        key="helmet-detection",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTCConfiguration(
            {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        ),
        video_frame_callback=video_frame_callback,
        media_stream_constraints={
            "video": {"facingMode": video_mode},
            "audio": False,
        },
        async_processing=True,
    )
