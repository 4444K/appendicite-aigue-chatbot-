import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=api_key)

# Define appendicitis symptoms scoring
symptoms = {
    "Douleur au quadrant inférieur droit": 1,
    "Leucocytes > 10 000/mm³": 1,
    "Migration de la douleur": 1,
    "Anorexie ou corps cétoniques dans les urines": 1,
    "Nausées ou vomissements": 1,
    "Douleur à la décompression abdominale": 1,
    "Température > 37,5°C": 1,
    "Polynucléaires neutrophiles > 75%": 1,
}

# Define ultrasound findings
ultrasound_findings = {
    "Appendice non visualisé": 0,
    "Appendice dilaté (>6mm)": 2,
    "Épanchement liquidien péri-appendiculaire": 2,
    "Épaississement pariétal appendiculaire": 2,
}

# Function to evaluate appendicitis risk
def diagnose_appendicitis():
    score = 0

    print("\nRépondez par 'oui' ou 'non' aux questions suivantes:\n")
    
    for symptom, points in symptoms.items():
        answer = input(f"Avez-vous {symptom.lower()}? ").strip().lower()
        if answer == "oui":
            score += points

    for finding, points in ultrasound_findings.items():
        answer = input(f"L'échographie montre {finding.lower()}? ").strip().lower()
        if answer == "oui":
            score += points

    print("\nAnalyse du risque...\n")

    if score >= 6:
        risk = "Élevé (Appendicite probable)"
    elif 4 <= score < 6:
        risk = "Modéré (Observation recommandée, refaire bilan)"
    else:
        risk = "Faible (Appendicite peu probable, réévaluer si aggravation)"

    return risk, score

# Function to get AI-based explanation
def get_explanation(risk, score):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
    Un patient présente un score de {score} pour l'appendicite avec un risque {risk}.
    Expliquez la prise en charge recommandée, les examens complémentaires, et les décisions possibles.
    """
    response = model.generate_content(prompt)
    return response.text

# Main chatbot loop
def chatbot():
    print("💬 Chatbot Diagnostic de l'Appendicite 💬\n")
    
    risk, score = diagnose_appendicitis()
    print(f"\n🔹 Score: {score} | Risque: {risk}\n")
    
    explanation = get_explanation(risk, score)
    print("🧠 Explication IA:\n")
    print(explanation)

# Run the chatbot
if __name__ == "__main__":
    chatbot()
