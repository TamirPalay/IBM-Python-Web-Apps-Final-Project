import requests
import json

def emotion_detector(text_to_analyze):
    """
    Detects emotions in the provided text using the Watson NLP Emotion Predict function.
    Args:
        text_to_analyze (str): The text to analyze.
    Returns:
        dict: A dictionary containing scores for anger, disgust, fear, joy, and sadness,
              and the dominant emotion. If the input is invalid, returns a dictionary
              with all values set to None.
    """
    # Handle blank or invalid input
    if not text_to_analyze or text_to_analyze.strip() == "":
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    # URL for the Emotion Predict service
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    # Request payload
    payload = {"raw_document": {"text": text_to_analyze}}
    # Headers for the API call
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    try:
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        response_data = response.json()  # Parse the JSON response
        
        # Extract emotion scores from the correct location
        emotions = response_data.get("emotionPredictions", [{}])[0].get("emotion", {})
    except (requests.RequestException, json.JSONDecodeError, IndexError, KeyError):
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    # Extract scores for required emotions
    anger_score = emotions.get("anger", 0)
    disgust_score = emotions.get("disgust", 0)
    fear_score = emotions.get("fear", 0)
    joy_score = emotions.get("joy", 0)
    sadness_score = emotions.get("sadness", 0)

    # Check if all scores are zero
    if not any([anger_score, disgust_score, fear_score, joy_score, sadness_score]):
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    # Find the dominant emotion
    emotion_scores = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
    }
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    # Return the formatted output
    return {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        'dominant_emotion': dominant_emotion
    }
