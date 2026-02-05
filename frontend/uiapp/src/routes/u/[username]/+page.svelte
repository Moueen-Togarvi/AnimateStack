<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { api } from '$lib/api';
    import ComponentPreview from '$lib/components/ComponentPreview.svelte';
    import type { Component } from '$lib/types';

    let username = $page.params.username;
    let user: any = null;
    let components: Component[] = [];
    let loading = true;
    let activeTab = 'created';

    onMount(async () => {
        try {
            // Fetch User Profile
            user = await api.get(`/auth/profile/${username}/`);
            
            // Fetch User Components (We might need a filter on the components endpoint)
            // For now, fetching all and filtering client side (Not ideal for prod)
            // TODO: Add ?creator=username to components endpoint
            const allComponents = await api.get<Component[]>('/components/');
            components = allComponents.filter(c => c.creator.username === username);
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    });
</script>

<div class="min-h-screen pt-24 pb-12 px-4 lg:px-8">
    {#if loading}
        <div class="flex items-center justify-center h-64">
            <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
    {:else if user}
        <!-- Profile Header -->
        <div class="max-w-6xl mx-auto mb-12">
            <div class="bg-black/40 backdrop-blur-xl border border-white/10 rounded-3xl p-8 flex flex-col md:flex-row items-center md:items-start gap-8">
                <!-- Avatar -->
                <div class="relative group">
                    <div class="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full blur opacity-50 group-hover:opacity-75 transition duration-500"></div>
                    <img 
                        src={user.avatar || `https://ui-avatars.com/api/?name=${user.username}&background=random`} 
                        alt={user.username} 
                        class="relative w-32 h-32 rounded-full border-4 border-black object-cover"
                    />
                </div>

                <!-- Info -->
                <div class="flex-1 text-center md:text-left">
                    <h1 class="text-4xl font-bold text-white mb-2">{user.username}</h1>
                    {#if user.bio}
                        <p class="text-gray-400 max-w-2xl mb-6">{user.bio}</p>
                    {/if}

                    <!-- Social Links -->
                    <div class="flex items-center justify-center md:justify-start gap-4">
                        {#if user.github_handle}
                            <a href="https://github.com/{user.github_handle}" target="_blank" class="p-2 bg-white/5 rounded-lg hover:bg-white/10 transition-colors text-gray-300 hover:text-white">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                            </a>
                        {/if}
                        {#if user.twitter_handle}
                            <a href="https://twitter.com/{user.twitter_handle}" target="_blank" class="p-2 bg-white/5 rounded-lg hover:bg-white/10 transition-colors text-gray-300 hover:text-white">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/></svg>
                            </a>
                        {/if}
                        {#if user.website}
                            <a href={user.website} target="_blank" class="p-2 bg-white/5 rounded-lg hover:bg-white/10 transition-colors text-gray-300 hover:text-white">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>
                            </a>
                        {/if}
                    </div>
                </div>

                <!-- Stats -->
                <div class="flex gap-8 text-center">
                    <div>
                        <div class="text-2xl font-bold text-white">{components.length}</div>
                        <div class="text-xs text-gray-500 uppercase tracking-wider">Creations</div>
                    </div>
                    <div>
                        <div class="text-2xl font-bold text-white">0</div>
                        <div class="text-xs text-gray-500 uppercase tracking-wider">Likes</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Content Tabs -->
        <div class="max-w-7xl mx-auto">
            <div class="flex items-center justify-center gap-8 mb-12 border-b border-white/10">
                {#each ['Created', 'Liked', 'Collections'] as tab}
                    <button 
                        class="px-4 py-4 text-sm font-medium border-b-2 transition-colors {activeTab === tab.toLowerCase() ? 'border-indigo-500 text-white' : 'border-transparent text-gray-500 hover:text-gray-300'}"
                        on:click={() => activeTab = tab.toLowerCase()}
                    >
                        {tab}
                    </button>
                {/each}
            </div>

            <!-- Grid -->
            {#if activeTab === 'created'}
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {#each components as component}
                        <a href="/components/{component.slug}" class="group relative bg-black/40 backdrop-blur-md rounded-3xl border border-white/10 overflow-hidden hover:border-indigo-500/50 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_10px_40px_rgba(99,102,241,0.15)]">
                            <div class="h-60 bg-black/20 relative overflow-hidden flex items-center justify-center p-6">
                                <div class="absolute inset-0 bg-[url('/grid.svg')] bg-center opacity-20"></div>
                                <div class="relative w-full h-full flex items-center justify-center transform group-hover:scale-105 transition-transform duration-500">
                                    <ComponentPreview code_content={component.code_content} scale={0.65} />
                                </div>
                            </div>
                            <div class="p-5 border-t border-white/5">
                                <h3 class="text-lg font-bold text-gray-200 group-hover:text-white transition-colors truncate">{component.title}</h3>
                                <div class="flex items-center justify-between mt-2 text-xs text-gray-500">
                                    <span>{new Date(component.created_at).toLocaleDateString()}</span>
                                    <div class="flex gap-3">
                                        <span>👁️ {component.views}</span>
                                        <span>❤️ {component.likes?.length || 0}</span>
                                    </div>
                                </div>
                            </div>
                        </a>
                    {/each}
                </div>
            {:else}
                <div class="text-center py-20 text-gray-500">
                    <p>Coming soon...</p>
                </div>
            {/if}
        </div>
    {:else}
        <div class="text-center py-20">
            <h1 class="text-2xl font-bold text-white mb-4">User not found</h1>
            <a href="/" class="text-indigo-400 hover:text-indigo-300">Go Home</a>
        </div>
    {/if}
</div>
