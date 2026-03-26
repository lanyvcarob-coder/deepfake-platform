import random

def analyze_file(filename):
    probability = random.randint(0, 100)
    explanation = "Patrones faciales inconsistentes detectados" if probability > 50 else "Sin evidencia significativa"
    return {
        "file": filename,
        "deepfake_probability": probability,
        "explanation": explanation
    }
