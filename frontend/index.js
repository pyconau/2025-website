const FORMATTER_DIFF_DAY = Intl.DateTimeFormat(
  'en-au',
  {
    weekday: 'short',
    hour: 'numeric',
    minute: 'numeric',
    timeZoneName: 'short',
  }
)

const FORMATTER_SAME_DAY = Intl.DateTimeFormat(
  'en-au',
  {
    hour: 'numeric',
    minute: 'numeric',
    timeZoneName: 'short',
  }
)

function onload() {
  document.querySelectorAll('time').forEach(t => {  
  // The date constructor will convert to the user's local tz
  const awareDate = new Date(t.dateTime)
  // if we strip out the tz and create a new date, and that date matches,
  // the original date was already local for this user
  const naiveDate = new Date(t.dateTime.replace(/[+-]\d\d:?\d\d$/, ''))
  if (awareDate.getTime() == naiveDate.getTime()) return
  
  const formatter = awareDate.getDay() == naiveDate.getDay() ? FORMATTER_SAME_DAY : FORMATTER_DIFF_DAY
  
  const txt = document.createTextNode(` (${formatter.format(awareDate)})`)
  t.appendChild(txt)
})
}

/^(complete|interactive|loaded)$/.test(document.readyState) ? onload() : document.addEventListener('DOMContentLoaded', onload, {once: true})