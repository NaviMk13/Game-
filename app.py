import streamlit as st
import streamlit.components.v1 as components

# Seite konfigurieren
st.set_page_config(page_title="Glitch of Olympus", layout="wide")

# --- CSS FÜR FULLSCREEN LOOK ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    [data-testid="stSidebar"] { background-color: #1a1c24; }
    iframe { border: 2px solid #00ffcc; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: KI & STORY ---
with st.sidebar:
    st.title("📜 Quest-Log")
    st.info("Ziel: Erreiche den Tempel und sprich mit der KI-Pythia.")
    
    st.divider()
    st.subheader("KI-Chat mit den Göttern")
    user_input = st.text_input("Deine Nachricht an die Götter:")
    if st.button("Senden"):
        # Hier kannst du später deinen OpenAI/HuggingFace API Key einbauen
        st.write(f"**Hermes (KI):** 'Dein Prompt {user_input} ist syntaktisch korrekt, aber mein göttlicher Buffer ist voll! Bring mir 3 Datenpakete!'")

# --- DAS 3D-SPIELFELD (Three.js) ---
# Wir nutzen WASD zur Steuerung innerhalb des Iframes.
game_code = """
<div id="ui" style="position: absolute; color: white; padding: 10px; font-family: sans-serif;">
    WASD zum Bewegen | Ziel: Der goldene Würfel (Tempel-Server)
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x001122);
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Licht
    const light = new THREE.PointLight(0xffffff, 1, 100);
    light.position.set(10, 10, 10);
    scene.add(light);
    scene.add(new THREE.AmbientLight(0x404040));

    // Boden (Die Simulationsebene)
    const grid = new THREE.GridHelper(100, 50, 0x00ffcc, 0x444444);
    scene.add(grid);

    // Der "Tempel" (Ein goldener Monolith)
    const geometry = new THREE.BoxGeometry(2, 5, 2);
    const material = new THREE.MeshPhongMaterial({ color: 0xffd700 });
    const temple = new THREE.Mesh(geometry, material);
    temple.position.set(0, 2.5, -20);
    scene.add(temple);

    camera.position.set(0, 1.6, 5);

    // Steuerung
    const keys = {};
    window.addEventListener('keydown', (e) => keys[e.key.toLowerCase()] = true);
    window.addEventListener('keyup', (e) => keys[e.key.toLowerCase()] = false);

    function updatePlayer() {
        const speed = 0.1;
        if (keys['w']) camera.position.z -= speed;
        if (keys['s']) camera.position.z += speed;
        if (keys['a']) camera.position.x -= speed;
        if (keys['d']) camera.position.x += speed;
        
        // Kollisions-Check (Simpel)
        if (camera.position.z < -18 && Math.abs(camera.position.x) < 2) {
            document.getElementById('ui').innerHTML = "SYSTEM: Kontakt mit Tempel-Server hergestellt! Schau in die Sidebar!";
        }
    }

    function animate() {
        requestAnimationFrame(animate);
        updatePlayer();
        temple.rotation.y += 0.01;
        renderer.render(scene, camera);
    }
    animate();
</script>
<style> body { margin: 0; overflow: hidden; } </style>
"""

components.html(game_code, height=600)

st.markdown("---")
st.caption("Nutze die **WASD** Tasten im Fenster oben, um dich zu bewegen. Klicke einmal in das 3D-Feld, damit die Steuerung aktiv wird.")
