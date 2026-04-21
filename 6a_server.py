"""
Flask web server for Emotion Detector application
Web deployment using Flask framework
"""
from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def render_index_page():
    """Render the main page of the application"""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET"])
def emotion_detection():
    """
    Flask route for emotion detection using GET method
    
    This route accepts text input as a query parameter and returns
    emotion analysis with all five emotion scores and dominant emotion.
    
    Query Parameters:
        textToAnalyze (str): The text to analyze for emotions
        
    Returns:
        JSON response with emotion scores and dominant emotion:
        {
            "anger": float,
            "disgust": float,
            "fear": float,
            "joy": float,
            "sadness": float,
            "dominant_emotion": string
        }
    """
    # Get the text to analyze from query parameters
    text_to_analyze = request.args.get("textToAnalyze")
    
    # Check if text parameter is provided
    if not text_to_analyze:
        return jsonify({
            "error": "textToAnalyze parameter is required"
        }), 400
    
    # Call the emotion_detector function with the text input
    result = emotion_detector(text_to_analyze)
    
    # Check for error status codes
    if result.get("status_code") == 400:
        return jsonify({
            "error": "Invalid input provided",
            "anger": result.get("anger"),
            "disgust": result.get("disgust"),
            "fear": result.get("fear"),
            "joy": result.get("joy"),
            "sadness": result.get("sadness"),
            "dominant_emotion": result.get("dominant_emotion")
        }), 400
    
    if result.get("status_code") and result.get("status_code") != 200:
        return jsonify({
            "error": "Error processing emotions",
            "anger": result.get("anger"),
            "disgust": result.get("disgust"),
            "fear": result.get("fear"),
            "joy": result.get("joy"),
            "sadness": result.get("sadness"),
            "dominant_emotion": result.get("dominant_emotion")
        }), result.get("status_code", 500)
    
    # Format and return the response with all five emotion scores
    return jsonify({
        "anger": result.get("anger"),
        "disgust": result.get("disgust"),
        "fear": result.get("fear"),
        "joy": result.get("joy"),
        "sadness": result.get("sadness"),
        "dominant_emotion": result.get("dominant_emotion")
    }), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
