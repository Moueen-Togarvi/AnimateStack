<script lang="ts">
    import { onMount } from 'svelte';
    import { api } from '$lib/api';
    import ComponentPreview from '$lib/components/ComponentPreview.svelte';
    import type { Component } from '$lib/types';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';

    let components: Component[] = [];
    let loading = true;
    let searchQuery = '';
    let activeCategory = 'all';

    const categories = [
        { id: 'all', name: 'All Components' },
        { id: 'buttons', name: 'Buttons' },
        { id: 'cards', name: 'Cards' },
        { id: 'loaders', name: 'Loaders' },
        { id: 'inputs', name: 'Inputs' },
        { id: 'navigation', name: 'Navigation' },
        { id: 'backgrounds', name: 'Backgrounds' }
    ];

    async function fetchComponents() {
        loading = true;
        try {
            let url = '/components/';
            const params = new URLSearchParams();
            
            if (searchQuery) params.append('search', searchQuery);
            // In a real app, we'd filter by category on backend too. 
            // For now, we'll filter client-side or assume backend support if implemented.
            
            if (params.toString()) url += `?${params.toString()}`;
            
            const res = await api.get<Component[]>(url);
            
            if (activeCategory !== 'all') {
                // Client-side filtering for now as backend category filtering might need setup
                components = res.filter(c => c.category?.slug === activeCategory || c.category?.name.toLowerCase() === activeCategory);
            } else {
                components = res;
            }
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    }

    function handleSearch() {
        fetchComponents();
    }

    function handleCategoryChange(catId: string) {
        activeCategory = catId;
        fetchComponents();
    }

    onMount(() => {
        fetchComponents();
    });
</script>

<div class="flex h-[calc(100vh-64px)] bg-gray-50 dark:bg-gray-900">
    <!-- Sidebar -->
    <aside class="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col overflow-y-auto">
        <div class="p-6">
            <h2 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">Categories</h2>
            <nav class="space-y-1">
                {#each categories as cat}
                    <button
                        class="w-full flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg transition-all {activeCategory === cat.id ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/30' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'}"
                        on:click={() => handleCategoryChange(cat.id)}
                    >
                        <div class="w-2 h-2 rounded-full {activeCategory === cat.id ? 'bg-white' : 'bg-gray-400'}"></div>
                        {cat.name}
                    </button>
                {/each}
            </nav>
        </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto p-8">
        <div class="max-w-7xl mx-auto">
            <div class="flex items-center justify-between mb-8">
                <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Explore Components</h1>
                <div class="w-96">
                    <div class="relative">
                        <input 
                            type="text" 
                            bind:value={searchQuery}
                            on:keydown={(e) => e.key === 'Enter' && handleSearch()}
                            placeholder="Search components..." 
                            class="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500"
                        />
                        <span class="absolute left-3 top-2.5 text-gray-400">🔍</span>
                    </div>
                </div>
            </div>

            {#if loading}
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {#each Array(6) as _}
                        <div class="aspect-video bg-gray-200 dark:bg-gray-800 rounded-xl animate-pulse"></div>
                    {/each}
                </div>
            {:else if components.length > 0}
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {#each components as component (component.id)}
                        <a href="/components/{component.slug}" class="group relative bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
                            <!-- Preview Container -->
                            <div class="h-56 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 relative overflow-hidden flex items-center justify-center p-4">
                                <div class="absolute inset-0 bg-grid-pattern opacity-5"></div>
                                <div class="relative w-full h-full flex items-center justify-center">
                                    <ComponentPreview code_content={component.code_content} scale={0.6} />
                                </div>
                                <!-- Hover Overlay -->
                                <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                            </div>
                            
                            <!-- Info Section -->
                            <div class="p-5 bg-white dark:bg-gray-800">
                                <div class="flex items-start justify-between mb-2">
                                    <h3 class="text-lg font-bold text-gray-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors line-clamp-1">
                                        {component.title}
                                    </h3>
                                    {#if component.category}
                                        <span class="text-xs px-2 py-1 rounded-full bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 font-medium whitespace-nowrap ml-2">
                                            {component.category.name}
                                        </span>
                                    {/if}
                                </div>
                                <p class="text-sm text-gray-600 dark:text-gray-400 line-clamp-2 mb-4">{component.description}</p>
                                
                                <!-- Stats with Icons -->
                                <div class="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400">
                                    <span class="flex items-center gap-1">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                        </svg>
                                        {component.views}
                                    </span>
                                    <span class="flex items-center gap-1">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                                        </svg>
                                        {component.likes?.length || 0}
                                    </span>
                                </div>
                            </div>
                        </a>
                    {/each}
                </div>
            {:else}
                <div class="text-center py-12 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
                    <p class="text-gray-500 dark:text-gray-400 text-lg">No components found matching your criteria.</p>
                    <button on:click={() => { searchQuery = ''; activeCategory = 'all'; fetchComponents(); }} class="mt-4 text-indigo-600 hover:text-indigo-500">
                        Clear filters
                    </button>
                </div>
            {/if}
        </div>
    </main>
</div>
