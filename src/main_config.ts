/// Whether or not tickets are on sale.
export const CONFERENCE_TZ = "Australia/Melbourne"
export const TICKETS_AVAILABLE: boolean = false

export const ROOMS = [
  { slug: "ballroom1", name: "Ballroom 1", days: ['friday', 'saturday', 'sunday'] },
  { slug: "ballroom2", name: "Ballroom 2", days: ['friday', 'saturday', 'sunday'] },
  { slug: "ballroom3", name: "Ballroom 3", days: ['friday', 'saturday', 'sunday'] },
  { slug: "juniorballroom", name: "Junior Ballroom", days: ['monday'] },
] as const
export const SPECIALIST_TRACKS = [
  { slug: "scientific", name: "Scientific Python", room: "ballroom2" },
  { slug: "education", name: "Education", room: "ballroom3" },
  { slug: "data-ai", name: "Data & AI", room: "ballroom1" },

] as const

export const SPONSOR_TIERS = [
  {
    slug: "platinum",
    name: "Platinum Sponsor",
    plural_name: "Platinum Sponsors",
  },
  { slug: "gold", name: "Gold Sponsor", plural_name: "Gold Sponsors" },
  { slug: "standard", name: "Sponsor", plural_name: "Sponsors" },
  { slug: "startup", name: "Startups", plural_name: "Startups @ PyCon AU" },
  { slug: "auspice", name: "Auspice", plural_name: "Auspices" },
] as const

// -----

export type RoomSlug = (typeof ROOMS)[number]["slug"]
export type SponsorTierSlug = (typeof SPONSOR_TIERS)[number]["slug"]
type ExtractSlug<T extends readonly { slug: any }[]> = {
  [I in keyof T]: T[I]["slug"]
}
export const ROOM_SLUGS = ROOMS.map((room) => room.slug) as any as ExtractSlug<
  typeof ROOMS
>
export const ROOMS_BY_SLUG = Object.fromEntries(
  ROOMS.map((room) => [room.slug, room]),
)
export const SPONSOR_TIER_SLUGS = SPONSOR_TIERS.map(
  (tier) => tier.slug,
) as any as ExtractSlug<typeof SPONSOR_TIERS>
export const SPECIALIST_TRACK_SLUGS = SPECIALIST_TRACKS.map(
  (track) => track.slug,
) as any as ExtractSlug<typeof SPECIALIST_TRACKS>
export const ROOM_NAMES: Record<RoomSlug, string> = Object.create(
  ROOMS.map(({ slug, name }) => [slug, name]),
)
