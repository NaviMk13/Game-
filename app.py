import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguration ohne Schnickschnack
st.set_page_config(layout="wide")

# 2. CSS direkt einbetten
st.markdown("""
    <style>
    header {visibility: hidden;}
    .main .block-container {padding: 0px;}
    iframe {border: none;}
    </style>
""", unsafe_allow_html=True)

# 3. Der Game-Inhalt als sauberer String (Raw-String gegen Syntax-Fehler)
game_html = r"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background: #000; color: gold; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; font-family: sans-serif; }
        #start-btn { padding: 20px 40px; border: 2px solid gold; cursor: pointer; font-size: 20px; }
    </style>
</head>
<body>
    <div id="start-btn" onclick="initGame()">GRAFIK INITIALISIEREN</div>
    <div id="container"></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        function initGame() {
            document.getElementById('start-btn').style.display = 'none';
            
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87CEEB);
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // Boden
            const floor = new THREE.Mesh(new THREE.PlaneGeometry(100, 100), new THREE.MeshStandardMaterial({color: 0x228B22}));
            floor.rotation.x = -Math.PI / 2;
            scene.add(floor);

            // Licht
            const light = new THREE.DirectionalLight(0xffffff, 1);
            light.position.set(5, 10, 5);
            scene.add(light);
            scene.add(new THREE.AmbientLight(0x404040));

            camera.position.set(0, 5, 10);
            camera.lookAt(0, 0, 0);

            function animate() {
                requestAnimationFrame(animate);
                renderer.render(scene, camera);
            }
            animate();
        }
    </script>
</body>
</html>
"""

# 4. Der entscheidende Befehl: Wir nutzen components.html, 
# aber erzwingen die korrekten Iframe-Rechte
components.html(game_html, height=800)
