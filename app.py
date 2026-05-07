import streamlit as st

# 1. Grund-Konfiguration
st.set_page_config(page_title="Odyssey Engine v10.0", layout="wide")

# 2. CSS für echtes Fullscreen (entfernt alle Streamlit-Ränder)
st.markdown("""
    <style>
    header {visibility: hidden;}
    .main .block-container {padding: 0; max-width: 100%; height: 100vh;}
    iframe {width: 100vw; height: 100vh; border: none;}
    #start-screen {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle, #1a1a2e 0%, #000 100%);
        color: gold; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 9999;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Das HTML für die Game-Engine
# Hinweis: Wir speichern das HTML in einer Variable, um es dem Iframe zu übergeben.
game_html_content = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/PointerLockControls.js"></script>
    <style>
        body { margin: 0; overflow: hidden; background: #000; }
        #btn { 
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            padding: 20px; border: 2px solid gold; color: gold; background: none;
            cursor: pointer; font-family: serif; font-size: 24px;
        }
    </style>
</head>
<body>
    <button id="btn">GRIECHENLAND BETRETEN</button>
    <script>
        let scene, camera, renderer, controls, clock;
        const btn = document.getElementById('btn');

        btn.addEventListener('click', () => {
            btn.style.display = 'none';
            init();
            animate();
        });

        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87CEEB);
            scene.fog = new THREE.FogExp2(0x87CEEB, 0.01);
            clock = new THREE.Clock();

            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            
            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // Boden & Säulen
            const floor = new THREE.Mesh(new THREE.PlaneGeometry(500, 500), new THREE.MeshStandardMaterial({color: 0x228B22}));
            floor.rotation.x = -Math.PI / 2;
            scene.add(floor);
            
            scene.add(new THREE.AmbientLight(0xffffff, 0.8));
            const sun = new THREE.DirectionalLight(0xffffff, 1);
            sun.position.set(10, 20, 10);
            scene.add(sun);

            for(let i=0; i<30; i++) {
                const s = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 8), new THREE.MeshStandardMaterial({color: 0xffffff}));
                s.position.set(Math.random()*60-30, 4, Math.random()*-60);
                scene.add(s);
            }

            controls = new THREE.PointerLockControls(camera, document.body);
            controls.lock();
        }

        function animate() {
            requestAnimationFrame(animate);
            if(controls.isLocked) {
                // Hier kommt später die WASD Bewegung rein
            }
            renderer.render(scene, camera);
        }
    </script>
</body>
</html>
"""

# 4. Der neue Streamlit-Befehl (Ersetzt st.components.v1.html)
# Wir nutzen srcdoc, um den HTML-Inhalt direkt einzubinden
st.components.v1.html(game_html_content, height=1000, scrolling=False)
