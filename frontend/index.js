import { DateTime, LocalZone, Settings } from "luxon"
import backstage from "./backstage"
import program from "./program"

Settings.defaultLocale = "en-AU"

const FORMATTER_DIFF_DAY = Intl.DateTimeFormat("en-au", {
  weekday: "short",
  hour: "numeric",
  minute: "numeric",
  timeZoneName: "short",
})

const FORMATTER_SAME_DAY = Intl.DateTimeFormat("en-au", {
  hour: "numeric",
  minute: "numeric",
  timeZoneName: "short",
})

function onload() {
  backstage()
  const programEl = document.querySelector("s-schedule")
  if (programEl) program(programEl)
  document.querySelectorAll("time").forEach((t) => {
    const date = DateTime.fromISO(t.dateTime, { setZone: true })
    const localDate = date.toLocal()
    // If the given date is already in the user's TZ, skip it
    console.log(date.toISO())
    if (date.offset === localDate.offset) return
    const formatted = localDate.toLocaleString({
      weekday: date.weekday === localDate.weekday ? undefined : "short",
      hour: "numeric",
      minute: localDate.minute === 0 ? undefined : "numeric",
      timeZoneName: "short",
    })
    const txt = document.createTextNode(` (${formatted})`)
    t.appendChild(txt)
  })
}

;/^(complete|interactive|loaded)$/.test(document.readyState)
  ? onload()
  : document.addEventListener("DOMContentLoaded", onload, { once: true })
