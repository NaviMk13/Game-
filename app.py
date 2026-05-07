import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Ancient AI World", layout="wide")

# CSS für kompletten Fullscreen und UI-Overlays
st.markdown("""
    <style>
    .stApp { margin: 0; padding: 0; }
    iframe { width: 100vw; height: 100vh; position: fixed; top: 0; left: 0; }
    #chat-overlay {
        position: fixed; bottom: 30px; left: 30px; width: 350px;
        background: rgba(10, 10, 10, 0.85); border: 2px solid #d4af37;
        border-radius: 15px; padding: 15px; z-index: 1000; color: white;
        font-family: 'Georgia', serif; box-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style> body { margin: 0; overflow: hidden; } </style>
</head>
<body>
    <div id="chat-overlay">
        <h3 style="margin-top:0; color:#d4af37;">📜 Das Orakel von Streamlit</h3>
        <div id="messages" style="height: 120px; overflow-y: auto; font-size: 14px;">
            Willkommen, Reisender. Bewege dich mit WASD und schau dich mit der Maus um. Springe mit der Leertaste über die Ruinen.
        </div>
        <input type="text" id="chat-input" style="width:100%; background:#222; border:1px solid #d4af37; color:white; padding:5px; margin-top:10px;" placeholder="Sprich mit der Welt...">
    </div>

    <script>
        let scene, camera, renderer, velocity, moveForward, moveBackward, moveLeft, moveRight, canJump;
        let prevTime = performance.now();
        
        init();
        animate();

        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0xaaccff);
            scene.fog = new THREE.FogExp2(0xaaccff, 0.002);

            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 2000);
            camera.position.y = 2;

            // --- LICHT & SCHATTEN ---
            const ambientLight = new THREE.AmbientLight(0x404040, 1.5); 
            scene.add(ambientLight);

            const sunLight = new THREE.DirectionalLight(0xffffff, 1.2);
            sunLight.position.set(50, 100, 50);
            sunLight.castShadow = true;
            // Schatten-Qualität optimieren
            sunLight.shadow.mapSize.width = 2048;
            sunLight.shadow.mapSize.height = 2048;
            sunLight.shadow.camera.left = -100;
            sunLight.shadow.camera.right = 100;
            sunLight.shadow.camera.top = 100;
            sunLight.shadow.camera.bottom = -100;
            scene.add(sunLight);

            // --- WELTDESIGN ---
            // Boden mit Textur-Farbe
            const floorGeo = new THREE.PlaneGeometry(1000, 1000);
            const floorMat = new THREE.MeshPhongMaterial({ color: 0x3a5f0b }); // Dunkelgrünes Gras
            const floor = new THREE.Mesh(floorGeo, floorMat);
            floor.rotation.x = -Math.PI / 2;
            floor.receiveShadow = true;
            scene.add(floor);

            // Bäume & Statuen generieren
            for (let i = 0; i < 150; i++) {
                const x = Math.random() * 400 - 200;
                const z = Math.random() * 400 - 200;
                if (Math.abs(x) < 10 && Math.abs(z) < 10) continue; // Startplatz frei lassen

                if (Math.random() > 0.2) {
                    // Ein Baum (Zypresse)
                    const trunkGeo = new THREE.CylinderGeometry(0.2, 0.2, 2);
                    const leafGeo = new THREE.ConeGeometry(1, 8, 8);
                    const matTrunk = new THREE.MeshPhongMaterial({color: 0x4b3621});
                    const matLeaf = new THREE.MeshPhongMaterial({color: 0x0b3d0b});
                    
                    const trunk = new THREE.Mesh(trunkGeo, matTrunk);
                    const leaf = new THREE.Mesh(leafGeo, matLeaf);
                    trunk.position.set(x, 1, z);
                    leaf.position.set(x, 5, z);
                    trunk.castShadow = true; leaf.castShadow = true;
                    scene.add(trunk); scene.add(leaf);
                } else {
                    // Eine "Statue" (Antiker Monolith)
                    const statGeo = new THREE.BoxGeometry(2, 6, 2);
                    const statMat = new THREE.MeshPhongMaterial({color: 0xcccccc});
                    const statue = new THREE.Mesh(statGeo, statMat);
                    statue.position.set(x, 3, z);
                    statue.rotation.y = Math.random() * Math.PI;
                    statue.castShadow = true;
                    scene.add(statue);
                }
            }

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // --- STEUERUNG ---
            velocity = new THREE.Vector3();
            moveForward = false; moveBackward = false; moveLeft = false; moveRight = false; canJump = false;

            document.addEventListener('click', () => document.body.requestPointerLock());
            
            document.addEventListener('keydown', (e) => {
                switch(e.code) {
                    case 'KeyW': moveForward = true; break;
                    case 'KeyS': moveBackward = true; break;
                    case 'KeyA': moveLeft = true; break;
                    case 'KeyD': moveRight = true; break;
                    case 'Space': if (canJump) velocity.y += 12; canJump = false; break;
                }
            });
            document.addEventListener('keyup', (e) => {
                switch(e.code) {
                    case 'KeyW': moveForward = false; break;
                    case 'KeyS': moveBackward = false; break;
                    case 'KeyA': moveLeft = false; break;
                    case 'KeyD': moveRight = false; break;
                }
            });

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
            velocity.y -= 30.0 * delta; // Gravitation

            let dir = new THREE.Vector3();
            camera.getWorldDirection(dir);
            dir.y = 0; dir.normalize();
            let side = new THREE.Vector3().crossVectors(camera.up, dir).normalize();

            if (moveForward) velocity.add(dir.multiplyScalar(80 * delta));
            if (moveBackward) velocity.sub(dir.multiplyScalar(80 * delta));
            if (moveLeft) velocity.add(side.multiplyScalar(80 * delta));
            if (moveRight) velocity.sub(side.multiplyScalar(80 * delta));

            camera.position.x += velocity.x * delta;
            camera.position.z += velocity.z * delta;
            camera.position.y += velocity.y * delta;

            if (camera.position.y < 2) {
                velocity.y = 0;
                camera.position.y = 2;
                canJump = true;
            }

            renderer.render(scene, camera);
            prevTime = time;
        }

        // Chat Input Logic
        document.getElementById('chat-input').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                const text = this.value;
                document.getElementById('messages').innerHTML += "<div><b style='color:#00ffcc'>Du:</b> "+text+"</div>";
                this.value = '';
                // Hier könnte man die Antwort einer KI simulieren
                setTimeout(() => {
                    document.getElementById('messages').innerHTML += "<div><b style='color:#d4af37'>Orakel:</b> Deine Worte hallen durch die Hallen von Hades...</div>";
                }, 800);
            }
        });
    </script>
</body>
</html>
"""

components.html(game_html, height=1000)
