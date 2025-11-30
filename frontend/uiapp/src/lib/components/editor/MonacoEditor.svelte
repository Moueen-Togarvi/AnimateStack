<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import type * as Monaco from 'monaco-editor/esm/vs/editor/editor.api';

    export let value = '';
    export let language = 'html';
    export let theme = 'vs-dark';
    export let readOnly = false;

    let editorContainer: HTMLElement;
    let editor: Monaco.editor.IStandaloneCodeEditor;
    let monaco: typeof Monaco;

    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();

    $: if (editor && value !== editor.getValue()) {
        editor.setValue(value);
    }

    onMount(async () => {
        console.log('MonacoEditor mounting with value:', value);
        if (typeof window !== 'undefined') {
            try {
                const monacoImport = await import('monaco-editor');
                monaco = monacoImport.default || monacoImport;
                console.log('Monaco loaded', monaco);
                
                if (!editorContainer) {
                    console.error('Editor container not found');
                    return;
                }

                editor = monaco.editor.create(editorContainer, {
                    value,
                    language,
                    theme,
                    readOnly,
                    automaticLayout: true,
                    minimap: { enabled: false },
                    scrollBeyondLastLine: false,
                    fontSize: 14,
                    fontFamily: "'JetBrains Mono', 'Fira Code', Consolas, monospace",
                });
                console.log('Editor created');

                editor.onDidChangeModelContent(() => {
                    value = editor.getValue();
                    dispatch('change', value);
                });
            } catch (e) {
                console.error('Failed to initialize Monaco:', e);
            }
        }
    });
</script>

<div bind:this={editorContainer} class="w-full h-full min-h-[300px] border border-gray-700 rounded-lg overflow-hidden" />
