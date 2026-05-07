import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Odyssey AI Ultimate", layout="wide")

# CSS für das professionelle Gaming-Interface
st.markdown("""
    <style>
    .stApp { margin: 0; padding: 0; overflow: hidden; background: #000; }
    iframe { width: 100vw; height: 100vh; border: none; }
    
    #minimap-container {
        position: fixed; top: 20px; right: 20px;
        width: 180px; height: 180px;
        border: 3px solid #d4af37; border-radius: 50%;
        background: rgba(0, 40, 0, 0.6); overflow: hidden; z-index: 1000;
    }
    #player-dot {
        position: absolute; top: 50%; left: 50%;
        width: 8px; height: 8px; background: white;
        border-radius: 50%; transform: translate(-50%, -50%);
    }
    #game-messages {
        position: fixed; top: 200px; right: 20px;
        color: #d4af37; font-family: 'Cinzel', serif; text-align: right;
    }
    #mount-status {
        position: fixed; bottom: 20px; right: 20px;
        color: white; font-family: sans-serif; font-size: 12px;
    }
    </style>
    
    <div id="minimap-container"><div id="player-dot"></div><div id="npc-dots"></div></div>
    <div id="game-messages"><b>QUEST:</b> Erreiche das Kap von Attika</div>
    <div id="mount-status">[X] Pferd rufen | [F] Aufsteigen/Absteigen</div>
    """, unsafe_allow_html=True)

game_code = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <script>
        // --- ENGINE VARIABLEN ---
        let scene, camera, renderer, player, horse, clock;
        let npcs = [], keys = {}, isPaused = false, isMounted = false;
        let cameraAngleY = 0, cameraAngleX = 0.6;
        let velocity = new THREE.Vector3();
        let particles = [];

        // --- INITIALISIERUNG ---
        init();
        animate();

        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87CEEB);
            scene.fog = new THREE.FogExp2(0x87CEEB, 0.005);
            clock = new THREE.Clock();

            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 2000);

            // LICHT (Dynamisch)
            const sun = new THREE.DirectionalLight(0xfff4e0, 1.5);
            sun.position.set(100, 200, 100);
            sun.castShadow = true;
            scene.add(sun);
            scene.add(new THREE.AmbientLight(0x404040, 1.2));

            // SPIELER MODELL
            player = new THREE.Group();
            const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.5, 1.2), new THREE.MeshStandardMaterial({color: 0x0000ff}));
            body.position.y = 1.1;
            player.add(body);
            scene.add(player);

            // PFERD MODELL (Phobos)
            horse = new THREE.Group();
            const hBody = new THREE.Mesh(new THREE.BoxGeometry(1, 1.5, 2.5), new THREE.MeshStandardMaterial({color: 0x4b3621}));
            hBody.position.y = 1;
            horse.add(hBody);
            const hHead = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.8, 1), new THREE.MeshStandardMaterial({color: 0x4b3621}));
            hHead.position.set(0, 1.8, 1.2);
            horse.add(hHead);
            horse.position.set(10, 0, -10); // Startposition Pferd
            scene.add(horse);

            // TERRAIN & DETAILS
            const floor = new THREE.Mesh(new THREE.PlaneGeometry(2000, 2000), new THREE.MeshStandardMaterial({color: 0x3d6e1d}));
            floor.rotation.x = -Math.PI / 2;
            floor.receiveShadow = true;
            scene.add(floor);

            // NPCs (Gegner/Bürger)
            for(let i=0; i<15; i++) {
                const npc = new THREE.Mesh(new THREE.CapsuleGeometry(0.5, 1), new THREE.MeshStandardMaterial({color: 0xd4af37}));
                npc.position.set(Math.random()*200-100, 1, Math.random()*200-100);
                scene.add(npc);
                npcs.push(npc);
            }

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            document.body.appendChild(renderer.domElement);

            // EVENT HANDLER
            window.addEventListener('keydown', e => {
                keys[e.code] = true;
                if(e.code === 'KeyX') callHorse();
                if(e.code === 'KeyF') toggleMount();
            });
            window.addEventListener('keyup', e => keys[e.code] = false);
            
            document.addEventListener('mousemove', e => {
                if (document.pointerLockElement === document.body) {
                    cameraAngleY -= e.movementX * 0.003;
                    cameraAngleX = Math.max(0.2, Math.min(1.4, cameraAngleX + e.movementY * 0.003));
                }
            });
            document.body.addEventListener('click', () => document.body.requestPointerLock());
        }

        function callHorse() {
            // Pferd teleportiert sich in die Nähe (wie in AC)
            horse.position.set(player.position.x + 5, 0, player.position.z + 5);
        }

        function toggleMount() {
            const dist = player.position.distanceTo(horse.position);
            if(!isMounted && dist < 5) {
                isMounted = true;
                player.visible = false;
            } else if(isMounted) {
                isMounted = false;
                player.visible = true;
                player.position.copy(horse.position);
                player.position.x += 2;
            }
        }

        function animate() {
            requestAnimationFrame(animate);
            const delta = clock.getDelta();

            // BEWEGUNGS LOGIK
            let currentSpeed = isMounted ? 35 : 12;
            let moveZ = (keys['KeyW']?1:0) - (keys['KeyS']?1:0);
            let moveX = (keys['KeyA']?1:0) - (keys['KeyD']?1:0);

            let target = isMounted ? horse : player;

            if(moveX !== 0 || moveZ !== 0) {
                const angle = cameraAngleY + Math.atan2(moveX, moveZ);
                target.position.x += Math.sin(angle) * currentSpeed * delta;
                target.position.z += Math.cos(angle) * currentSpeed * delta;
                target.rotation.y = angle;
                if(isMounted) player.position.copy(horse.position);
            }

            // KAMERA FOLLOW (Smoothed)
            const camDist = isMounted ? 15 : 8;
            camera.position.x = target.position.x - Math.sin(cameraAngleY) * camDist * Math.cos(cameraAngleX);
            camera.position.z = target.position.z - Math.cos(cameraAngleY) * camDist * Math.cos(cameraAngleX);
            camera.position.y = target.position.y + Math.sin(cameraAngleX) * camDist + 3;
            camera.lookAt(target.position.x, target.position.y + 2, target.position.z);

            // MINI-MAP UPDATE (Kommunikation mit UI)
            // Simuliert: In einem echten Build würden wir hier postMessage nutzen.

            renderer.render(scene, camera);
        }
    </script>
</body>
</html>
"""

components.html(game_code, height=1000)
