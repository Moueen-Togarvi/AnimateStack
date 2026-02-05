<script lang="ts">
    import { page } from '$app/stores';
    import { auth } from '$lib/stores/auth';
    import { goto } from '$app/navigation';

    function handleLogout() {
        auth.logout();
        goto('/login');
    }
</script>

<header class="sticky top-0 z-50 w-full border-b border-[#2a2a2a] bg-[#101010]/80 backdrop-blur-md">
    <nav class="flex h-16 items-center justify-between px-6">
        <!-- Logo -->
        <a href="/" class="flex items-center gap-3 group">
            <div class="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center shadow-lg group-hover:bg-indigo-500 transition-colors">
                <span class="text-white font-bold text-lg">A</span>
            </div>
            <span class="font-bold text-lg tracking-tight text-white">
                AnimateStack
            </span>
        </a>

        <!-- Links -->
        <div class="hidden md:flex items-center gap-6">
            <a href="/components" class="text-sm font-medium text-gray-400 hover:text-white transition-colors {$page.url.pathname.startsWith('/components') ? 'text-white' : ''}">
                Components
            </a>
            <a href="/generate" class="text-sm font-medium text-gray-400 hover:text-white transition-colors {$page.url.pathname === '/generate' ? 'text-white' : ''}">
                AI Generator
            </a>
            <a href="/upload" class="text-sm font-medium text-gray-400 hover:text-white transition-colors {$page.url.pathname === '/upload' ? 'text-white' : ''}">
                Upload
            </a>
        </div>

        <!-- Auth -->
        <div class="flex items-center gap-4">
            <div class="hidden md:flex items-center border-r border-gray-800 pr-4 mr-1">
                 <a href="https://github.com/animate-stack" target="_blank" class="text-gray-400 hover:text-white transition-colors">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                 </a>
            </div>

            {#if $auth.isAuthenticated}
                <div class="relative group">
                    <button class="flex items-center gap-2">
                        <img 
                            src={$auth.user?.avatar || `https://ui-avatars.com/api/?name=${$auth.user?.username}&background=6366f1&color=fff`} 
                            alt="User" 
                            class="w-8 h-8 rounded-full border border-gray-700"
                        />
                    </button>
                    <!-- Dropdown -->
                    <div class="absolute right-0 top-full mt-2 w-48 py-2 bg-[#1e1e1e] border border-[#2a2a2a] rounded-xl shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all transform origin-top-right">
                        <div class="px-4 py-2 border-b border-gray-800 mb-2">
                            <p class="text-sm font-medium text-white truncate">{$auth.user?.username}</p>
                            <p class="text-xs text-gray-500 truncate">{$auth.user?.email}</p>
                        </div>
                        <a href="/u/{$auth.user?.username}" class="block px-4 py-2 text-sm text-gray-300 hover:bg-white/5 hover:text-white">Profile</a>
                        <a href="/dashboard" class="block px-4 py-2 text-sm text-gray-300 hover:bg-white/5 hover:text-white">Dashboard</a>
                        {#if $auth.user?.is_staff}
                            <a href="/admin" class="block px-4 py-2 text-sm text-indigo-400 hover:bg-white/5 hover:text-indigo-300">Admin Panel</a>
                        {/if}
                        <button on:click={handleLogout} class="w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-white/5 hover:text-red-300">Logout</button>
                    </div>
                </div>
            {:else}
                <a href="/login" class="px-4 py-2 text-sm font-medium bg-white text-black rounded-lg hover:bg-gray-200 transition-colors">
                    Log in
                </a>
                <a href="/register" class="px-4 py-2 text-sm font-medium bg-indigo-600 text-white rounded-lg hover:bg-indigo-500 transition-colors">
                    Sign up
                </a>
            {/if}
        </div>
    </nav>
</header>
