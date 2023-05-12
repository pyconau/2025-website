import { z, defineCollection } from "astro:content"

const sponsors = defineCollection({
  schema: z.object({
    name: z.string(),
    logo: z.string(),
    url: z.string(),
    tier: z.string(),
  }),
})
const pages = defineCollection({ schema: z.object({ title: z.string() }) })

export const collections = {
  sponsors,
  pages,
}
