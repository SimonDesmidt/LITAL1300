import streamlit as st
import pandas as pd
import random
import os

# ===== CONFIG =====
CARTELLA_VERBI = "verbi"
FILE_CSV = os.path.join(CARTELLA_VERBI, "verbi.csv")

PERSONE = ["io", "tu", "lui/lei", "noi", "voi", "loro"]

TEMPI = {
    # tenses WITHOUT persons
    "Gerundio": {"cols": 10, "persons": None},
    "Participio passato": {"cols": 9, "persons": None},

    # tenses WITH persons (6 persons)
    "Presente": {"cols": (2, 7), "persons": PERSONE},
    "Imperfetto": {"cols": (11, 16), "persons": PERSONE},
    "Futuro": {"cols": (23, 28), "persons": PERSONE},

    # Imperativo: only persons = [tu, lui/lei, noi, voi, loro]
    "Imperativo": {
        "cols": (47, 51),
        "persons": ["tu", "lui/lei", "noi", "voi", "loro"]
    },
}

if not os.path.exists(FILE_CSV):
    raise Exception("File verbi.csv non trovato!")

# ===== APP LOGIC =====

# Load verbs
df = pd.read_csv(FILE_CSV)

# ===== SESSION STATE =====
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.totale = 0
    st.session_state.verbo_corrente = None
    st.session_state.persona_corrente = None
    st.session_state.tempo_corrente = None
    st.session_state.risposta_corretta = None
    st.session_state.significato = None

# ===== FUNCTIONS =====

def nuovo_verbo():
    """Pick a new random verb and tense"""
    # Active tenses only
    tempi_validi = [tempo for tempo, var in st.session_state.tempi_attivi.items() if var]
    if not tempi_validi:
        st.warning("❌ Nessun tempo selezionato!")
        return

    st.session_state.indice_verbo = random.randint(0, len(df)-1)
    tempo = random.choice(tempi_validi)
    st.session_state.tempo_corrente = tempo
    tempo_info = TEMPI[tempo]
    col_info = tempo_info["cols"]
    persons = tempo_info["persons"]

    if persons is None:  # Tense without persons
        st.session_state.persona_corrente = None
        colonna = col_info
    else:  # Tense with persons
        persona = random.choice(persons)
        st.session_state.persona_corrente = persona
        idx_persona = persons.index(persona)
        start_col, _ = col_info
        colonna = start_col + idx_persona

    st.session_state.colonna = colonna
    st.session_state.verbo_corrente = df.iloc[st.session_state.indice_verbo, 0]
    st.session_state.significato = df.iloc[st.session_state.indice_verbo, 1]
    st.session_state.risposta_corretta = str(df.iloc[st.session_state.indice_verbo, colonna]).strip()

def controlla_risposta(risposta):
    """Check answer and update score"""
    corretto = st.session_state.risposta_corretta
    st.session_state.totale += 1
    if risposta.lower().strip() == corretto.lower():
        st.session_state.score += 1
        st.success("✅ Risposta CORRETTA!")
    else:
        st.error(f"❌ Risposta SBAGLIATA. Corretto: {corretto}")

def riprova():
    """Retry the same verb"""
    st.session_state.entry_risposta = ""
    # Keeps the same verbo, tempo, persona
    # Do nothing, just clear the input

# ===== LAYOUT =====
# st.title("Coniugazione degli verbi italiani")

# --- Right panel: tense checkboxes ---
st.sidebar.header("Tempi disponibili")
st.session_state.tempi_attivi = {}
for tempo in TEMPI.keys():
    st.session_state.tempi_attivi[tempo] = st.sidebar.checkbox(tempo, value=True)

# --- Main content ---
if st.session_state.verbo_corrente is None:
    nuovo_verbo()

# Keep the title as is
st.title("🏫 Coniugazione degli verbi italiani")

# Increase size of all other text
st.markdown(f"<span style='font-size:20px'>**Verbo:** {st.session_state.verbo_corrente}</span>", unsafe_allow_html=True)
st.markdown(f"<span style='font-size:20px'>**Tempo:** {st.session_state.tempo_corrente}</span>", unsafe_allow_html=True)
if st.session_state.persona_corrente:
    st.markdown(f"<span style='font-size:20px'>**Persona:** {st.session_state.persona_corrente}</span>", unsafe_allow_html=True)
st.markdown(f"<span style='font-size:20px'>**Significato:** {st.session_state.significato}</span>", unsafe_allow_html=True)

# Score display bigger


# Entry field
st.session_state.entry_risposta = st.text_input("Inserisci la coniugazione:", value="", key="input_field")

col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("❌ Riprova (Space)"):
        riprova()
with col2:
    if st.button("✅ OK (Enter)"):
        controlla_risposta(st.session_state.entry_risposta)
        nuovo_verbo()
with col3:
    # st.write(f"Punteggio: {st.session_state.score}/{st.session_state.totale}")
    col3.write(f"<span style='font-size:18px'>Punteggio: {st.session_state.score}/{st.session_state.totale}</span>", unsafe_allow_html=True)

# --- Keyboard shortcuts ---
st.write("💡 Premi Enter per confermare, Space per riprovare")