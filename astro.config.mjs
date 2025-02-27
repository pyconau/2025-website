import { defineConfig } from "astro/config"

// https://astro.build/config
import mdx from "@astrojs/mdx"

// https://astro.build/config
export default defineConfig({
  markdown: {
    syntaxHighlight: "prism",
  },
  integrations: [mdx()],
  redirects: {
    // "/pycon-au-2024/schedule": "/program",
  },
})
