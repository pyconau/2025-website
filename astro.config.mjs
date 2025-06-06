// @ts-check
import { defineConfig } from "astro/config"

// https://astro.build/config
import mdx from "@astrojs/mdx"

// https://astro.build/config
export default defineConfig({
  markdown: {
    syntaxHighlight: "prism",
  },
  integrations: [mdx()],
  legacy: {
    // https://docs.astro.build/en/guides/upgrade-to/v5/#legacy-v20-content-collections-api
    collections: true,
  },
  redirects: {
    // "/pycon-au-2024/schedule": "/program",
  },
})
