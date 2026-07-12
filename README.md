# content-skills

A Claude Code plugin marketplace with one plugin, **content-factory**. It ships
reusable Hebrew short-form content workflows with explicit proof, QA, and
publishing gates.

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
| viral-short-form | `/content-factory:viral-short-form` | Builds objective-led short-form story packets with proof, narrative spine, and one-variable experiments. |
| viral-hooks | `/content-factory:viral-hooks` | Generates and critiques three-layer hook hypotheses without fake algorithm guarantees. |
| viral-captions-and-ctas | `/content-factory:viral-captions-and-ctas` | Audits captions, CTAs, on-screen text, hashtags, and pinned comments against objective and delivery proof. |
| content-performance-review | `/content-factory:content-performance-review` | Reviews Metricool performance at 24 hours and 7 days, then proposes one controlled next experiment. |

## Important: external dependencies

These skills can run as guidance on their own. Full automation still needs the
consumer's content repo, renderer scripts, design files, media host, secrets,
and Metricool connector. The plugin never bundles credentials or assumes a
specific local filesystem.

On a fresh machine the skills load and give full guidance, but the automation
steps that shell out to those scripts or read those design files will not run
until the surrounding repo, secrets, and MCP servers are present. Treat this
plugin as the reusable playbooks; the runtime rig stays in the content repo.

### Placeholders to fill

The skills were genericized for publishing. Substitute these for your own setup:

| Placeholder | Meaning |
|---|---|
| `<content-repo>` | local content working directory |
| `<website-repo>` | the repo that serves your guide pages |
| `<your-domain>` | the domain guide pages are published on |
| `<METRICOOL_BLOG_ID>` | your Metricool brand/blog id |
| `<your-handle>` / `<your-brand>` | your Instagram handles |
| `<CHROME_PROFILE>` | the Chrome profile logged into your IG |
| `<macos-user>` | macOS username, only if your own scripts use Keychain |
| `<host>` | the remote host running the CTA automation |

## License

MIT. See [LICENSE](LICENSE). The `israeli-social-content` skill is distributed
under MIT as noted in its own frontmatter.
