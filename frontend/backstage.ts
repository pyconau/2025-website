import { DateTime } from "luxon"

const backstageBar = document.createElement("template")
backstageBar.innerHTML = `
<div class="backstage-bar">
  <span class='time'></span>
</div>
`

const reltimeSpan = document.createElement("template")
reltimeSpan.innerHTML = `
<span>
  <span class='reltime-fixed'></span>&mdash;<b><span class='reltime-relative'></span></b>
</span>
`

const TIME_COMPACT = {
  weekday: "short",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
  timeZoneName: "short",
  hour12: false,
}
const TIME_COMPACT_ADL = { ...TIME_COMPACT, timeZone: "Australia/Adelaide" }
const TIME_HRMIN = {
  hour: "2-digit",
  minute: "2-digit",
  timeZoneName: "short",
  hour12: false,
}
const TIME_HRMIN_ADL = { ...TIME_HRMIN, timeZone: "Australia/Adelaide" }

function clockTick(output: HTMLElement) {
  const now = DateTime.local()
  output.innerText = now
    .setZone("Australia/Adelaide")
    .toLocaleString(TIME_COMPACT_ADL)
  setTimeout(clockTick.bind(null, output), 1000 - (now.toMillis() % 1000))
}

export default function () {
  let qs = new URLSearchParams(document.location.search)
  if (qs.get("backstage") === "true") {
    localStorage.setItem("backstage", "true")
  } else if (qs.get("backstage") === "false") {
    localStorage.removeItem("backstage")
  }

  if (
    localStorage.getItem("backstage") !== null ||
    qs.get("speaker") === "true"
  ) {
    document.body.classList.add("backstage")

    // add backstage bar
    const bar = backstageBar.content.firstElementChild!.cloneNode(
      true,
    ) as HTMLElement
    document.body.appendChild(bar)
    const time = bar.querySelector(".time") as HTMLElement
    console.log(bar, time)
    clockTick(time)

    // handle any reltime tags
    ;(document.querySelectorAll("[data-reltime]") as NodeListOf<
      HTMLElement
    >).forEach((el) => {
      const dt = DateTime.fromISO(el.dataset.reltime!)
      console.log(el, dt)
      const rtt = reltimeSpan.content.firstElementChild!.cloneNode(
        true,
      ) as HTMLElement
      rtt.querySelector(".reltime-fixed")!.innerHTML = `${dt.toLocaleString(
        TIME_HRMIN_ADL,
      )} (${dt.toLocaleString(TIME_HRMIN)})`
      const relative = rtt.querySelector(".reltime-relative")
      setInterval(() => {
        relative!.innerHTML = dt.toRelative() || ""
      }, 1000)
      el.textContent = ""
      el.appendChild(rtt)
    })
  }
}
