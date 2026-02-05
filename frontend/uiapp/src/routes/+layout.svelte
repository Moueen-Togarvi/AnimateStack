<script>
    import "../app.css";
    import { onMount } from 'svelte';
    import { auth } from '$lib/stores/auth';
    import Navbar from '$lib/components/Navbar.svelte';

    onMount(() => {
        auth.initialize();
    });
</script>

<div class="relative min-h-screen bg-[#101010] text-white font-sans selection:bg-indigo-500 selection:text-white">
    <Navbar />
    <main>
        <slot />
    </main>
</div>
