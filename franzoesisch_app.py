import streamlit as st
import os
from openai import OpenAI
import random
import re

# Streamlit Seitenkonfiguration
st.set_page_config(page_title="Französisch Sprachlern-App", layout="wide")

# OpenAI API-Schlüssel Setup
# Zugriff auf den API-Schlüssel aus den Streamlit-Secrets
OPENAI_API_KEY = st.secrets["openai"]["api_key"]

# Initialisiere den OpenAI-Client
client = OpenAI(api_key=OPENAI_API_KEY)

# Listen für Tipps, Witze und Vokabeln (Platzhalter)
tips_of_the_day = [
    "Regelmäßiges Üben ist der Schlüssel zum Erfolg beim Sprachenlernen!",
    "Höre französische Musik, um dein Hörverständnis zu verbessern.",
    "Schaue französische Filme mit Untertiteln, um dein Vokabular zu erweitern.",
    "Übe täglich 15 Minuten Französisch sprechen, auch wenn du alleine bist.",
    "Lese französische Nachrichten oder Blogs zu Themen, die dich interessieren.",
    "Nutze Sprachlern-Apps für zusätzliche Übungen zwischendurch.",
    "Finde einen Tandem-Partner zum regelmäßigen Austausch auf Französisch.",
    "Schreibe ein Tagebuch auf Französisch, um deine Schreibfähigkeiten zu verbessern."
]
# Liste der französischen Witze
french_jokes = [
    "Pourquoi les Français mangent-ils des escargots ? Parce qu'ils n'aiment pas la fast food !",
    "Que fait une fraise sur un cheval ? Tagada tagada !",
    "Que disent deux chiens qui se rencontrent ? Canie-chal !",
    "Pourquoi le foot c'est rigolo ? Parce que Thierry en rit !",
    "Quel est le comble pour un électricien ? De ne pas être au courant !",
    "Que fait une vache quand elle a les yeux fermés ? Du lait concentré !",
    "Pourquoi les poissons vivent dans l'eau salée ? Parce que dans l'eau poivrée, ils éternuent !",
    "Que se fait un Schtroumpf quand il tombe ? Un bleu !",
    "Quel fruit est assez fort pour couper des arbres ? Le citron scie !",
    "Pourquoi le lapin est bleu ? Parce qu'on l'a peint !",
    "Que dit un oignon quand il se cogne ? Aïe !",
    "Pourquoi les pompiers ont-ils des bretelles rouges ? Pour tenir leur pantalon !",
    "Quel est le café préféré des chats ? Le miaou-cchiato !",
    "Que dit un informaticien quand il s'ennuie ? Je me fichier !",
    "Pourquoi les Martiens n'aiment pas boire de l'eau ? Parce que c'est trop terre à terre !",
    "Que fait une fraise quand elle va au cinéma ? Elle se fait un fraisier !",
    "Quel est le comble pour un mathématicien ? Être dans de mauvais draps !",
    "Pourquoi les plongeurs plongent-ils toujours en arrière et jamais en avant ? Sinon ils tombent dans le bateau !",
    "Que disent deux planètes qui se rencontrent ? Alors, ça gaze ?",
    "Pourquoi les Belges viennent-ils à la messe avec du savon ? Pour l'Ave Maria !"
]



# Liste der Vokabeln des Tages
vocab_of_the_day = [
    ("le chat 🐱", "die Katze"),
    ("la maison 🏠", "das Haus"),
    ("le soleil ☀️", "die Sonne"),
    ("la voiture 🚗", "das Auto"),
    ("le livre 📚", "das Buch"),
    ("la fleur 🌸", "die Blume"),
    ("l'arbre 🌳", "der Baum"),
    ("le café ☕", "der Kaffee"),
    ("la musique 🎵", "die Musik"),
    ("le chien 🐶", "der Hund"),
    ("la plage 🏖️", "der Strand"),
    ("le vélo 🚲", "das Fahrrad"),
    ("la lune 🌙", "der Mond"),
    ("le pain 🥖", "das Brot"),
    ("la montagne ⛰️", "der Berg"),
    ("le poisson 🐠", "der Fisch"),
    ("la pomme 🍎", "der Apfel"),
    ("le téléphone 📱", "das Telefon"),
    ("la porte 🚪", "die Tür"),
    ("le vin 🍷", "der Wein")
]


def generate_exercise(level, topic, grammar):
    prompt = f"""Generiere eine Französisch-Übung für das Niveau {level} zum Thema '{topic}' mit Fokus auf die Grammatik '{grammar}'.
    Die Übung sollte aus folgenden Teilen bestehen:
    1. Eine kurze Einleitung oder Kontext (auf Deutsch)
    2. 5 Sätze auf Französisch, bei denen jeweils ein Wort oder eine Phrase fehlt. Markiere die Lücke mit _____.
    3. Die korrekten Antworten für jede Lücke, einschließlich möglicher Alternativen.

    Bitte formatiere die Ausgabe so:
    Einleitung: [Einleitungstext]

    Übung:
    [Erster Satz mit _____]
    [Zweiter Satz mit _____]
    [Dritter Satz mit _____]
    [Vierter Satz mit _____]
    [Fünfter Satz mit _____]

    Antworten:
    1. [Hauptantwort für Satz 1] (Alternative: [Alternative Antwort, falls vorhanden])
    2. [Hauptantwort für Satz 2] (Alternative: [Alternative Antwort, falls vorhanden])
    3. [Hauptantwort für Satz 3] (Alternative: [Alternative Antwort, falls vorhanden])
    4. [Hauptantwort für Satz 4] (Alternative: [Alternative Antwort, falls vorhanden])
    5. [Hauptantwort für Satz 5] (Alternative: [Alternative Antwort, falls vorhanden])
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Du bist ein hilfreicher Französischlehrer, der Übungen erstellt."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {str(e)}"


def check_answers(user_answers, correct_answers, level):
    prompt = f"""
    Überprüfe die folgenden Antworten des Schülers für eine Französisch-Übung des Niveaus {level}:

    {', '.join([f'Frage {i + 1}: Schülerantwort: "{ua}", Korrekte Antwort(en): "{ca}"' for i, (ua, ca) in enumerate(zip(user_answers, correct_answers))])}

    Bitte gib für jede Antwort an:
    1. Ob sie korrekt ist
    2. Falls nicht korrekt, erkläre den Fehler
    3. Gib einen Tipp zur Verbesserung

    Abschließend:
    4. Bewerte den allgemeinen Lernstand basierend auf diesen Antworten
    5. Gib einen allgemeinen Tipp zur Verbesserung
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "Du bist ein erfahrener Französischlehrer, der Schülerantworten bewertet."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ein Fehler ist aufgetreten bei der Überprüfung: {str(e)}"


def display_exercise(exercise_text):
    parts = exercise_text.split('\n')

    # Zeige die Einleitung
    st.write("### Übung:")
    st.write(parts[0])  # Einleitung

    user_answers = []
    questions = [q.strip() for q in parts[1:] if
                 q.strip() and not q.startswith("Antworten:") and not q.lower().startswith("übung:")]

    for i, question in enumerate(questions, start=1):
        # Entferne jegliche vorhandene Nummerierung am Anfang der Frage
        clean_question = re.sub(r'^\d+\.?\s*', '', question)
        st.write(f"{i}. {clean_question}")
        answer = st.text_input(f"Deine Antwort für Frage {i}", key=f"q{i}")
        user_answers.append(answer)

    return user_answers


# Initialisierung der Session State Variablen
if 'exercise' not in st.session_state:
    st.session_state.exercise = ''
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'joke' not in st.session_state:
    st.session_state.joke = random.choice(french_jokes)
if 'vocab' not in st.session_state:
    st.session_state.vocab = random.choice(vocab_of_the_day)

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.title("Französisch Sprachlern-App")

    level = st.selectbox("Wähle das Sprachniveau:", ["A1", "A2", "B1", "B2", "C1", "C2"])
    topic = st.text_input("Gib das Thema ein:")
    grammar = st.text_input("Welche grammatischen Phänomene sollen geübt werden?")

    if st.button("Übung generieren"):
        if topic and grammar:
            with st.spinner('Generiere Übung...'):
                exercise_text = generate_exercise(level, topic, grammar)
                parts = exercise_text.split("Antworten:")
                st.session_state.exercise = parts[0].strip()
                st.session_state.answers = [ans.strip() for ans in parts[1].strip().split('\n') if ans.strip()]
            st.success('Übung wurde generiert!')

    if st.session_state.exercise:
        user_answers = display_exercise(st.session_state.exercise)

        if st.button("Antworten überprüfen"):
            feedback = check_answers(user_answers, st.session_state.answers, level)
            st.write("### Feedback:")
            st.write(feedback)

with col2:
    st.markdown('<div class="sidebar">', unsafe_allow_html=True)
    st.write("### Tipp des Tages 💡")
    st.info(random.choice(tips_of_the_day))

    st.write("### Witz des Tages 😆")
    st.success(st.session_state.joke)

    st.write("### Vokabel des Tages")
    french, german = st.session_state.vocab
    st.info(f"{french} - {german}")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("Erstellt mit ❤️ für Französischlernende")