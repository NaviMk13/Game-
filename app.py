import streamlit as st

# --- INITIALISIERUNG ---
if 'pos' not in st.session_state:
    st.session_state.pos = [1, 1]  # Startposition (x, y)
    st.session_state.inventory = []
    st.session_state.story_log = ["Willkommen in der Glitch-Welt. Finde den KI-Wächter."]

# Weltkarte (0 = Weg, 1 = Wand, 'G' = Geist/KI)
WORLD_MAP = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 'G', 1],
    [1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1],
]

def move(direction):
    x, y = st.session_state.pos
    new_x, new_y = x, y
    if direction == "Vorwärts": new_x -= 1
    if direction == "Rückwärts": new_x += 1
    if direction == "Links": new_y -= 1
    if direction == "Rechts": new_y += 1
    
    if WORLD_MAP[new_x][new_y] != 1:
        st.session_state.pos = [new_x, new_y]
    else:
        st.error("Autsch! Du bist gegen eine Wand gelaufen.")

# --- UI DESIGN ---
st.title("🕹️ AI 3D-Quest-Adventure")

col1, col2 = st.columns([2, 1])

with col1:
    # "3D" Ansicht simulieren (ASCII oder Bild-Generierung)
    st.subheader("Deine Sicht")
    x, y = st.session_state.pos
    current_cell = WORLD_MAP[x][y]
    
    if current_cell == 'G':
        st.write("🤖 **Ein KI-Wächter blockiert den Weg!**")
        st.info("System: 'Ich lasse dich nur durch, wenn du mir ein Kompliment machst, das meine Schaltkreise zum Schmelzen bringt.'")
    else:
        st.code("""
             ____________________
            /  ________________  \\
           /  /                \  \\
          /  /      [ Weg ]     \  \\
         /__/____________________\__\\
        """, language="text")

with col2:
    st.subheader("Steuerung")
    c1, c2, c3 = st.columns(3)
    with c2: st.button("⬆️", on_click=move, args=("Vorwärts",))
    with c1: st.button("⬅️", on_click=move, args=("Links",))
    with c3: st.button("➡️", on_click=move, args=("Rechts",))
    with c2: st.button("⬇️", on_click=move, args=("Rückwärts",))

# --- KI INTERAKTION ---
st.divider()
if current_cell == 'G':
    user_input = st.text_input("Was sagst du zur KI?")
    if st.button("Überzeugen"):
        # HIER: KI-API einbinden. Für den Test:
        if len(user_input) > 10:
            st.success("KI: 'Oh... das war schmeichelhaft. Du darfst passieren!'")
            WORLD_MAP[x][y] = 0 # Weg frei machen
        else:
            st.warning("KI: 'Zu schwach. Versuchs nochmal!'")

st.sidebar.markdown(f"**Position:** {st.session_state.pos}")
st.sidebar.markdown(f"**Inventar:** {st.session_state.inventory}")
