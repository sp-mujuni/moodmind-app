# MoodMind: Emotion Detector with Recommendation System
- This script creates a graphical user interface (GUI) that captures video from the default camera, analyzes the emotion of the person in the video frame using DeepFace, and provides a recommendation based on the detected emotion. The user inputs their name and age, which are displayed on the video feed along with the detected emotion and recommendation.

- It uses DeepFace for emotion detection and Gemini AI for generating recommendations. The user details and the detected emotion with the recommendation are stored in a Firestore database.

- The script integrates emotion detection with a recommendation system, making it useful for applications in mental health, personalized user experiences, and more.

# Getting Started
1. Camera Access: 
Ensure your system has a camera, and it is accessible.

2. Internet Connection: 
Ensure your system is connected to the internet as the script will interact with Firebase and the Gemini model.

3. Open the Flutter App Version folder in an IDE (for example: VS Code)

4. Using the IDE terminal, create a virtual environment to manage dependencies:
python -m venv moodmind-env
cd moodmind-env
source bin/activate. On Windows, use `.\Scripts\activate`

5. Install Necessary Libraries:
pip install firebase-admin
pip install google-cloud-firestore
pip install opencv-python
pip install deepface
pip install python-dotenv
pip install flet
pip install google-generativeai

6. Run the script using the following command:
python app.py
