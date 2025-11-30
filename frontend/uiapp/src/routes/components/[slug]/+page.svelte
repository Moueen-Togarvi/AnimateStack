<script lang="ts">
    import { page } from '$app/stores';
    import { onMount, onDestroy } from 'svelte';
    import { api } from '$lib/api';
    import { ws } from '$lib/stores/websocket';
    import type { Component } from '$lib/types';
    import MonacoEditor from '$lib/components/editor/MonacoEditor.svelte';

    let component: Component | null = null;
    let loading = true;
    let activeTab = 'html';
    let code = '';
    let debounceTimer: any;

    let previewUrl = '';

    $: slug = $page.params.slug;

    onMount(async () => {
        try {
            component = await api.get<Component>(`/components/${slug}/`);
            if (component && component.code_content) {
                code = component.code_content[activeTab] || '';
                updatePreview(component.code_content);
            } else if (component?.preview_url) {
                previewUrl = component.preview_url;
            }
            
            // Connect to WebSocket
            ws.connect(slug);
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    });

    onDestroy(() => {
        ws.disconnect();
        if (previewUrl) URL.revokeObjectURL(previewUrl);
    });

    // Listen for incoming messages
    $: if ($ws.message && $ws.message.code_content) {
        const newCodeContent = $ws.message.code_content;
        const newCode = newCodeContent[activeTab];
        if (newCode !== code) {
            code = newCode;
        }
        updatePreview(newCodeContent);
    }

    function updatePreview(codeContent: any) {
        if (!codeContent) return;
        
        const { html, css, js } = codeContent;
        const blob = new Blob([`
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <script src="https://cdn.tailwindcss.com"><\/script>
                <style>${css || ''}</style>
            </head>
            <body>
                ${html || ''}
                <script>${js || ''}<\/script>
            </body>
            </html>
        `], { type: 'text/html' });
        
        if (previewUrl) URL.revokeObjectURL(previewUrl);
        previewUrl = URL.createObjectURL(blob);
    }

    function handleCodeChange(newCode: string) {
        code = newCode;
        
        // Update local component state immediately so tab switching preserves changes
        if (component && component.code_content) {
             component.code_content[activeTab] = newCode;
        }

        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            if (component && component.code_content) {
                // Create a fresh copy to ensure reactivity if needed, though direct mutation worked above
                const updatedContent = { ...component.code_content };
                
                updatePreview(updatedContent);
                
                ws.sendMessage({
                    message: 'code_update',
                    code_content: updatedContent
                });
            }
        }, 500);
    }

    function handleTabChange(tab: string) {
        activeTab = tab;
        if (component?.code_content) {
            code = component.code_content[tab] || '';
        }
    }
</script>

{#if loading}
    <div class="flex items-center justify-center min-h-screen">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
    </div>
{:else if component}
    <div class="flex h-[calc(100vh-64px)]">
        <!-- Sidebar / Info -->
        <div class="w-80 border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 p-6 overflow-y-auto">
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">{component.title}</h1>
            <div class="flex items-center gap-2 mb-6">
                <img src={component.creator.avatar || '/default-avatar.png'} alt={component.creator.username} class="w-6 h-6 rounded-full" />
                <span class="text-sm text-gray-600 dark:text-gray-400">by {component.creator.username}</span>
            </div>

            <div class="prose dark:prose-invert mb-8">
                <p>{component.description}</p>
            </div>

            <div class="flex flex-wrap gap-2 mb-8">
                {#each component.tags as tag}
                    <span class="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded text-xs text-gray-600 dark:text-gray-400">
                        #{tag.name}
                    </span>
                {/each}
            </div>

            <button class="w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-medium transition-colors">
                Download / Copy
            </button>
        </div>

        <!-- Main Content -->
        <div class="flex-1 flex flex-col min-w-0">
            <!-- Toolbar -->
            <div class="h-12 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 flex items-center px-4 gap-4">
                <div class="flex bg-gray-100 dark:bg-gray-800 rounded p-1">
                    {#each ['html', 'css', 'js', 'svelte'] as tab}
                        <button 
                            class="px-3 py-1 rounded text-sm font-medium transition-colors {activeTab === tab ? 'bg-white dark:bg-gray-700 shadow text-gray-900 dark:text-white' : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'}"
                            on:click={() => handleTabChange(tab)}
                        >
                            {tab.toUpperCase()}
                        </button>
                    {/each}
                </div>
                <div class="ml-auto flex items-center gap-2">
                    <button class="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded">
                        <span class="sr-only">Desktop</span>
                        🖥️
                    </button>
                    <button class="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded">
                        <span class="sr-only">Mobile</span>
                        📱
                    </button>
                </div>
            </div>

            <!-- Split View -->
            <div class="flex-1 flex min-h-0">
                <!-- Editor -->
                <div class="w-1/2 border-r border-gray-200 dark:border-gray-700">
                    <MonacoEditor 
                        value={code} 
                        language={activeTab === 'js' || activeTab === 'svelte' ? 'javascript' : activeTab}
                        on:change={(e) => handleCodeChange(e.detail)}
                    />
                </div>

                <!-- Preview -->
                <!-- Preview -->
                <div class="w-1/2 bg-gray-50 dark:bg-gray-950 relative">
                    {#if previewUrl}
                        <iframe 
                            src={previewUrl} 
                            title="Preview"
                            class="w-full h-full border-0"
                        />
                    {:else}
                        <div class="absolute inset-0 flex items-center justify-center text-gray-400">
                            Preview not available
                        </div>
                    {/if}
                </div>
            </div>
        </div>
    </div>
{:else}
    <div class="flex items-center justify-center min-h-screen">
        <div class="text-xl text-gray-500">Component not found</div>
    </div>
{/if}
