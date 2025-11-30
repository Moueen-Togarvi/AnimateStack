<script lang="ts">
    import { onMount } from 'svelte';
    import { api } from '$lib/api';
    import { auth } from '$lib/stores/auth';
    import type { Component } from '$lib/types';
    import ComponentCard from '$lib/components/ComponentCard.svelte';

    let components: Component[] = [];
    let loading = true;
    let stats = {
        views: 0,
        likes: 0,
        downloads: 0,
        earnings: 0
    };

    $: user = $auth.user;

    onMount(async () => {
        if (!user) return;
        
        try {
            components = await api.get<Component[]>(`/components/?creator=${user.id}`);
            
            // Calculate stats
            stats.views = components.reduce((acc, c) => acc + (c.views || 0), 0);
            stats.likes = components.reduce((acc, c) => acc + (c.likes_count || 0), 0);
            stats.downloads = components.reduce((acc, c) => acc + (c.downloads || 0), 0);
            // Mock earnings calculation
            stats.earnings = components.reduce((acc, c) => acc + (parseFloat(c.price.toString()) * (c.downloads || 0)), 0);

        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    });

    async function handleDelete(id: number) {
        if (!confirm('Are you sure you want to delete this component?')) return;
        
        try {
            await api.delete(`/components/${id}/`);
            components = components.filter(c => c.id !== id);
        } catch (e) {
            console.error(e);
            alert('Failed to delete component');
        }
    }
</script>

<div class="container mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-8">
        <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Creator Dashboard</h1>
            <p class="text-gray-600 dark:text-gray-400">Manage your components and view performance</p>
        </div>
        <a href="/generate" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
            Create New
        </a>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
        <div class="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Total Views</div>
            <div class="text-3xl font-bold text-gray-900 dark:text-white">{stats.views}</div>
        </div>
        <div class="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Total Likes</div>
            <div class="text-3xl font-bold text-gray-900 dark:text-white">{stats.likes}</div>
        </div>
        <div class="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Downloads</div>
            <div class="text-3xl font-bold text-gray-900 dark:text-white">{stats.downloads}</div>
        </div>
        <div class="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Earnings</div>
            <div class="text-3xl font-bold text-green-600 dark:text-green-400">${stats.earnings.toFixed(2)}</div>
        </div>
    </div>

    <!-- Components List -->
    <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">Your Components</h2>
    
    {#if loading}
        <div class="text-center py-12">Loading...</div>
    {:else if components.length > 0}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each components as component (component.id)}
                <div class="relative group">
                    <ComponentCard {component} />
                    <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-2">
                        <button 
                            class="p-2 bg-white dark:bg-gray-800 text-red-600 rounded-lg shadow-lg hover:bg-red-50 dark:hover:bg-red-900/30"
                            on:click|preventDefault={() => handleDelete(component.id)}
                        >
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                        </button>
                    </div>
                </div>
            {/each}
        </div>
    {:else}
        <div class="text-center py-12 bg-gray-50 dark:bg-gray-800/50 rounded-xl border-2 border-dashed border-gray-200 dark:border-gray-700">
            <p class="text-gray-500 dark:text-gray-400 mb-4">You haven't created any components yet.</p>
            <a href="/generate" class="text-indigo-600 hover:text-indigo-500 font-medium">Generate your first component &rarr;</a>
        </div>
    {/if}
</div>
