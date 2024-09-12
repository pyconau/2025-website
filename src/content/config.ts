import { z, defineCollection } from "astro:content"
import { ROOM_SLUGS, SPECIALIST_TRACK_SLUGS } from "../main_config"

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
const tracks = defineCollection({
  schema: z.object({ name: z.string() }),
})
const sessions = defineCollection({
  schema: z.object({
    title: z.string(),
    abstract: z.string(),
    description: z.string(),
    track: z.enum(SPECIALIST_TRACK_SLUGS).nullable(),
    code: z.string(),
    speakers: z.array(z.string()),
    cw: z.string().nullable(),
    youtube_slug: z.string().nullable().optional().default(null),
    start: z.date().nullable(),
    end: z.date().nullable(),
    room: z.enum(ROOM_SLUGS).nullable(),
    type: z
      .enum(["talk", "stall", "open-close", "special", "keynote"])
      .optional()
      .default("talk"),
    online: z.boolean(),
  }),
  type: "data",
})
const breaks = defineCollection({
  schema: z.object({
    room: z.enum(ROOM_SLUGS),
    start: z.date(),
    end: z.date(),
    description: z.string(),
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
  tracks,
  sessions,
  breaks,
  people,
}
