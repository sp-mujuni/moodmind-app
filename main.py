import firebase_admin
from firebase_admin import credentials, firestore
import google.cloud.exceptions
import time
import cv2
from deepface import DeepFace
from dotenv import load_dotenv
import google.generativeai as genai
import os
import flet as ft

# Load environment variables
load_dotenv()

# Initialize Firebase
cred = credentials.Certificate('moodmind-key.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

# Initializing Gemini model
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to store user data in Firestore
def store_user_data(name, age, emotion, recommendation):
    doc_ref = db.collection('users').document(name)
    doc_ref.set({
        'name': name,
        'age': age,
        'emotion': emotion,
        'recommendation': recommendation,
    })

# Function to retrieve user data from Firestore
def get_user_data(name):
    doc_ref = db.collection('users').document(name)
    try:
        doc = doc_ref.get()
        return doc.to_dict()
    except google.cloud.exceptions.NotFound:
        print(f'No such document for user: {name}')
        return None

# Function to analyze emotions from video frame
def analyze_frame_emotions(frame):
    analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
    return analysis[0]['dominant_emotion']

# Function to get recommendation based on emotion from Gemini model
def get_recommendation(emotion):
    if emotion == 'happy':
        recommendation = model.generate_content("in five words only, generate a recommendation for a happy emotion")
    elif emotion == 'sad':
        recommendation = model.generate_content("in five words only, generate a recommendation for a sad emotion")
    elif emotion == 'angry':
        recommendation = model.generate_content("in five words only, generate a recommendation for an angry emotion")
    elif emotion == 'neutral':
        recommendation = model.generate_content("in five words only, generate a recommendation for a neutral emotion")
    elif emotion == 'surprise':
        recommendation = model.generate_content("in five words only, generate a recommendation for a surprise emotion")
    elif emotion == 'fear':
        recommendation = model.generate_content("in five words only, generate recommendation for a fear emotion")
    elif emotion == 'disgust':
        recommendation = model.generate_content("in five words only, generate recommendation for a disgust emotion")
    else:
        recommendation = model.generate_content("in five words only, generate recommendation for no emotion")
    return recommendation

# Function to start video capture and analyze emotions
def start_video_capture(name, age):
    # Open video capture
    video_capture = cv2.VideoCapture(0)  # 0 for the default camera

    # Resize window
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Video', 1024, 768)

    last_capture_time = time.time()

    # Process video frames
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        current_time = time.time()
        if current_time - last_capture_time >= 10:
            # Analyze the frame for emotions
            emotion = analyze_frame_emotions(frame)
            print("Predicted Emotion from Video Frame:\n", emotion)

            # Get recommendation based on emotion
            recommendation = get_recommendation(emotion)

            # Store user data in Firestore
            store_user_data(name, age, emotion, recommendation.text)

            # Display the frame with emotion, name, age and recommendation labels
            cv2.putText(frame, f'Emotion: {emotion}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, f'Name: {name}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, f'Age: {age}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, f'Recommendation: {recommendation.text}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

            # Update the last capture time
            last_capture_time = current_time

            # Display the frame
            cv2.imshow('Video', frame)

            # Add a delay of 5 seconds
            cv2.waitKey(5000)  # 5000 milliseconds = 5 seconds

        cv2.imshow('Video', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    video_capture.release()
    cv2.destroyAllWindows()

# Function to handle the start button click event
def start_button_clicked(e, name_input, age_input):
    name = name_input.value
    age = age_input.value
    start_video_capture(name, age)

# Create the Flet app
def main(page: ft.Page):
    page.title = "Emotion Detector with Recommendation"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Create input fields and button
    name_input = ft.TextField(label="Enter your name:", width=200)
    age_input = ft.TextField(label="Enter your age:", width=200)
    start_button = ft.ElevatedButton(text="Start Video Capture", on_click=lambda e: start_button_clicked(e, name_input, age_input))

    # Create a container to hold the input fields and button
    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("MoodMind", style="headlineMedium", text_align=ft.TextAlign.CENTER),
                name_input,
                age_input,
                start_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        width=300,
        padding=20,
        border_radius=20,
        bgcolor=ft.colors.BLUE_GREY_50,
        shadow=ft.BoxShadow(blur_radius=15, spread_radius=5, color=ft.colors.BLACK45),
    )

    page.add(container)

ft.app(target=main)
