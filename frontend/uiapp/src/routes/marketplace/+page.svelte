<script lang="ts">
    import { onMount } from 'svelte';
    import { api } from '$lib/api';
    import type { Component } from '$lib/types';
    import ComponentCard from '$lib/components/ComponentCard.svelte';

    let components: Component[] = [];
    let loading = true;

    onMount(async () => {
        try {
            // Fetch premium components (mock filter for now, ideally backend supports ?price_gt=0)
            const allComponents = await api.get<Component[]>('/components/');
            components = allComponents.filter(c => c.price > 0);
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    });
</script>

<div class="container mx-auto px-4 py-8">
    <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">Marketplace</h1>
        <p class="text-xl text-gray-600 dark:text-gray-400">Premium components from top creators</p>
    </div>

    {#if loading}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each Array(3) as _}
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
            No premium components available yet.
        </div>
    {/if}
</div>
