# Content Factory configuration

Copy `config/content-factory.example.json` to `.content-factory.json` in the
consumer project and fill only fields used by that project. Do not store API
keys, passwords, cookies, access tokens, or private media URLs in this file.

Publishing skills must stop before upload or scheduling when required fields
are missing. They must not substitute example values or infer live targets.

Required for publishing:

- `metricool_blog_id`
- `metricool_timezone`
- `publishing_networks`
- `reel_schedule_time`, when automatic scheduling is requested
- explicit current-turn approval

Required for comment-to-DM delivery:

- `website_repo`
- `public_domain`
- `cta_automation_base_url`, HTTPS only outside a local development environment
- explicit consent and anti-duplication controls

Required for public media upload:

- `public_upload_provider`
- `public_uploads_require_approval: true`
- confirmation that source media is approved for public exposure

Project files live under `${CLAUDE_PROJECT_DIR}`. Plugin-bundled scripts and
references live under `${CLAUDE_PLUGIN_ROOT}`. Never assume current working
directory points at either location.

The project workflow fields are optional for draft-only use:

- `pipeline_path`
- `ledger_path`
- `design_system_path`
- `design_lessons_path`
- `music_licenses_path`
- `performance_output_dir`

Read a configured file only after confirming it exists inside the intended
project. If no pipeline or ledger is configured, collect the required state in
the skill's output packet. Do not invent a path or claim a write-back happened.
