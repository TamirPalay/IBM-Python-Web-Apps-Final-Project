import requests
import json

def emotion_detector(text_to_analyze):
    """
    Detects emotions in the provided text using the Watson NLP Emotion Predict function.

    Args:
        text_to_analyze (str): The text to analyze.

    Returns:
        dict: A dictionary containing scores for anger, disgust, fear, joy, and sadness,
              and the dominant emotion.
    """
    # URL for the Emotion Predict service
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    # Request payload
    payload = {"raw_document": {"text": text_to_analyze}}
    # Headers for the API call
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    # Make the POST request
    response = requests.post(url, json=payload, headers=headers)

    # Parse the JSON response
    try:
        response_data = json.loads(response.text)
        # Extract emotion scores from the correct location
        emotions = response_data.get("emotionPredictions", [{}])[0].get("emotion", {})
    except (json.JSONDecodeError, IndexError, KeyError):
        return {"error": "Invalid API response"}

    # Extract scores for required emotions
    anger_score = emotions.get("anger", 0)
    disgust_score = emotions.get("disgust", 0)
    fear_score = emotions.get("fear", 0)
    joy_score = emotions.get("joy", 0)
    sadness_score = emotions.get("sadness", 0)

    # Check if all scores are zero
    if not any([anger_score, disgust_score, fear_score, joy_score, sadness_score]):
        return {"error": "No valid emotion detected"}

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
