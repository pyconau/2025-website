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
const sessions = defineCollection({
  schema: z.object({
    title: z.string(),
    abstract: z.string(),
    description: z.string(),
    code: z.string(),
    speakers: z.array(z.string()),
    cw: z.string().nullable(),
    youtube_slug: z.string().nullable(),
  }),
  type: "data",
})
const people = defineCollection({
  schema: z.object({
    name: z.string(),
    pronouns: z.string().nullable(),
    bio: z.string(),
    has_pic: z.boolean(),
    twitter: z.string().nullable().optional(),
    fedi: z.string().nullable().optional(),
  }),
  type: "data",
})

export const collections = {
  sponsors,
  pages,
  sessions,
  people,
}
