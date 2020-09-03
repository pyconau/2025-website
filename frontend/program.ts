import { DateTime, LocalZone, DateTimeFormatOptions } from "luxon"

const ZONE = "Australia/Adelaide"
const TIME_ONLY: DateTimeFormatOptions = {
  hour: "numeric",
  minute: "numeric",
}
const TIME_ONLY_DIFF_DAY = { ...TIME_ONLY, weekday: "short" }
const TIME_ONLY_TZ = { ...TIME_ONLY, timeZoneName: "short" }
const TIME_ONLY_ACST = { ...TIME_ONLY, timeZone: "Australia/Adelaide" }

const HOUR_MARKER = { hour: "numeric" }
const HOUR_MARKER_DIFF_DAY = { ...HOUR_MARKER, weekday: "short" }

export default function scheduleInit(schedule: HTMLElement) {
  // Show local times on all time markers
  ;(schedule.querySelectorAll("p.time") as NodeListOf<
    HTMLParagraphElement
  >).forEach((time) => {
    const start = DateTime.fromISO(time.dataset.start!, {
      zone: ZONE,
    })
    const end = DateTime.fromISO(time.dataset.end!, {
      zone: ZONE,
    })
    const startLocal = start.toLocal()
    const startLocalIsDiffDay = startLocal.weekday !== start.weekday
    time.innerText = `${start.toLocaleString(
      TIME_ONLY_ACST,
    )}\u2013${end.toLocaleString(TIME_ONLY_ACST)} (${startLocal.toLocaleString(
      startLocalIsDiffDay ? TIME_ONLY_DIFF_DAY : TIME_ONLY,
    )}\u2013${end.toLocal().toLocaleString(TIME_ONLY_TZ)})`
    console.log(start, end)
  })

  //Update hour markers for local TZ
  schedule
    .querySelectorAll("s-time, s-time-rule")
    .forEach((x) => x.parentElement?.removeChild(x))
  const eventStart = DateTime.fromISO(schedule.dataset.start!, { zone: ZONE })
  const eventEnd = DateTime.fromISO(schedule.dataset.end!, { zone: ZONE })
  const rules = new Set<number>()
  let hour = eventStart.startOf("hour")
  while (hour.diff(eventEnd).milliseconds < 0) {
    console.log(hour.toLocaleString(HOUR_MARKER))
    const newTime = document.createElement("s-time")
    newTime.innerText = hour.toLocaleString(HOUR_MARKER)
    const minute = hour.toMillis() / 60_000
    rules.add(minute)
    newTime.style.setProperty("--at", "" + minute)
    schedule.appendChild(newTime)
    hour = hour.plus({ hours: 1 })
  }
  // TODO merge copypaste
  hour = eventStart.toLocal().startOf("hour")
  if (hour.diff(eventStart).milliseconds < 0) hour = hour.plus({ hours: 1 })
  while (hour.diff(eventEnd).milliseconds < 0) {
    console.log(hour.toLocaleString(HOUR_MARKER))
    const newTime = document.createElement("s-time")
    const hourHasDifferentDay = hour.weekday !== hour.setZone(ZONE).weekday
    const label = hour.toLocaleString(
      hourHasDifferentDay ? HOUR_MARKER_DIFF_DAY : HOUR_MARKER,
    )
    console.log(hourHasDifferentDay, label, hour)
    newTime.innerText = label
    const minute = hour.toMillis() / 60_000
    console.log(hour.toMillis(), minute)
    rules.add(minute)
    newTime.classList.add("local")
    newTime.style.setProperty("--at", "" + minute)
    schedule.appendChild(newTime)
    hour = hour.plus({ hours: 1 })
  }
  rules.forEach((rule) => {
    const newRule = document.createElement("s-time-rule")
    newRule.style.setProperty("--at", "" + rule)
    schedule.appendChild(newRule)
  })
  const acstLabel = document.createElement("s-tz-header")
  acstLabel.innerText = "ACST"
  schedule.appendChild(acstLabel)
  const localLabel = document.createElement("s-tz-header")
  localLabel.classList.add("local")
  localLabel.innerText = new LocalZone().offsetName(hour.toMillis(), {
    format: "short",
  })
  schedule.appendChild(localLabel)

  // now marker
  let nowMarker: HTMLElement | undefined
  function updateNow() {
    if (nowMarker && eventEnd.diffNow().milliseconds < 0) {
      schedule.removeChild(nowMarker)
      return
    }
    const nowMillis = Date.now()
    if (!nowMarker) {
      nowMarker = document.createElement("s-now-rule")
      schedule.appendChild(nowMarker)
    }
    nowMarker.style.setProperty("--at", "" + nowMillis / 60_000)
    window.setTimeout(updateNow, 60_000 - (nowMillis % 60_000))
  }
  const timeUntilStart = eventStart.diffNow().milliseconds
  if (timeUntilStart < 0) updateNow()
  else window.setTimeout(updateNow, timeUntilStart)
}
