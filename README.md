You are an expert full-stack engineer. Build a complete production-ready web application called **Animate stack** — a developer-focused platform that provides ready-to-use animated UI components, templates, and an AI component generator.

Follow ALL requirements below.

=================================================
PROJECT GOAL
=================================================
Build a professional web app that developers can use to:
- browse animated components
- preview animations
- customize components
- copy/export code for multiple frameworks
- generate components using AI
- download templates
- purchase/upload components in a marketplace

=================================================
STACK CHOICE
=================================================
Use the following stack:

Frontend:
- Svelte
- Tailwind CSS
- TypeScript
- Three.js (for 3D previews)
- Monaco Editor (code editor)
- Local storage + JWT auth handling

Backend:
- Django
- Django REST Framework
- sqlite
- Django Channels (for real-time live preview sync)
- Celery + Redis (for background AI jobs)
- OpenAI / local AI model integration


=================================================
CORE FEATURES TO BUILD
=================================================
1. Component Library
   - 3D components
   - Animation components
   - Text animations
   - Fully animated UI blocks
   - Pro-level cards, forms, dashboards
   - Background gradients & animated backgrounds
   - Light/dark variants
   - Built-in + custom animations

2. Previews & Editing
   - Live preview window
   - Multi-breakpoint (mobile/tablet/desktop)
   - Code editor (Monaco)
   - One-click "Copy Code"
   - Framework toggle (HTML, CSS, JS, React, Next, Vue, Svelte, Tailwind, Django)

3. Customization System
   - Custom animation builder
   - Text animation editor
   - Easing editor
   - Timeline editor
   - Color, size, depth, shadows
   - Save presets

4. Template Library
   - Landing pages
   - SaaS dashboards
   - Portfolio layouts
   - Ecommerce sections
   - Multi-step forms

5. Asset Library
   - 3D models (gltf)
   - SVG icons
   - Lottie animations
   - Animated backgrounds
   - Gradient packs

6. AI Features
   - AI Component Generator (input → preview + code)
   - AI Animation Generator
   - AI Template Creator
   - AI Motion Optimizer (performance-friendly animations)

7. Marketplace
   - Users can upload/sell components
   - Creator dashboard
   - Earnings, analytics, payouts
   - Ratings + reviews

8. User System
   - JWT auth
   - Saved components
   - Favorites
   - Custom presets
   - Team collaboration (invite + roles)
   - Private libraries

9. NPM Package
   - @motionforge/components
   - Allow importing any component programmatically
   - Tree-shakeable + theme override friendly

10. Admin Dashboard
    - Manage users
    - Manage components, templates, assets
    - Approve marketplace uploads
    - Analytics (usage, searches, downloads)

=================================================
WHAT YOU MUST OUTPUT
=================================================
When generating code or planning, output the following:

1) Full folder structure for:
   - SvelteKit frontend
   - Django backend
   - Shared utilities
   - Infrastructure config files

2) Database schema (PostgreSQL models)
   - Components
   - Templates
   - Assets
   - Marketplace items
   - Users
   - AI tasks
   - Teams

3) API design (Django REST)
   - Auth APIs
   - Component APIs
   - Template APIs
   - Marketplace APIs
   - Asset APIs
   - AI generation APIs

4) SvelteKit pages and layout architecture
   - routes
   - components
   - stores
   - API clients
   - theme system

5) Complete UI/UX flow
   - Dashboard
   - Component viewer
   - AI generator page
   - Marketplace
   - Template browser
   - Profile
   - Admin panel

6) System Architecture Diagram (ASCII allowed)

7) Deployment guide
   - Vercel (frontend)
   - Fly/Railway (backend)
   - S3/R2 (storage)
   - PostgreSQL + Redis setup

8) NPM package structure + example usage

9) Security + performance checklist

10) A roadmap:
    - MVP
    - v1.0
    - Pro version
    - Enterprise features

=================================================
IMPORTANT RULES
=================================================
- Generate clean, production-ready code.
- Use DRY principles.
- Use reusable animations + Svelte actions.
- Keep Tailwind config modular (extendable).
- All components must support dark/light mode.
- AI outputs must always return multi-framework code.
- Use comments in code where needed.
- Avoid filler text — generate real implementation.
- Do not skip any major feature.
- Produce scalable architecture.

=================================================
START NOW.
frontend and backend are setup
