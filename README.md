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
| carousel | `/content-factory:carousel` | Hebrew carousel copy, visual blueprint, rights checks, pixel QA, and scheduling proof. |
| carousel-with-face | `/content-factory:carousel-with-face` | Instagram carousel featuring your own face on slides via img2img. |
| carousel-guide | `/content-factory:carousel-guide` | Builds and verifies a named resource, request-scoped keyword route, and delivery proof before scheduling. |
| reel | `/content-factory:reel` | Legacy routing alias for the full Hebrew-captioned talking-head Reel workflow. |
| hebrew-captioned-video-reels | `/content-factory:hebrew-captioned-video-reels` | Produces transcript-faithful Hebrew talking-head videos, verifies media and rights, then optionally schedules to configured networks. |
| israeli-social-content | `/content-factory:israeli-social-content` | Localizes approved copy for Israeli audiences with spoken Hebrew, RTL, calendar, and policy checks. |
| viral-short-form | `/content-factory:viral-short-form` | Builds objective-led short-form story packets with proof, narrative spine, and one-variable experiments. |
| viral-hooks | `/content-factory:viral-hooks` | Generates and critiques three-layer hook hypotheses without fake algorithm guarantees. |
| viral-captions-and-ctas | `/content-factory:viral-captions-and-ctas` | Audits captions, CTAs, on-screen text, hashtags, and pinned comments against objective and delivery proof. |
| content-performance-review | `/content-factory:content-performance-review` | Reviews Metricool performance at 24 hours and 7 days, then proposes one controlled next experiment. |

## Important: external dependencies

These skills can run as guidance on their own. Full automation still needs the
consumer's content repo, renderer, design files, media host, authenticated
connectors, and platform accounts. The plugin never bundles credentials.

On a fresh machine the skills load and give full guidance, but the automation
steps that shell out to those scripts or read those design files will not run
until the surrounding repo, secrets, and MCP servers are present. Treat this
plugin as the reusable playbooks; the runtime rig stays in the content repo.

### Configure before publishing

Copy `plugins/content-factory/config/content-factory.example.json` to
`.content-factory.json` in your content project. Fill publishing targets. Never
put secrets in this file. Missing target means upload or scheduling must stop.

Important configuration fields:

| Field | Meaning |
|---|---|
| `content_repo` | local content working directory |
| `pipeline_path` / `ledger_path` | optional project workflow and history files |
| `design_system_path` / `design_lessons_path` | optional brand and production rules |
| `website_repo` / `public_domain` | resource hosting project and public domain |
| `cta_automation_base_url` | HTTPS health API base URL for request-scoped delivery |
| `metricool_blog_id` / `metricool_timezone` | live publishing target and timezone |
| `publishing_networks` | networks approved for this project |
| `timeline_path` / `performance_output_dir` | optional durable write-back locations |

## License

MIT. See [LICENSE](LICENSE). Modified third-party material and preserved license
notices are listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
