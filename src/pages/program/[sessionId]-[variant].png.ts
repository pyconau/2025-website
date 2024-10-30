import { getCollection, getEntry } from "astro:content"
import { mkdtemp, open } from "node:fs/promises"
import { join } from "node:path"
import { tmpdir } from "node:os"
import { execa } from "execa"
import { DateTime } from "luxon"
import { CONFERENCE_TZ, ROOMS_BY_SLUG } from "../../main_config"

type Params = {
  sessionId: string
  variant: "og" | "social"
}

export async function GET({
  params,
  request,
}: {
  params: Params
  request: Request
}) {
  let session = (await getEntry("sessions", params.sessionId))!
  let speakers = await Promise.all(
    session?.data.speakers.map(async (speakerId) => {
      let speaker = (await getEntry("people", speakerId))!
      return {
        name: speaker.data.name,
        image: speaker.data.has_pic
          ? `../../public/people/${speaker.id}.jpg`
          : "",
      }
    }),
  )
  let inputData = {
    title: session.data.title,
    speakers,
    room: ROOMS_BY_SLUG[session.data.room!]?.name,
    time: DateTime.fromJSDate(session.data.start!, {
      zone: CONFERENCE_TZ,
    }).toLocaleString({
      weekday: "long",
      hour: "numeric",
      minute: "numeric",
    }),
    showPhotos: speakers.every((speaker) => !!speaker.image),
  }
  let dir = await mkdtemp(join(tmpdir(), "pyconau-2023-typst-"))
  let inputPath = join(dir, "input.typ")
  let inputFile = await open(inputPath, "wx")
  let typstFile = (
    { og: "speakerCard.typ", social: "socialCard.typ" } as const
  )[params.variant]
  await inputFile.close()
  const { stdout } = await execa({
    encoding: "buffer",
  })`typst compile src/typst/${typstFile} - -f png --font-path src/typst/fonts/ --input data=${JSON.stringify(inputData)} --root ../..`
  let nonResizableArrayBuffer = new ArrayBuffer(stdout.byteLength)
  let nonResizableArrayBufferView = new Uint8Array(nonResizableArrayBuffer)
  nonResizableArrayBufferView.set(stdout)
  return new Response(nonResizableArrayBuffer)
}

export async function getStaticPaths(): Promise<{ params: Params }[]> {
  const pages = await getCollection("sessions")
  return pages.filter((entry) => entry.data.speakers.length > 0).flatMap((entry) =>
    ["og", "social"].map((variant) => ({
      params: {
        sessionId: entry.id,
        variant,
      },
    })),
  )
}
