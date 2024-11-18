# PyCon AU 2024 website

This website is built with [Astro](https://astro.build).

Yes, we're fully aware of the irony of building the website for a Python conference with JavaScript tooling ;) Previous versions of this site were built with [Statik](https://getstatik.com), and Astro is very similar in spirit while being more actively maintained.

## Installing and running

This website depends on Typst; check out their [install instructions](https://github.com/typst/typst?tab=readme-ov-file#installation) for that.

You'll need to install Node.js (which you can usually get from your friendly local system package manager) and [PNPM](https://pnpm.io/installation). Then, run:

```shell
pnpm install
pnpm start
```

## Dynamically updated data

While this repo is the source of truth for _most_ content on the website, talk data and speaker bios are synced from Pretalx.

This is done by a script that loads data using the Pretalx API and commits it to this repo. This lets us ensure that remote services don't block us from being able to rebuild the website, and also makes it easier to archive the website once the conference is over.

## Repository structure

- `scripts`
  - `schedule_sync.py`: This is the script that handles syncing data from Pretalx.
- `src`
  - `content`: Astro [content collections](https://docs.astro.build/en/guides/content-collections/) root.
    - `pages`: **Most static prose content is in here.** The structure of this directory mirrors the website's URL structure.
    - `people`, `sessions`: These directories are auto-populated by the Pretalx sync script. Manual changes made here may be overwritten.
    - `sponsors`: Sponsor data is in here. This populates the website footer and the `/sponsor/` page.
    - `tracks`: Prose about specialist tracks is in here.
  - `pages`: This is the root of Astro's file-based routing. The structure of this directory mirrors the website's URL structure.
    - `index.astro`: This is the home page. Its content is directly written in HTML in the template; it's not pulled from anywhere else.
    - `[...slug].astro`: This is the route that generates the actual HTML for the files in `src/content/pages/`.
  - `components`
    - `Navigation.astro`: Top-of-page navigation.
  - `layouts`
    - `Base.astro`: Base layout used for every page.
    - `Page.astro`: Layout used for most pages with prose content on them.
