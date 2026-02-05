<script lang="ts">
    import { onMount } from 'svelte';
    import { api } from '$lib/api';
    import { auth } from '$lib/stores/auth';
    import { goto } from '$app/navigation';
    import type { Component } from '$lib/types';

    let pendingComponents: Component[] = [];
    let loading = true;
    let error = '';

    onMount(async () => {
        if (!$auth.user?.is_staff) {
            goto('/');
            return;
        }
        await loadPendingComponents();
    });

    async function loadPendingComponents() {
        try {
            loading = true;
            // Fetch all components, then filter in frontend or add a query param for 'status=pending'
            // Since we modified get_queryset to show all for admins, we can just fetch and filter.
            // Ideally, backend should support ?status=pending
            const allComponents = await api.get<Component[]>('/components/');
            pendingComponents = allComponents.filter(c => !c.is_approved);
        } catch (e: any) {
            error = e.message;
        } finally {
            loading = false;
        }
    }

    async function handleApprove(slug: string) {
        if (!confirm('Approve this component?')) return;
        try {
            await api.post(`/components/${slug}/approve/`, {});
            await loadPendingComponents();
        } catch (e: any) {
            alert(e.message);
        }
    }

    async function handleReject(slug: string) {
        const reason = prompt('Reason for rejection:');
        if (reason === null) return;
        
        try {
            await api.post(`/components/${slug}/reject/`, { reason });
            await loadPendingComponents();
        } catch (e: any) {
            alert(e.message);
        }
    }
</script>

<div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-8">Admin Dashboard</h1>

    {#if loading}
        <div class="flex justify-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
        </div>
    {:else if error}
        <div class="p-4 bg-red-100 text-red-700 rounded-lg mb-6">{error}</div>
    {:else if pendingComponents.length === 0}
        <div class="text-center py-12 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <p class="text-gray-500 dark:text-gray-400 text-lg">No pending components to review.</p>
        </div>
    {:else}
        <div class="grid grid-cols-1 gap-6">
            {#each pendingComponents as component}
                <div class="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex items-start gap-6">
                    <!-- Preview Thumbnail (iframe or image) -->
                    <div class="w-48 h-32 bg-gray-100 dark:bg-gray-900 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700 relative">
                        {#if component.preview_url}
                             <iframe src={component.preview_url} title={component.title} class="w-full h-full border-0 pointer-events-none" />
                        {:else}
                            <div class="absolute inset-0 flex items-center justify-center text-gray-400 text-xs">No Preview</div>
                        {/if}
                    </div>

                    <div class="flex-1">
                        <div class="flex items-start justify-between mb-2">
                            <div>
                                <h3 class="text-xl font-bold text-gray-900 dark:text-white">{component.title}</h3>
                                <p class="text-sm text-gray-500 dark:text-gray-400">by {component.creator.username} • {new Date(component.created_at).toLocaleDateString()}</p>
                            </div>
                            <div class="flex gap-2">
                                <a 
                                    href="/components/{component.slug}" 
                                    target="_blank"
                                    class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
                                >
                                    Review Code
                                </a>
                            </div>
                        </div>
                        
                        <p class="text-gray-600 dark:text-gray-300 mb-4 line-clamp-2">{component.description}</p>

                        <div class="flex gap-3">
                            <button 
                                on:click={() => handleApprove(component.slug)}
                                class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors"
                            >
                                Approve
                            </button>
                            <button 
                                on:click={() => handleReject(component.slug)}
                                class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors"
                            >
                                Reject
                            </button>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>
