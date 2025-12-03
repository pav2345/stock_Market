from transformers import pipeline

# 🔥 Force Transformers to use PyTorch and ignore TensorFlow/Keras
sentiment_model = pipeline(
    "sentiment-analysis",
    framework="pt"  # Force PyTorch
)

def analyze_sentiment(news_text: str):
    try:
        result = sentiment_model(news_text)[0]

        label = result["label"]
        score = result["score"]

        # Convert model output to BUY / SELL / HOLD
        if label == "POSITIVE":
            signal = "BUY"
        elif label == "NEGATIVE":
            signal = "SELL"
        else:
            signal = "HOLD"

        return {
            "sentiment": label,
            "confidence": round(score * 100, 2),
            "signal": signal
        }

    except Exception as e:
        return {"error": str(e)}
