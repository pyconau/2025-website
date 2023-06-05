import { z, defineCollection } from "astro:content"

const sponsors = defineCollection({
  schema: z.object({
    name: z.string(),
    logo: z.string(),
    url: z.string(),
    tier: z.string(),
  }),
})
const pages = defineCollection({
  schema: z.object({ title: z.string(), order: z.number().optional() }),
})

export const collections = {
  sponsors,
  pages,
}
