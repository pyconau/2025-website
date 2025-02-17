#let data = json.decode(sys.inputs.data)

// we want to produce a 1200 by 630 image, but typst is designed for print
// so we generate it at 600pt by 315pt, and produce images at 144dpi
// effectively making 1pt in this document morally equivalent to 1dp

#set page(width: 600pt, height: 600pt, background: place(top, image("social-card-background.png")), margin: 0pt)
#set text(font: "Catamaran")
#set par(spacing: 10pt)

/*
#let data = json.decode(`
{
  "title": "Failsafes and Safety Fails: How to crash a train and other lessons for software engineers",
  "speakers": [
    {"name": "Jack Skinner", "image": "PB9BKD.jpg"},
    {"name": "Jack Skinner", "image": "PB9BKD.jpg"}
  ],
  "room": "Goldfields Theatre",
  "time": "Sunday 12pm"
}
`.text)
*/

#let wattleLeaf = rgb(0, 191, 111)

#let fillSpace(contentFunc, startSize: 40pt) = layout(containerSize => {
  let size = startSize
  while size > 0pt {
      let content = contentFunc(size)
      let (height,) = measure(
        block(width: containerSize.width, content),
      )
      if (height <= containerSize.height) {
        content
        break
      }      
      size = size - 0.25pt
    }
})

#let compressHorizontally(content) = layout(containerSize => {
  let (width,) = measure(content)
  if width < containerSize.width {
    content
  } else {
    scale(x: (containerSize.width / width) * 100%, reflow: true, content)
  }
})

#place(bottom, rect(width: 100%, height: 80pt, fill: wattleLeaf))

#block(height: 100%)[
#grid(
  columns: if data.showPhotos {(1fr, 200pt)} else {(1fr)},
  rows: (75pt, 1fr, 100pt, 80pt),
  //stroke: black,
  grid.cell(x: 0, y: 1, colspan: if data.showPhotos {2} else {1}, align: horizon, fillSpace(baseSize => {
    block(
      inset: 24pt,
      {
        par(spacing: 1em, text(size: baseSize * 0.6, weight: 400)[Join me at PyCon AU 2025 for])
        text(size: baseSize, font: "Catamaran", weight: 700)[#data.title]
        par(spacing: 1em, text(size: baseSize * 0.6, weight: 400)[PyCon AU will be returning to Melbourne in 2025 - details to be announced soon!])
      }
    )
  })),
  grid.cell(x: 0, y: 2, align: horizon, {
    block(
      inset: 24pt,
      {
        par(spacing: 1em, text(size: 24pt, weight: 400)[Register today!])
        par(spacing: 1em, text(size: 24pt, weight: 700)[pycon.org.au/attend])
      }
    )
  }),
  grid.cell(x: 0, y: 3, align: horizon,
    block(inset: 18pt)[
      #compressHorizontally(
        text(
          size: 24pt,
          weight: 700,
          fill: white,
          if data.speakers.len() > 1 [
            #data.speakers.at(0).name and #data.speakers.at(1).name
          ] else [
            #data.speakers.at(0).name
          ]
        )
      )
      #text(
        size: 18pt,
        weight: 400,
        fill: white,
        [#data.room, #data.time]
      )
    ]
  ),
  if data.showPhotos {
    grid.cell(x: 1, y: 2, rowspan: 2, align: bottom,
      block(inset: 14pt,
        if data.speakers.len() > 1 {
          grid(
            columns: (1fr, 1fr),
            gutter: 0pt,
            move(dy: -10pt,
              box(
                radius: 50%,
                clip: true,
                width: 1fr,
                image(data.speakers.at(0).image, width: 86pt, height: 86pt)
              )
            ),
            move(dy: -50pt,
              box(
                radius: 50%,
                clip: true,
                width: 1fr,
                image(data.speakers.at(1).image, width: 86pt, height: 86pt)
              )
            )
          )
        } else {
          box(
            radius: 50%,
            clip: true,
            width: 100%,
            image(data.speakers.at(0).image, width: 172pt, height: 172pt, fit: "cover")
          )
        }
      )
    )
  }
)]