<script lang="ts">
    import type { Component } from '$lib/types';

    export let component: Component;
</script>

<div class="group relative bg-white dark:bg-gray-800 rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700 hover:border-indigo-500 dark:hover:border-indigo-500 transition-all duration-300 hover:shadow-lg">
    <!-- Preview Area -->
    <div class="aspect-video bg-gray-100 dark:bg-gray-900 relative overflow-hidden">
        {#if component.preview_url}
            <iframe 
                src={component.preview_url} 
                title={component.title}
                class="w-full h-full object-cover pointer-events-none"
                loading="lazy"
            />
        {:else}
            <div class="w-full h-full flex items-center justify-center text-gray-400">
                <span class="text-sm">No Preview</span>
            </div>
        {/if}
        
        <!-- Hover Overlay -->
        <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
            <a 
                href="/components/{component.slug}" 
                class="px-4 py-2 bg-white text-gray-900 rounded-lg font-medium hover:bg-gray-100 transition-colors"
            >
                View Details
            </a>
        </div>
    </div>

    <!-- Info -->
    <div class="p-4">
        <div class="flex items-start justify-between mb-2">
            <h3 class="font-semibold text-gray-900 dark:text-gray-100 truncate pr-2">
                {component.title}
            </h3>
            <span class="text-xs font-medium px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-full text-gray-600 dark:text-gray-300">
                {component.category?.name || 'Uncategorized'}
            </span>
        </div>
        
        <div class="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
            <div class="flex items-center gap-2">
                {#if component.creator.avatar}
                    <img src={component.creator.avatar} alt={component.creator.username} class="w-5 h-5 rounded-full" />
                {/if}
                <span>{component.creator.username}</span>
            </div>
            <div class="flex items-center gap-3">
                <span class="flex items-center gap-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                    {component.views}
                </span>
                <span class="flex items-center gap-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>
                    {component.likes_count}
                </span>
            </div>
        </div>
    </div>
</div>
