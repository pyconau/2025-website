/// Whether or not tickets are on sale.
export const CONFERENCE_TZ = "Australia/Melbourne"
export const TICKETS_AVAILABLE: boolean = false

export const ROOMS = [
  { slug: "goldfields", name: "Goldfields Theatre" },
  { slug: "eureka2", name: "Eureka 2" },
  { slug: "eureka3", name: "Eureka 3" },
] as const
export const SPECIALIST_TRACKS = [
  { slug: "scientific", name: "Scientific Python", room: "eureka2" },
  { slug: "devoops", name: "DevOops", room: "goldfields" },
  { slug: "education", name: "Education", room: "eureka3" },
] as const

// -----

export type RoomSlug = (typeof ROOMS)[number]["slug"]
type ExtractSlug<T extends readonly { slug: any }[]> = {
  [I in keyof T]: T[I]["slug"]
}
export const ROOM_SLUGS = ROOMS.map((room) => room.slug) as any as ExtractSlug<
  typeof ROOMS
>
export const SPECIALIST_TRACK_SLUGS = SPECIALIST_TRACKS.map(
  (track) => track.slug,
) as any as ExtractSlug<typeof SPECIALIST_TRACKS>
export const ROOM_NAMES: Record<RoomSlug, string> = Object.create(
  ROOMS.map(({ slug, name }) => [slug, name]),
)
