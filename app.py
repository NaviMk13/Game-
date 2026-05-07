import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Antike KI-Simulation", layout="wide")

# Verstecke Streamlit-Elemente für echtes Fullscreen-Feeling
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0px;}
    iframe {border: none;}
    </style>
    """, unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        body { margin: 0; overflow: hidden; font-family: 'Segoe UI', sans-serif; }
        #gui { position: absolute; top: 20px; left: 20px; z-index: 100; color: white; pointer-events: none; }
        #chat-window { 
            position: absolute; bottom: 20px; left: 20px; width: 300px; 
            background: rgba(0,0,0,0.7); border: 1px solid #d4af37; 
            padding: 10px; border-radius: 5px; pointer-events: auto;
        }
        #chat-input { width: 90%; background: #222; color: #d4af37; border: 1px solid #d4af37; padding: 5px; }
        #crosshair { 
            position: absolute; top: 50%; left: 50%; width: 10px; height: 10px; 
            border: 2px solid white; border-radius: 50%; transform: translate(-50%, -50%); 
        }
    </style>
</head>
<body>
    <div id="gui">
        <h1 style="color: #d4af37; margin: 0;">🏺 Project Odyssey-AI</h1>
        <p>Klick ins Bild zum Starten | WASD = Bewegen | SPACE = Springen</p>
    </div>

    <div id="crosshair"></div>

    <div id="chat-window">
        <div id="messages" style="height: 100px; overflow-y: auto; font-size: 12px; margin-bottom: 5px;">
            <span style="color: #d4af37;">Orakel:</span> Willkommen in der Simulation, Sterblicher...
        </div>
        <input type="text" id="chat-input" placeholder="Frag die KI...">
    </div>

    <script>
        let scene, camera, renderer, velocity, moveForward, moveBackward, moveLeft, moveRight, canJump;
        let prevTime = performance.now();
        const objects = [];

        init();
        animate();

        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87ceeb); // Griechischer Himmel
            scene.fog = new THREE.Fog(0x87ceeb, 0, 750);

            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            
            // Licht
            const light = new THREE.HemisphereLight(0xeeeeff, 0x777788, 0.75);
            scene.add(light);
            const dirLight = new THREE.DirectionalLight(0xffffff, 0.5);
            dirLight.position.set(10, 10, 10);
            scene.add(dirLight);

            // Pointer Lock Steuerung (Umgucken wie AC)
            const controls = new function() {
                this.enabled = false;
                document.body.addEventListener('click', () => {
                    document.body.requestPointerLock();
                });
            };

            // Physik-Variablen
            velocity = new THREE.Vector3();
            moveForward = false; moveBackward = false; moveLeft = false; moveRight = false; canJump = false;

            // Boden (Sand/Stein Optik)
            const floorGeo = new THREE.PlaneGeometry(2000, 2000, 100, 100);
            const floorMat = new THREE.MeshPhongMaterial({ color: 0xdeb887 });
            const floor = new THREE.Mesh(floorGeo, floorMat);
            floor.rotation.x = -Math.PI / 2;
            scene.add(floor);

            // Antike Welt-Elemente (Säulen)
            for (let i = 0; i < 50; i++) {
                const colGeo = new THREE.CylinderGeometry(1, 1, 10, 32);
                const colMat = new THREE.MeshPhongMaterial({ color: 0xffffff });
                const col = new THREE.Mesh(colGeo, colMat);
                col.position.set(Math.random()*200 - 100, 5, Math.random()*200 - 100);
                scene.add(col);
                objects.push(col);
            }

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // Event Listeners
            const onKeyDown = (e) => {
                switch(e.code) {
                    case 'KeyW': moveForward = true; break;
                    case 'KeyS': moveBackward = true; break;
                    case 'KeyA': moveLeft = true; break;
                    case 'KeyD': moveRight = true; break;
                    case 'Space': if (canJump) velocity.y += 15; canJump = false; break;
                }
            };
            const onKeyUp = (e) => {
                switch(e.code) {
                    case 'KeyW': moveForward = false; break;
                    case 'KeyS': moveBackward = false; break;
                    case 'KeyA': moveLeft = false; break;
                    case 'KeyD': moveRight = false; break;
                }
            };
            document.addEventListener('keydown', onKeyDown);
            document.addEventListener('keyup', onKeyUp);

            // Mouse Look
            document.addEventListener('mousemove', (e) => {
                if (document.pointerLockElement === document.body) {
                    camera.rotation.y -= e.movementX * 0.002;
                    camera.rotation.x -= e.movementY * 0.002;
                    camera.rotation.x = Math.max(-Math.PI/2, Math.min(Math.PI/2, camera.rotation.x));
                }
            });
            camera.rotation.order = "YXZ";
        }

        function animate() {
            requestAnimationFrame(animate);
            const time = performance.now();
            const delta = (time - prevTime) / 1000;

            velocity.x -= velocity.x * 10.0 * delta;
            velocity.z -= velocity.z * 10.0 * delta;
            velocity.y -= 9.8 * 4.0 * delta; // Gravitation

            if (moveForward) velocity.z -= 150.0 * delta;
            if (moveBackward) velocity.z += 150.0 * delta;
            if (moveLeft) velocity.x -= 150.0 * delta;
            if (moveRight) velocity.x += 150.0 * delta;

            camera.translateX(velocity.x * delta);
            camera.translateY(velocity.y * delta);
            camera.translateZ(velocity.z * delta);

            if (camera.position.y < 1.6) {
                velocity.y = 0;
                camera.position.y = 1.6;
                canJump = true;
            }

            renderer.render(scene, camera);
            prevTime = time;
        }

        // Chat Logik
        document.getElementById('chat-input').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                const msg = this.value;
                document.getElementById('messages').innerHTML += "<div><span style='color:#00ffcc'>Du:</span> " + msg + "</div>";
                this.value = '';
                // Hier könnte man den Text an Streamlit zurückgeben
                setTimeout(() => {
                    document.getElementById('messages').innerHTML += "<div><span style='color:#d4af37'>Orakel:</span> " + msg.length + " Zeichen? Interessantes Opfer...</div>";
                }, 1000);
            }
        });
    </script>
</body>
</html>
"""

components.html(game_html, height=800)
