import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Odyssey AI Engine", layout="wide")

# CSS für Fullscreen ohne Scrollbars
st.markdown("""
    <style>
    .stApp { margin: 0; padding: 0; overflow: hidden; }
    iframe { width: 100vw; height: 100vh; border: none; }
    #game-ui {
        position: fixed; bottom: 10%; left: 50%; transform: translateX(-50%);
        color: #d4af37; font-family: 'Cinzel', serif; text-align: center;
        text-shadow: 2px 2px 4px #000; z-index: 100; pointer-events: none;
        font-size: 24px; display: none;
    }
    </style>
    <div id="game-ui">Drücke 'E' um mit dem Gott zu sprechen</div>
    """, unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style> body { margin: 0; cursor: crosshair; } </style>
</head>
<body>
    <script>
        let scene, camera, renderer, velocity, moveForward, moveBackward, moveLeft, moveRight, canJump;
        let prevTime = performance.now();
        let npcs = [];
        
        init();
        animate();

        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0xadd8e6);
            scene.fog = new THREE.Fog(0xadd8e6, 0, 100);

            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.y = 2;

            // Licht (Sonne)
            const light = new THREE.DirectionalLight(0xffffff, 1.0);
            light.position.set(10, 20, 10);
            light.castShadow = true;
            scene.add(light);
            scene.add(new THREE.AmbientLight(0x404040, 2));

            // Boden (Marmor/Stein-Optik)
            const floorGeo = new THREE.PlaneGeometry(1000, 1000);
            const floorMat = new THREE.MeshStandardMaterial({ color: 0xcccccc, roughness: 0.2 });
            const floor = new THREE.Mesh(floorGeo, floorMat);
            floor.rotation.x = -Math.PI / 2;
            scene.add(floor);

            // NPCs & Welt-Details (Säulengänge)
            for (let i = 0; i < 40; i++) {
                const x = Math.random() * 200 - 100;
                const z = Math.random() * 200 - 100;
                
                // Eine Säule
                const cylGeo = new THREE.CylinderGeometry(0.8, 0.8, 8, 32);
                const cylMat = new THREE.MeshStandardMaterial({color: 0xffffff});
                const col = new THREE.Mesh(cylGeo, cylMat);
                col.position.set(x, 4, z);
                scene.add(col);

                // NPCs (Goldene Gestalten)
                if(i % 5 === 0) {
                    const npcGeo = new THREE.SphereGeometry(1, 32, 32);
                    const npcMat = new THREE.MeshStandardMaterial({color: 0xd4af37, metalness: 1});
                    const npc = new THREE.Mesh(npcGeo, npcMat);
                    npc.position.set(x + 2, 1, z + 2);
                    npc.userData = { name: "Gott " + i, msg: "Ich bin eine KI. Bringe mir 10 Zeilen Code!" };
                    scene.add(npc);
                    npcs.push(npc);
                }
            }

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // MOUSE LOOK (Pointer Lock)
            document.addEventListener('click', () => {
                document.body.requestPointerLock();
            });

            document.addEventListener('mousemove', (e) => {
                if (document.pointerLockElement === document.body) {
                    camera.rotation.y -= e.movementX * 0.002;
                    camera.rotation.x -= e.movementY * 0.002;
                    camera.rotation.x = Math.max(-Math.PI/2, Math.min(Math.PI/2, camera.rotation.x));
                }
            });
            camera.rotation.order = "YXZ";

            // WASD & Physik
            velocity = new THREE.Vector3();
            moveForward = moveBackward = moveLeft = moveRight = false;

            document.addEventListener('keydown', (e) => {
                if(e.code === 'KeyW') moveForward = true;
                if(e.code === 'KeyS') moveBackward = true;
                if(e.code === 'KeyA') moveLeft = true;
                if(e.code === 'KeyD') moveRight = true;
                if(e.code === 'Space' && canJump) { velocity.y += 10; canJump = false; }
            });
            document.addEventListener('keyup', (e) => {
                if(e.code === 'KeyW') moveForward = false;
                if(e.code === 'KeyS') moveBackward = false;
                if(e.code === 'KeyA') moveLeft = false;
                if(e.code === 'KeyD') moveRight = false;
            });
        }

        function animate() {
            requestAnimationFrame(animate);
            const time = performance.now();
            const delta = (time - prevTime) / 1000;

            velocity.x -= velocity.x * 10.0 * delta;
            velocity.z -= velocity.z * 10.0 * delta;
            velocity.y -= 25.0 * delta; // Schwerkraft

            let dir = new THREE.Vector3();
            camera.getWorldDirection(dir);
            dir.y = 0; dir.normalize();
            let side = new THREE.Vector3().crossVectors(camera.up, dir).normalize();

            if (moveForward) velocity.add(dir.multiplyScalar(100 * delta));
            if (moveBackward) velocity.sub(dir.multiplyScalar(100 * delta));
            if (moveLeft) velocity.add(side.multiplyScalar(100 * delta));
            if (moveRight) velocity.sub(side.multiplyScalar(100 * delta));

            camera.position.add(new THREE.Vector3(velocity.x * delta, velocity.y * delta, velocity.z * delta));

            if (camera.position.y < 2) {
                velocity.y = 0;
                camera.position.y = 2;
                canJump = true;
            }

            // NPC Check (Interaktion)
            let nearNPC = false;
            npcs.forEach(npc => {
                if(camera.position.distanceTo(npc.position) < 5) {
                    window.parent.document.getElementById('game-ui').style.display = 'block';
                    window.parent.document.getElementById('game-ui').innerText = npc.userData.msg;
                    nearNPC = true;
                }
            });
            if(!nearNPC) window.parent.document.getElementById('game-ui').style.display = 'none';

            renderer.render(scene, camera);
            prevTime = time;
        }
    </script>
</body>
</html>
"""

components.html(game_html, height=1000)
