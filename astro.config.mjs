// @ts-check
import { defineConfig } from 'astro/config';

import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  // TODO: update once the production domain is chosen
  site: 'https://punetechcommunity.dev',
  integrations: [sitemap()],
  vite: {
    server: {
      // dev-only: lets tunnels (ngrok, etc.) reach the dev server; free-tier ngrok
      // hostnames change on every restart so a fixed allowlist isn't practical
      allowedHosts: true
    }
  }
});