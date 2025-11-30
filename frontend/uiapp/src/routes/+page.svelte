<script>
    import { onMount } from 'svelte';
</script>

<div class="relative overflow-hidden">
    <!-- Hero Section -->
    <div class="container mx-auto px-4 py-24 md:py-32 relative z-10">
        <div class="text-center max-w-4xl mx-auto">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 text-sm font-medium mb-6">
                <span class="relative flex h-2 w-2">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
                </span>
                v1.0 is now live
            </div>
            
            <h1 class="text-5xl md:text-7xl font-bold tracking-tight text-gray-900 dark:text-white mb-8">
                Build beautiful UIs <br />
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 to-purple-600">at lightspeed</span>
            </h1>
            
            <p class="text-xl text-gray-600 dark:text-gray-300 mb-10 max-w-2xl mx-auto">
                The ultimate component library for modern web apps. 
                Browse thousands of animated components, customize them in real-time, or generate new ones with AI.
            </p>
            
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
                <a href="/components" class="px-8 py-4 text-lg font-medium text-white bg-indigo-600 rounded-xl hover:bg-indigo-700 transition-all hover:scale-105 shadow-lg shadow-indigo-500/25">
                    Browse Components
                </a>
                <a href="/generate" class="px-8 py-4 text-lg font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-700 transition-all hover:scale-105">
                    Try AI Generator
                </a>
            </div>
        </div>
    </div>

    <!-- Background Elements -->
    <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full max-w-7xl pointer-events-none z-0">
        <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl mix-blend-multiply dark:mix-blend-screen animate-blob"></div>
        <div class="absolute top-1/3 right-1/4 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl mix-blend-multiply dark:mix-blend-screen animate-blob animation-delay-2000"></div>
        <div class="absolute bottom-1/4 left-1/3 w-96 h-96 bg-pink-500/20 rounded-full blur-3xl mix-blend-multiply dark:mix-blend-screen animate-blob animation-delay-4000"></div>
    </div>
</div>

<!-- Features Grid -->
<div class="container mx-auto px-4 py-24">
    <div class="grid md:grid-cols-3 gap-8">
        <div class="p-8 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-indigo-500 transition-colors group">
            <div class="w-12 h-12 bg-indigo-100 dark:bg-indigo-900/50 rounded-xl flex items-center justify-center text-indigo-600 dark:text-indigo-400 mb-6 group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">Component Library</h3>
            <p class="text-gray-600 dark:text-gray-400">
                Access thousands of production-ready components. Copy and paste directly into your project.
            </p>
        </div>

        <div class="p-8 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-purple-500 transition-colors group">
            <div class="w-12 h-12 bg-purple-100 dark:bg-purple-900/50 rounded-xl flex items-center justify-center text-purple-600 dark:text-purple-400 mb-6 group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">AI Generation</h3>
            <p class="text-gray-600 dark:text-gray-400">
                Describe what you need and let our advanced AI generate the perfect component code for you.
            </p>
        </div>

        <div class="p-8 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-pink-500 transition-colors group">
            <div class="w-12 h-12 bg-pink-100 dark:bg-pink-900/50 rounded-xl flex items-center justify-center text-pink-600 dark:text-pink-400 mb-6 group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">Marketplace</h3>
            <p class="text-gray-600 dark:text-gray-400">
                Buy and sell premium components. Support creators and get access to exclusive designs.
            </p>
        </div>
    </div>
</div>

<style>
    @keyframes blob {
        0% { transform: translate(0px, 0px) scale(1); }
        33% { transform: translate(30px, -50px) scale(1.1); }
        66% { transform: translate(-20px, 20px) scale(0.9); }
        100% { transform: translate(0px, 0px) scale(1); }
    }
    .animate-blob {
        animation: blob 7s infinite;
    }
    .animation-delay-2000 {
        animation-delay: 2s;
    }
    .animation-delay-4000 {
        animation-delay: 4s;
    }
</style>
