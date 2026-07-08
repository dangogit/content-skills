# content-skills

A Claude Code plugin marketplace with one plugin, **content-factory** - the
Skills behind Daniel Goldman's Hebrew AI/agent personal-brand content pipeline.

## Install

```bash
# in an interactive Claude Code session
/plugin marketplace add dangogit/content-skills
/plugin install content-factory@content-skills
```

Then invoke any skill with the plugin namespace, e.g. `/content-factory:carousel`.

To develop or test locally before publishing:

```bash
claude --plugin-dir ./plugins/content-factory
# after edits:
/reload-plugins
```

## Skills

| Skill | Invoke | What it does |
|---|---|---|
| carousel | `/content-factory:carousel` | Faceless object-centerpiece Instagram carousel (Hebrew), copy + Nano Banana visuals + export. |
| carousel-with-face | `/content-factory:carousel-with-face` | Instagram carousel featuring your own face on slides via img2img. |
| carousel-guide | `/content-factory:carousel-guide` | For comment-for-guide CTAs: builds and verifies the guide page, keyword route, and Instagram CTA automation before scheduling. |
| reel | `/content-factory:reel` | Turns a video clip into a published FB/IG/TikTok/YouTube reel with a burned-in Hebrew hook title. |
| hebrew-captioned-video-reels | `/content-factory:hebrew-captioned-video-reels` | Adds Hebrew IG-style captions to talking-head video, cuts silence, adds a first-5s hook, schedules to Metricool. |
| israeli-social-content | `/content-factory:israeli-social-content` | Social content strategy and Hebrew copy tuned for Israeli audiences across FB/IG/TikTok/LinkedIn. |

## Important: external dependencies

These Skills were authored inside Daniel's private `content` repo. The SKILL.md
instructions reference helper scripts and files that live in that repo, not in
this plugin - for example `scripts/generate-image.mjs`, `scripts/daily-reel/`,
`tools/open-carrusel/`, `design/lessons.md`, `design/DESIGN.md`, and
`content-system/pipeline.md`, plus a `GEMINI_API_KEY_CAROUSEL` Keychain secret
and a Metricool MCP.

On a fresh machine the skills load and give full guidance, but the automation
steps that shell out to those scripts or read those design files will not run
until the surrounding repo, secrets, and MCP servers are present. Treat this
plugin as the reusable playbooks; the runtime rig stays in the content repo.

### Placeholders to fill

The skills were genericized for publishing. Substitute these for your own setup:

| Placeholder | Meaning |
|---|---|
| `<content-repo>` | your local content working directory |
| `<website-repo>` | the repo that serves your guide pages |
| `<your-domain>` | the domain guide pages are published on |
| `<METRICOOL_BLOG_ID>` | your Metricool brand/blog id |
| `<your-handle>` / `<your-brand>` | your Instagram handles |
| `<CHROME_PROFILE>` | the Chrome profile logged into your IG |
| `<macos-user>` | your macOS username (Keychain lookups) |
| `<host>` | the remote host running the CTA automation |

## License

MIT. See [LICENSE](LICENSE). The `israeli-social-content` skill is distributed
under MIT as noted in its own frontmatter.
