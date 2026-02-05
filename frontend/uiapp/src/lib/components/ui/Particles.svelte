<script lang="ts">
    import { onMount, onDestroy } from 'svelte';

    export let color = '#6366f1'; // Indigo-500
    export let count = 50;
    
    let canvas: HTMLCanvasElement;
    let ctx: CanvasRenderingContext2D | null;
    let animationFrame: number;
    let particles: Particle[] = [];
    let width: number;
    let height: number;

    class Particle {
        x: number;
        y: number;
        vx: number;
        vy: number;
        size: number;

        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.vx = (Math.random() - 0.5) * 0.5;
            this.vy = (Math.random() - 0.5) * 0.5;
            this.size = Math.random() * 2 + 1;
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            if (this.x < 0) this.x = width;
            if (this.x > width) this.x = 0;
            if (this.y < 0) this.y = height;
            if (this.y > height) this.y = 0;
        }

        draw() {
            if (!ctx) return;
            ctx.fillStyle = color;
            ctx.globalAlpha = 0.5;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    function resize() {
        if (!canvas) return;
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
    }

    function animate() {
        if (!ctx) return;
        ctx.clearRect(0, 0, width, height);
        
        particles.forEach(p => {
            p.update();
            p.draw();
        });

        // Draw connections
        ctx.strokeStyle = color;
        ctx.lineWidth = 0.5;
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 100) {
                    ctx.globalAlpha = 1 - distance / 100;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }

        animationFrame = requestAnimationFrame(animate);
    }

    onMount(() => {
        ctx = canvas.getContext('2d');
        resize();
        window.addEventListener('resize', resize);

        for (let i = 0; i < count; i++) {
            particles.push(new Particle());
        }

        animate();
    });

    onDestroy(() => {
        if (typeof window !== 'undefined') {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(animationFrame);
        }
    });
</script>

<canvas
    bind:this={canvas}
    class="absolute inset-0 w-full h-full pointer-events-none z-0"
></canvas>
