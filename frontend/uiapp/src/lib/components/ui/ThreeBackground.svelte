<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import * as THREE from 'three';

    let container: HTMLDivElement;
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let renderer: THREE.WebGLRenderer;
    let stars: THREE.Points;
    let animationId: number;

    onMount(() => {
        if (!container) return;

        // Scene Setup
        scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x000000, 0.001);

        // Camera Setup
        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 5;

        // Renderer Setup
        renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);

        // Stars
        const starGeometry = new THREE.BufferGeometry();
        const starCount = 5000;
        const posArray = new Float32Array(starCount * 3);
        
        for(let i = 0; i < starCount * 3; i++) {
            posArray[i] = (Math.random() - 0.5) * 20; // Spread stars
        }
        
        starGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        
        // Custom Shader Material for glowing stars
        const starMaterial = new THREE.PointsMaterial({
            size: 0.02,
            color: 0xffffff,
            transparent: true,
            opacity: 0.8,
            blending: THREE.AdditiveBlending
        });

        stars = new THREE.Points(starGeometry, starMaterial);
        scene.add(stars);

        // Nebula Effect (using simple glowing spheres for now, can be upgraded to shaders)
        const nebulaGeometry = new THREE.SphereGeometry(2, 32, 32);
        const nebulaMaterial = new THREE.MeshBasicMaterial({
            color: 0x6366f1, // Indigo
            transparent: true,
            opacity: 0.1,
            side: THREE.BackSide
        });
        const nebula = new THREE.Mesh(nebulaGeometry, nebulaMaterial);
        nebula.position.y = 3;
        scene.add(nebula);

        // Animation Loop
        const animate = () => {
            animationId = requestAnimationFrame(animate);

            // Rotate stars slowly
            stars.rotation.y += 0.0005;
            stars.rotation.x += 0.0002;

            renderer.render(scene, camera);
        };

        animate();

        // Resize Handler
        const handleResize = () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        };

        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
            cancelAnimationFrame(animationId);
            if (container && renderer.domElement) {
                container.removeChild(renderer.domElement);
            }
            // Dispose resources
            starGeometry.dispose();
            starMaterial.dispose();
            nebulaGeometry.dispose();
            nebulaMaterial.dispose();
            renderer.dispose();
        };
    });
</script>

<div 
    bind:this={container} 
    class="fixed inset-0 w-full h-full -z-10 bg-black pointer-events-none"
    style="background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #000000 70%);"
></div>
