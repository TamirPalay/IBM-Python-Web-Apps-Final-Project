# Import Flask and the emotion_detector function
from flask import Flask, request,render_template
from EmotionDetection.emotion_detection import emotion_detector
# Initialize the Flask application
app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emotion_detection():
    """
    Detect the emotion of the provided text.
    """
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')
    # Ensure text_to_analyze is not None or empty
    if not text_to_analyze:
        return "Invalid input! Please provide text for analysis."
    # Call the emotion_detector function with the text
    response = emotion_detector(text_to_analyze)
    # Extract the required fields
    anger = response.get('anger', 0)
    disgust = response.get('disgust', 0)
    fear = response.get('fear', 0)
    joy = response.get('joy', 0)
    sadness = response.get('sadness', 0)
    dominant_emotion = response.get('dominant_emotion', 'unknown')

    # Format the response string
    response_string = (
        f"For the given statement, the system response is 'anger': {anger}, "
        f"'disgust': {disgust}, 'fear': {fear}, 'joy': {joy}, and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant_emotion}."
    )

    return response_string

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

