<script lang="ts">
    import ComponentPreview from '$lib/components/ComponentPreview.svelte';
    import Sidebar from '$lib/components/Sidebar.svelte';
    import { onMount } from 'svelte';
    import { api } from '$lib/api';
    import type { Component } from '$lib/types';

    let featuredComponents: Component[] = [];
    let searchQuery = '';

    onMount(async () => {
        try {
            featuredComponents = await api.get<Component[]>('/components/');
        } catch (e) {
            console.error(e);
        }
    });
</script>

<div class="min-h-screen bg-[#101010]">
    <Sidebar />

    <!-- Main Content -->
    <div class="lg:ml-64 min-h-screen relative z-10">
        <!-- Hero Section -->
        <div class="pt-20 pb-12 px-8 border-b border-[#2a2a2a]">
            <div class="max-w-5xl mx-auto text-center">
                <h1 class="text-4xl md:text-6xl font-black tracking-tight text-white mb-6">
                    Open-Source UI Elements
                    <span class="block text-indigo-500 mt-2">made with CSS & HTML</span>
                </h1>
                <p class="text-lg text-gray-400 mb-10 max-w-2xl mx-auto">
                    AnimateStack is a library of free and customizable UI components.
                    <br class="hidden md:block" />
                    Copy & paste them into your project.
                </p>

                <!-- Search Bar -->
                <div class="relative max-w-2xl mx-auto group mb-12">
                    <div class="relative flex items-center bg-[#1e1e1e] border border-[#2a2a2a] rounded-xl p-2 focus-within:border-indigo-500 focus-within:ring-1 focus-within:ring-indigo-500 transition-all shadow-lg">
                        <span class="pl-4 text-gray-500">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                        </span>
                        <input 
                            type="text" 
                            bind:value={searchQuery}
                            placeholder="Search for buttons, cards, loaders..." 
                            class="w-full bg-transparent border-none text-white placeholder-gray-500 focus:ring-0 text-base py-2.5 px-4"
                        />
                        <div class="hidden md:flex items-center gap-2 pr-2">
                            <kbd class="px-2 py-1 bg-[#2a2a2a] rounded text-xs text-gray-400 font-mono border border-[#3a3a3a]">CTRL K</kbd>
                        </div>
                    </div>
                </div>

                <!-- Filter Tabs -->
                <div class="flex items-center justify-center gap-2 overflow-x-auto pb-2">
                    {#each ['Trending', 'New', 'Following', 'Editors Choice'] as tab, i}
                        <button class="px-5 py-2 rounded-lg text-sm font-bold transition-all {i === 0 ? 'bg-white text-black' : 'text-gray-400 hover:text-white hover:bg-[#1e1e1e]'}">
                            {tab}
                        </button>
                    {/each}
                </div>
            </div>
        </div>

        <!-- Components Grid -->
        <div class="p-8 bg-[#101010]">
            <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-6 max-w-[1920px] mx-auto">
                {#each featuredComponents as component}
                    <a href="/components/{component.slug}" class="group relative bg-[#1e1e1e] rounded-xl border border-[#2a2a2a] overflow-hidden hover:border-indigo-500 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:shadow-indigo-500/10">
                        <!-- Preview -->
                        <div class="h-56 bg-[#151515] relative overflow-hidden flex items-center justify-center p-4">
                            <div class="absolute inset-0 bg-[url('/grid-light.svg')] bg-center opacity-5"></div>
                            <div class="relative w-full h-full flex items-center justify-center transform group-hover:scale-105 transition-transform duration-500">
                                <ComponentPreview code_content={component.code_content} scale={0.7} />
                            </div>
                            
                            <!-- Quick Actions (Hover) -->
                            <div class="absolute top-3 right-3 flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-all duration-200 translate-x-2 group-hover:translate-x-0">
                                <button class="p-2 bg-[#2a2a2a] text-white rounded-lg hover:bg-indigo-600 transition-colors shadow-lg border border-[#3a3a3a]" title="Copy Code">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                                </button>
                                <button class="p-2 bg-[#2a2a2a] text-white rounded-lg hover:bg-pink-600 transition-colors shadow-lg border border-[#3a3a3a]" title="Like">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
                                </button>
                            </div>
                        </div>
                        
                        <!-- Info -->
                        <div class="p-4 border-t border-[#2a2a2a] bg-[#1e1e1e]">
                            <div class="flex items-center justify-between mb-3">
                                <h3 class="text-base font-bold text-gray-200 group-hover:text-white transition-colors truncate pr-2">{component.title}</h3>
                                {#if component.category}
                                    <span class="text-[10px] uppercase font-bold tracking-wider px-2 py-1 rounded bg-[#2a2a2a] text-gray-400">
                                        {component.category.name}
                                    </span>
                                {/if}
                            </div>
                            
                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-2">
                                    <img 
                                        src={component.creator.avatar || `https://ui-avatars.com/api/?name=${component.creator.username}&background=random`} 
                                        alt={component.creator.username} 
                                        class="w-5 h-5 rounded-full border border-[#3a3a3a]" 
                                    />
                                    <span class="text-xs font-medium text-gray-500 hover:text-gray-300 transition-colors">@{component.creator.username}</span>
                                </div>
                                <div class="flex items-center gap-3 text-xs font-medium text-gray-600">
                                    <span class="flex items-center gap-1"><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg> {component.views}</span>
                                </div>
                            </div>
                        </div>
                    </a>
                {/each}
            </div>
        </div>
    </div>
</div>
