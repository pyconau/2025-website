import { getCollection, CollectionEntry } from "astro:content"

type SponsorsByTier = {
  tier: "platinum" | "track" | "auspice"
  sponsors: CollectionEntry<"sponsors">[]
}[]

const data: SponsorsByTier = [
  { tier: "platinum", sponsors: [] },
  { tier: "track", sponsors: [] },
  { tier: "auspice", sponsors: [] },
]
let dataIsPopulated = false

export async function getSponsorsByTier(): Promise<SponsorsByTier> {
  if (dataIsPopulated) return data
  const allSponsors = await getCollection("sponsors")
  for (const tierObj of data) {
    tierObj.sponsors = allSponsors.filter(
      (sponsor) => sponsor.data.tier === tierObj.tier,
    )
  }
  dataIsPopulated = true
  return data
}
