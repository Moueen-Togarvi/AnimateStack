import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import monacoEditorImport from 'vite-plugin-monaco-editor';

import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import monacoEditorImport from 'vite-plugin-monaco-editor';

// Handle ESM/CJS interop
// @ts-ignore
const monacoEditor = monacoEditorImport.default || monacoEditorImport;

export default defineConfig({
	plugins: [
		tailwindcss(),
		sveltekit(),
		monacoEditor({
			languageWorkers: ['editorWorkerService', 'css', 'html', 'json', 'typescript']
		})
	],
	optimizeDeps: {
		exclude: ['monaco-editor']
	}
});
