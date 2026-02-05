<script lang="ts">
    import { page } from '$app/stores';
    import { onMount, onDestroy } from 'svelte';
    import { api } from '$lib/api';
    import { ws } from '$lib/stores/websocket';
    import { auth } from '$lib/stores/auth';
    import type { Component } from '$lib/types';
    import MonacoEditor from '$lib/components/editor/MonacoEditor.svelte';

    let component: Component | null = null;
    let loading = true;
    let activeTab = 'html';
    let code = '';
    let debounceTimer: any;
    let previewUrl = '';
    
    // Social State
    let isLiked = false;
    let likeCount = 0;
    let comments: any[] = [];
    let newComment = '';
    let submittingComment = false;

    $: slug = $page.params.slug;

    onMount(async () => {
        try {
            // Fetch Component
            component = await api.get<Component>(`/components/${slug}/`);
            if (component) {
                if (component.code_content) {
                    code = component.code_content[activeTab] || '';
                    updatePreview(component.code_content);
                } else if (component.preview_url) {
                    previewUrl = component.preview_url;
                }
                
                // Initialize Like State
                likeCount = component.likes?.length || 0;
                if ($auth.user) {
                    isLiked = component.likes?.some((l: any) => l.user === $auth.user?.id) || false;
                }

                // Fetch Comments
                fetchComments();
            }
            
            ws.connect(slug);
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    });

    async function fetchComments() {
        if (!component) return;
        try {
            const res = await api.get<any[]>(`/comments/?component_id=${component.id}`);
            comments = res;
        } catch (e) {
            console.error('Failed to fetch comments', e);
        }
    }

    async function toggleLike() {
        if (!$auth.user) return alert('Please login to like components');
        if (!component) return;

        // Optimistic UI update
        isLiked = !isLiked;
        likeCount += isLiked ? 1 : -1;

        try {
            await api.post('/likes/toggle/', { component_id: component.id });
        } catch (e) {
            // Revert on error
            isLiked = !isLiked;
            likeCount += isLiked ? 1 : -1;
            console.error('Like failed', e);
        }
    }

    async function postComment() {
        if (!$auth.user) return alert('Please login to comment');
        if (!newComment.trim() || !component) return;

        submittingComment = true;
        try {
            const comment = await api.post('/comments/', { 
                component: component.id, 
                text: newComment 
            });
            comments = [comment, ...comments];
            newComment = '';
        } catch (e) {
            console.error('Comment failed', e);
        } finally {
            submittingComment = false;
        }
    }

    function handleRemix() {
        if (!component || !component.code_content) return;
        
        localStorage.setItem('draft_component', JSON.stringify({
            title: `Remix of ${component.title}`,
            description: `Remixed from @${component.creator.username}`,
            code_content: component.code_content
        }));
        window.location.href = '/upload?draft=true';
    }

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
                <style>
                    body { margin: 0; padding: 20px; min-height: 100vh; display: flex; align-items: center; justify-content: center; background: transparent; }
                    ${css || ''}
                </style>
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
        if (component && component.code_content) {
             component.code_content[activeTab] = newCode;
        }
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            if (component && component.code_content) {
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
    <div class="flex h-[calc(100vh-64px)] overflow-hidden">
        <!-- Sidebar / Info -->
        <div class="w-96 border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 flex flex-col z-20 shadow-xl">
            <div class="p-6 overflow-y-auto flex-1">
                <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">{component.title}</h1>
                
                <div class="flex items-center justify-between mb-6">
                    <a href="/u/{component.creator.username}" class="flex items-center gap-2 group">
                        <img src={component.creator.avatar || `https://ui-avatars.com/api/?name=${component.creator.username}&background=random`} alt={component.creator.username} class="w-8 h-8 rounded-full border border-gray-700 group-hover:border-indigo-500 transition-colors" />
                        <span class="text-sm font-medium text-gray-600 dark:text-gray-300 group-hover:text-indigo-400 transition-colors">@{component.creator.username}</span>
                    </a>
                    <div class="flex items-center gap-2">
                        <button 
                            on:click={toggleLike}
                            class="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium transition-all {isLiked ? 'bg-pink-500/20 text-pink-500' : 'bg-gray-100 dark:bg-gray-800 text-gray-500 hover:bg-gray-200 dark:hover:bg-gray-700'}"
                        >
                            <svg class="w-4 h-4 {isLiked ? 'fill-current' : 'none'}" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
                            {likeCount}
                        </button>
                    </div>
                </div>

                <div class="prose dark:prose-invert prose-sm mb-8 text-gray-400">
                    <p>{component.description}</p>
                </div>

                <div class="flex flex-wrap gap-2 mb-8">
                    {#each component.tags as tag}
                        <span class="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded text-xs text-gray-500 border border-gray-700">
                            #{tag.name}
                        </span>
                    {/each}
                </div>

                <div class="grid grid-cols-2 gap-3 mb-8">
                    <button class="py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-bold transition-colors shadow-lg shadow-indigo-500/20">
                        Download
                    </button>
                    <button 
                        on:click={handleRemix}
                        class="py-2.5 bg-gray-800 hover:bg-gray-700 text-white border border-gray-600 rounded-xl font-bold transition-colors flex items-center justify-center gap-2"
                    >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path></svg>
                        Remix
                    </button>
                </div>

                <!-- Comments Section -->
                <div class="border-t border-gray-800 pt-6">
                    <h3 class="text-sm font-bold text-gray-300 mb-4">Comments ({comments.length})</h3>
                    
                    {#if $auth.user}
                        <div class="flex gap-3 mb-6">
                            <img src={$auth.user.avatar || `https://ui-avatars.com/api/?name=${$auth.user.username}`} class="w-8 h-8 rounded-full" alt="Me" />
                            <div class="flex-1">
                                <textarea 
                                    bind:value={newComment}
                                    placeholder="Add a comment..." 
                                    class="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-sm text-white focus:ring-1 focus:ring-indigo-500 resize-none h-20"
                                ></textarea>
                                <div class="flex justify-end mt-2">
                                    <button 
                                        on:click={postComment}
                                        disabled={submittingComment || !newComment.trim()}
                                        class="px-4 py-1.5 bg-white text-black text-xs font-bold rounded-lg hover:bg-gray-200 disabled:opacity-50"
                                    >
                                        Post
                                    </button>
                                </div>
                            </div>
                        </div>
                    {/if}

                    <div class="space-y-6">
                        {#each comments as comment}
                            <div class="flex gap-3">
                                <a href="/u/{comment.user.username}">
                                    <img src={comment.user.avatar || `https://ui-avatars.com/api/?name=${comment.user.username}`} class="w-8 h-8 rounded-full" alt={comment.user.username} />
                                </a>
                                <div>
                                    <div class="flex items-baseline gap-2">
                                        <a href="/u/{comment.user.username}" class="text-sm font-bold text-gray-300 hover:text-white">{comment.user.username}</a>
                                        <span class="text-xs text-gray-600">{new Date(comment.created_at).toLocaleDateString()}</span>
                                    </div>
                                    <p class="text-sm text-gray-400 mt-1">{comment.text}</p>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="flex-1 flex flex-col min-w-0 bg-[#1e1e1e]">
            <!-- Toolbar -->
            <div class="h-12 border-b border-gray-800 bg-[#1e1e1e] flex items-center px-4 gap-4">
                <div class="flex bg-gray-800 rounded p-1">
                    {#each ['html', 'css', 'js', 'svelte'] as tab}
                        <button 
                            class="px-3 py-1 rounded text-xs font-medium transition-colors {activeTab === tab ? 'bg-gray-600 text-white shadow' : 'text-gray-400 hover:text-gray-200'}"
                            on:click={() => handleTabChange(tab)}
                        >
                            {tab.toUpperCase()}
                        </button>
                    {/each}
                </div>
                <div class="ml-auto flex items-center gap-2 text-gray-500">
                    <div class="px-3 py-1 bg-gray-800 rounded text-xs">
                        {component.views} views
                    </div>
                </div>
            </div>

            <!-- Split View -->
            <div class="flex-1 flex min-h-0">
                <!-- Editor -->
                <div class="w-1/2 border-r border-gray-800 flex flex-col">
                    <MonacoEditor 
                        value={code} 
                        language={activeTab === 'js' || activeTab === 'svelte' ? 'javascript' : activeTab}
                        on:change={(e) => handleCodeChange(e.detail)}
                    />
                </div>

                <!-- Preview -->
                <div class="w-1/2 bg-[url('/grid.svg')] bg-center relative flex items-center justify-center overflow-hidden">
                    {#if previewUrl}
                        <iframe 
                            src={previewUrl} 
                            title="Preview"
                            class="w-full h-full border-0"
                        />
                    {:else}
                        <div class="absolute inset-0 flex items-center justify-center text-gray-600">
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
