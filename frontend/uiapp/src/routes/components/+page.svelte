<script lang="ts">
    import { onMount } from 'svelte';
    import { api } from '$lib/api';
    import type { Component } from '$lib/types';
    import ComponentCard from '$lib/components/ComponentCard.svelte';

    let components: Component[] = [];
    let loading = true;

    onMount(async () => {
        try {
            components = await api.get<Component[]>('/components/');
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    });
</script>

<div class="container mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Explore Components</h1>
        <div class="flex gap-4">
            <!-- Search/Filter placeholders -->
            <input 
                type="text" 
                placeholder="Search..." 
                class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500"
            />
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
                <ComponentCard {component} />
            {/each}
        </div>
    {:else}
        <div class="text-center py-12 text-gray-500 dark:text-gray-400">
            No components found. Be the first to create one!
        </div>
    {/if}
</div>
