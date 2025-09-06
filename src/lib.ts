import { ContentEntryType } from "astro"
import type { CollectionEntry } from "astro:content"
import { DateTime } from "luxon"

type Nested<T> = T & { children: Nested<T>[] }
export function nestHeadings<T extends { depth: number }>(
  headings: T[],
): Nested<T>[] {
  if (!headings[0]) return []
  const topDepth = headings[0].depth
  const result: Nested<T>[] = []
  for (const heading of headings) {
    let adjustedDepth = heading.depth - topDepth
    //console.log(heading, adjustedDepth)
    let childList = result
    while (adjustedDepth > 0) {
      childList = childList[childList.length - 1]!.children
      adjustedDepth--
    }
    childList.push({ ...heading, children: [] })
  }

  // if there is only one top-level heading, exclude it from the nav
  // and make all of its children top-level instead
  if (result.length === 1) {
    return result[0]!.children
  }
  return result
}

export function nestedMap<T, U, F extends (datum: T, children: U[]) => U>(
  data: Nested<T>[],
  func: F,
): U[] {
  return data.map((datum) => func(datum, nestedMap(datum.children, func)))
}

export type ScheduledSession = CollectionEntry<"sessions"> & {
  data: {
    start: Exclude<CollectionEntry<"sessions">["data"]["start"], null>
    end: Exclude<CollectionEntry<"sessions">["data"]["end"], null>
    room: Exclude<CollectionEntry<"sessions">["data"]["room"], null>
  }
}

export function isScheduled(
  session: CollectionEntry<"sessions">,
): session is ScheduledSession {
  return !!session.data.start && !!session.data.end && !!session.data.room
}

export function* timeSlices(
  start: DateTime,
  end: DateTime,
  duration: Duration,
) {
  let value = start
  while (value <= end) {
    yield value
    value = value.plus(duration)
  }
}

type ExtractCollectionTypes<T> = T extends CollectionEntry<infer U> ? U : never
type CollectionTypes = ExtractCollectionTypes<CollectionEntry<"sessions">>

export type LuxonifiedCollectionEntry<C extends CollectionTypes> = Omit<
  CollectionEntry<C>,
  "data"
> & {
  data: {
    [K in keyof CollectionEntry<C>["data"]]: CollectionEntry<C>["data"][K] extends Date | null
      ? DateTime | null
      : CollectionEntry<C>["data"][K] extends Date
        ? DateTime
        : CollectionEntry<C>["data"][K]
  }
}

export type LuxonifiedScheduledSession =
  LuxonifiedCollectionEntry<"sessions"> & {
    data: {
      start: Exclude<
        LuxonifiedCollectionEntry<"sessions">["data"]["start"],
        null
      >
      end: Exclude<LuxonifiedCollectionEntry<"sessions">["data"]["end"], null>
      room: Exclude<LuxonifiedCollectionEntry<"sessions">["data"]["room"], null>
      plenary: boolean
    }
  }
