import streamlit as st
import pandas as pd
import random
import os

# ===== CONFIG =====
CARTELLA_VERBI = "verbi"
FILE_CSV = os.path.join(CARTELLA_VERBI, "verbi.csv")

PERSONE = ["io", "tu", "lui/lei", "noi", "voi", "loro"]

TEMPI = {
    "Gerundio": {"cols": 10, "persons": None},
    "Participio passato": {"cols": 9, "persons": None},

    "Presente": {"cols": (2, 7), "persons": PERSONE},
    "Imperfetto": {"cols": (11, 16), "persons": PERSONE},
    "Futuro": {"cols": (23, 28), "persons": PERSONE},

    "Imperativo": {
        "cols": (47, 50),
        "persons": ["tu", "Lei", "noi", "voi"]
    },
}

if not os.path.exists(FILE_CSV):
    st.error("File verbi.csv non trovato!")
    st.stop()

df = pd.read_csv(FILE_CSV)

# ===== INITIAL STATE =====
if "punteggio" not in st.session_state:
    st.session_state.punteggio = 0
    st.session_state.totale = 0
    st.session_state.verbo_index = None
    st.session_state.risposta_corretta = ""
    st.session_state.tempo = ""
    st.session_state.persona = ""
    st.session_state.colonna = None
    st.session_state.significato = ""
    st.session_state.mostra_pulsanti = False


# ===== FUNCTIONS =====
def nuovo_verbo():
    st.session_state.mostra_pulsanti = False

    tempi_attivi = [
        t for t in TEMPI.keys()
        if st.session_state[f"chk_{t}"]
    ]

    if not tempi_attivi:
        st.warning("Nessun tempo selezionato!")
        return

    st.session_state.tempo = random.choice(tempi_attivi)
    info = TEMPI[st.session_state.tempo]
    persons = info["persons"]

    st.session_state.verbo_index = random.randint(0, len(df) - 1)
    verbo = df.iloc[st.session_state.verbo_index, 0]
    st.session_state.significato = df.iloc[st.session_state.verbo_index, 1]

    if persons is None:
        st.session_state.persona = None
        st.session_state.colonna = info["cols"]
    else:
        st.session_state.persona = random.choice(persons)
        idx = persons.index(st.session_state.persona)
        start, end = info["cols"]
        st.session_state.colonna = start + idx

    st.session_state.risposta_corretta = str(
        df.iloc[st.session_state.verbo_index, st.session_state.colonna]
    ).strip()


def controlla(risposta):
    risposta = risposta.strip()
    corretto = st.session_state.risposta_corretta

    st.session_state.totale += 1

    if risposta.lower() == corretto.lower():
        st.session_state.punteggio += 1
        st.success("Risposta corretta!")
    else:
        st.error(f"Risposta SBAGLIATA. Corretto: {corretto}")

    st.session_state.mostra_pulsanti = True


# ===== SIDEBAR (TENSES) =====
st.sidebar.header("Tempi verbali")
for tempo in TEMPI.keys():
    if f"chk_{tempo}" not in st.session_state:
        st.session_state[f"chk_{tempo}"] = True
    st.session_state[f"chk_{tempo}"] = st.sidebar.checkbox(
        tempo, value=st.session_state[f"chk_{tempo}"]
    )

# ===== MAIN AREA =====

st.title("Allenatore di verbi italiani (Streamlit Edition)")

if st.button("Nuovo verbo"):
    nuovo_verbo()

if st.session_state.verbo_index is None:
    st.stop()

verbo = df.iloc[st.session_state.verbo_index, 0]

st.subheader("Esercizio corrente")
st.write(
    f"**Verbo:** {verbo}  \n"
    f"**Tempo:** {st.session_state.tempo}  \n"
    f"**Persona:** {st.session_state.persona}  \n"
    f"**Significato:** {st.session_state.significato}"
)

if "go_next" not in st.session_state:
    st.session_state.go_next = False
if st.session_state.go_next:
    st.session_state.go_next = False
    nuovo_verbo()

# USER INPUT
risposta = st.text_input("La tua risposta:")

if st.button("Controlla"):
    controlla(risposta)

if st.session_state.mostra_pulsanti:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Riprova"):
            st.session_state.mostra_pulsanti = False
    with col2:
        if st.button("➡️ Avanti"):
            st.session_state.go_next = True
            st.rerun()


# SCORE
percentuale = (
    (st.session_state.punteggio / st.session_state.totale) * 100
    if st.session_state.totale > 0
    else 0
)

st.write(
    f"**Punteggio:** {st.session_state.punteggio} / {st.session_state.totale} "
    f"({percentuale:.1f}%)"
)