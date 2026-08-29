import streamlit as st
import os
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="IA & Santé | ODC Guinée",
    page_icon="🟧",
    layout="centered"
)

# 2. Main Header
st.header("🚀 ODC Guinée | Cohorte IA")
st.subheader("Système de Triage Médical - Groupe 4")
st.markdown("---")

# 3. Sidebar Profile
with st.sidebar:
    st.markdown("## ⚙️ Tableau de Bord")
    st.success("🟢 Système : ACTIF")
    st.warning("⚠️ **Avertissement :** Prototype d'orientation IA. Aucun diagnostic médical.")
    st.markdown("---")
    st.markdown("### 👨‍💻 Développeur")
    st.info("""
    **Nyoh Leonard Kanyi**  
    Ingénierie Informatique  
    [🌐 Visiter le Portfolio Web](https://nyoh-leonard.vercel.app)
    """)

# 4. System Instructions (Guardrails)
SYSTEM_INSTRUCTION = """
RÔLE SYSTÈME : Vous êtes l'Assistant d'Orientation Médicale (Groupe 4) pour ODC Guinée.
VOTRE MISSION : Évaluer la gravité des symptômes et orienter le patient.

RÈGLES STRICTES :
1. ZÉRO DIAGNOSTIC : Interdiction de poser un diagnostic médical ou de prescrire des médicaments. Refusez toute question hors domaine médical.
2. LOGIQUE DE TRIAGE :
   - NIVEAU 1 (BÉNIN) : Repos, hydratation, surveillance.
   - NIVEAU 2 (AMBIGU) : Posez 1 ou 2 questions de clarification, recommandez une consultation.
   - NIVEAU 3 (URGENCE) : ALERTE MAXIMALE. Recommandez les urgences immédiatement.
3. TON : Empathique, professionnel, concis.
"""
DEMO_API_KEY = "AIzaSyAOSO2y5GxiLxr1fxsYzz6Fjbo5g1zy7H8"

# 5. Chat Interface State & Logic
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "👋 **Bonjour ! Je suis l'assistant IA d'ODC Guinée.**\n\nJe suis ici pour vous orienter. *Rappel : Je ne suis pas un médecin.*\n\n👉 **Quels sont vos symptômes aujourd'hui ?**"
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("👉 Tapez vos symptômes ici (ex: J'ai des maux de tête depuis ce matin)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        client = genai.Client(api_key=DEMO_API_KEY)
        formatted_history = [
            types.Content(role="user" if m["role"] == "user" else "model", parts=[types.Part.from_text(text=m["content"])])
            for m in st.session_state.messages
        ]

        with st.chat_message("assistant"):
            with st.spinner("Analyse des symptômes en cours..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=formatted_history,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION, 
                        temperature=0.1
                    )
                )
                st.markdown(response.text)
                
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Erreur d'interface API : {str(e)}")
