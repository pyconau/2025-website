import { getCollection, CollectionEntry } from "astro:content"
import { SPONSOR_TIERS, SponsorTierSlug } from "./main_config"

type SponsorsByTier = {
  tier: SponsorTierSlug
  sponsors: CollectionEntry<"sponsors">[]
}[]

const data: SponsorsByTier = SPONSOR_TIERS.map((tier) => ({
  tier: tier.slug,
  sponsors: [],
}))
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
