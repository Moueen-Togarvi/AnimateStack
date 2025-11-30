<script>
    import "../app.css";
    import { onMount } from 'svelte';
    import { auth } from '$lib/stores/auth';
    import Navbar from '$lib/components/Navbar.svelte';

    onMount(() => {
        auth.initialize();
    });
</script>

<div class="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 font-sans">
    <Navbar />
    <main>
        <slot />
    </main>
</div>
