<script lang="ts">
    import { onMount } from 'svelte';
    import { api } from '$lib/api';
    import ThreeViewer from '$lib/components/ThreeViewer.svelte';

    let assets: any[] = [];
    let loading = true;

    onMount(async () => {
        try {
            assets = await api.get<any[]>('/assets/');
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    });
</script>

<div class="container mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Assets Library</h1>
        <a href="/assets/upload" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
            Upload Asset
        </a>
    </div>

    {#if loading}
        <div class="text-center py-12">Loading...</div>
    {:else if assets.length > 0}
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            {#each assets as asset}
                <div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
                    <div class="aspect-square bg-gray-100 dark:bg-gray-900 relative">
                        {#if asset.asset_type === '3d'}
                            <ThreeViewer modelUrl={asset.file} />
                        {:else}
                            <img src={asset.file} alt="Asset" class="w-full h-full object-cover" />
                        {/if}
                    </div>
                    <div class="p-4">
                        <div class="text-sm font-medium text-gray-900 dark:text-white truncate">
                            {asset.file.split('/').pop()}
                        </div>
                        <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                            {asset.asset_type.toUpperCase()}
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {:else}
        <div class="text-center py-12 text-gray-500 dark:text-gray-400">
            No assets found. Upload one to get started.
        </div>
    {/if}
</div>
