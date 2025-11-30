<script lang="ts">
    import { auth } from '$lib/stores/auth';
    import { page } from '$app/stores';

    $: user = $auth.user;
    $: activeRoute = $page.url.pathname;

    const links = [
        { href: '/components', label: 'Components' },
        { href: '/marketplace', label: 'Marketplace' },
        { href: '/generate', label: 'AI Generator' },
    ];
</script>

<nav class="sticky top-0 z-50 w-full border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-900/80 backdrop-blur">
    <div class="container mx-auto px-4 h-16 flex items-center justify-between">
        <a href="/" class="flex items-center gap-2 font-bold text-xl text-gray-900 dark:text-white">
            <div class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
            </div>
            AnimateStack
        </a>

        <div class="hidden md:flex items-center gap-6">
            {#each links as link}
                <a 
                    href={link.href}
                    class="text-sm font-medium transition-colors hover:text-indigo-600 dark:hover:text-indigo-400 {activeRoute.startsWith(link.href) ? 'text-indigo-600 dark:text-indigo-400' : 'text-gray-600 dark:text-gray-300'}"
                >
                    {link.label}
                </a>
            {/each}
        </div>

        <div class="flex items-center gap-4">
            {#if user}
                <div class="flex items-center gap-4">
                    <a href="/dashboard" class="text-sm font-medium text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400">Dashboard</a>
                    <div class="flex items-center gap-3">
                        <img src={user.avatar || `https://ui-avatars.com/api/?name=${user.username}`} alt={user.username} class="w-8 h-8 rounded-full bg-gray-200" />
                        <button 
                            on:click={() => { auth.logout(); window.location.href = '/login'; }}
                            class="text-sm font-medium text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
                        >
                            Logout
                        </button>
                    </div>
                </div>
            {:else}
                <a href="/login" class="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">Log in</a>
                <a href="/register" class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors">Sign up</a>
            {/if}
        </div>
    </div>
</nav>
