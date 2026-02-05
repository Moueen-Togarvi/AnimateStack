<script lang="ts">
    import { page } from '$app/stores';
    
    const links = [
        { name: 'Universe', icon: 'M21 12a9 9 0 11-18 0 9 9 0 0118 0z', href: '/' }, // Globe/Universe
        { name: 'Challenges', icon: 'M13 10V3L4 14h7v7l9-11h-7z', href: '/challenges' }, // Lightning/Challenge
        { name: 'Spotlight', icon: 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z', href: '/spotlight' }, // Star
    ];

    const categories = [
        { name: 'All', icon: 'M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z', href: '/components' }, // Grid
        { name: 'Buttons', icon: 'M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122', href: '/components?cat=buttons' }, // Cursor/Click
        { name: 'Cards', icon: 'M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z', href: '/components?cat=cards' }, // Layout
        { name: 'Loaders', icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z', href: '/components?cat=loaders' }, // Clock
        { name: 'Inputs', icon: 'M3 10h18M3 14h18m-9-4v8m-7-2.5l5 5M5 10.5l5-5', href: '/components?cat=inputs' }, // Text/Input
    ];
</script>

<aside class="w-64 h-[calc(100vh-64px)] fixed top-16 left-0 z-40 hidden lg:flex flex-col bg-[#101010] border-r border-[#2a2a2a] py-6 px-4 overflow-y-auto">
    <!-- Navigation -->
    <div class="mb-8">
        <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-4 px-3">Discover</h3>
        <nav class="space-y-1">
            {#each links as link}
                <a 
                    href={link.href}
                    class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-all group {$page.url.pathname === link.href ? 'bg-white/5 text-white' : ''}"
                >
                    <svg class="w-5 h-5 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={link.icon}></path></svg>
                    <span class="font-medium text-sm">{link.name}</span>
                </a>
            {/each}
        </nav>
    </div>

    <!-- Categories -->
    <div class="flex-1">
        <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-4 px-3">Categories</h3>
        <nav class="space-y-1">
            {#each categories as cat}
                <a 
                    href={cat.href}
                    class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-all group"
                >
                    <svg class="w-5 h-5 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={cat.icon}></path></svg>
                    <span class="font-medium text-sm">{cat.name}</span>
                </a>
            {/each}
        </nav>
    </div>

    <!-- Footer -->
    <div class="mt-auto pt-6 border-t border-[#2a2a2a]">
        <a href="/upload" class="flex items-center justify-center gap-2 w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-bold transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
            Create
        </a>
    </div>
</aside>
