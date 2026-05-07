import streamlit as st
import streamlit.components.v1 as components

# Erzwingt das Breitbild-Layout in Streamlit
st.set_page_config(page_title="Odyssey Fullscreen", layout="wide", initial_sidebar_state="collapsed")

# CSS für echtes Fullscreen-Feeling ohne Ränder
st.markdown("""
    <style>
    /* Entfernt Streamlit Header und Padding */
    header {visibility: hidden;}
    .main .block-container {
        padding: 0;
        max-width: 100%;
        height: 100vh;
    }
    iframe {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        border: none;
    }
    #start-overlay {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle, #1a1a2e 0%, #000 100%);
        color: #d4af37;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        z-index: 9999;
        font-family: 'Cinzel', serif;
    }
    .play-btn {
        padding: 20px 50px;
        font-size: 24px;
        background: transparent;
        border: 2px solid #d4af37;
        color: #d4af37;
        cursor: pointer;
        transition: 0.3s;
    }
    .play-btn:hover { background: #d4af37; color: black; }
    </style>
    
    <div id="start-overlay">
        <h1>ODYSSEY ENGINE v8.0</h1>
        <p>GRIECHENLAND LÄDT...</p>
        <button class="play-btn" onclick="startGame()">SPIEL STARTEN</button>
    </div>

    <script>
    function startGame() {
        document.getElementById('start-overlay').style.display = 'none';
        // Sperrt die Maus für das Spiel
        const frame = document.getElementsByTagName('iframe')[0];
        frame.contentWindow.postMessage('lock', '*');
    }
    </script>
    """, unsafe_allow_html=True)

game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #000; }
        canvas { width: 100vw; height: 100vh; display: block; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/PointerLockControls.js"></script>
</head>
<body>
    <script>
        let scene, camera, renderer, controls, player, clock;
        let keys = {};

        init();
        animate();

        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87CEEB);
            scene.fog = new THREE.FogExp2(0x87CEEB, 0.01);
            clock = new THREE.Clock();

            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

            // Licht
            const sun = new THREE.DirectionalLight(0xffffff, 1.2);
            sun.position.set(50, 100, 50);
            scene.add(sun);
            scene.add(new THREE.AmbientLight(0x404040, 1.0));

            // Spieler & Kamera Setup
            player = new THREE.Group();
            scene.add(player);

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            document.body.appendChild(renderer.domElement);

            // Welt-Objekte (Boden & Tempel zur Orientierung)
            const floor = new THREE.Mesh(new THREE.PlaneGeometry(1000, 1000), new THREE.MeshStandardMaterial({color: 0x3d6e1d}));
            floor.rotation.x = -Math.PI / 2;
            scene.add(floor);

            for(let i=0; i<50; i++) {
                const col = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 10), new THREE.MeshStandardMaterial({color: 0xffffff}));
                col.position.set(Math.random()*100-50, 5, Math.random()*100-150);
                scene.add(col);
            }

            // Steuerung
            controls = new THREE.PointerLockControls(camera, document.body);
            
            window.addEventListener('message', (e) => {
                if(e.data === 'lock') controls.lock();
            });

            window.addEventListener('keydown', e => keys[e.code] = true);
            window.addEventListener('keyup', e => keys[e.code] = false);

            window.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });
        }

        function animate() {
            requestAnimationFrame(animate);
            if (controls.isLocked) {
                const delta = clock.getDelta();
                const speed = 15;

                if (keys['KeyW']) controls.moveForward(speed * delta);
                if (keys['KeyS']) controls.moveForward(-speed * delta);
                if (keys['KeyA']) controls.moveRight(-speed * delta);
                if (keys['KeyD']) controls.moveRight(speed * delta);
            }
            renderer.render(scene, camera);
        }
    </script>
</body>
</html>
"""

components.html(game_code, height=2000) # Große Höhe für Fullscreen-Scroll-Vermeidung
