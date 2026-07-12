# Instagram Agent Routing

## Keyword Rules

- Use one short uppercase keyword per guide.
- Match whole word when the platform supports it.
- Avoid keyword substrings. `AGENT` collides with `AGENTIC`.
- If platform only supports "contains", choose collision-proof words like `SUBAGENT`, `MEMORY`, `CODEX`, or `STACK`.
- Keep keyword consistent across carousel slide, caption, guide page, and automation.

## Automation Fields

```text
Trigger name: Guide - <KEYWORD>
When: Instagram comment matches whole word <KEYWORD>
Do: send one private DM containing only the requested resource
Public reply: שלחתי לך בפרטי
Collision notes: <none or explanation>
Consent scope: this comment request only
Dedupe key: <comment-id plus route-id>
Rate limit: <configured per-account limit>
```

## DM Text Pattern

```text
הנה המדריך שביקשת:
<guide-url>
```

If multiple keywords appear:

```text
מצאתי כמה מדריכים שביקשת:
- <KEYWORD>: <guide-url>
- <KEYWORD>: <guide-url>
```

If keyword is unclear:

```text
לא בטוח לאיזה מדריך התכוונת. כתוב אחת מהמילים האלה: <keywords>.
```

## Knowledge Base Roles

Links:

- Store source URLs only.
- Keep one line per guide.

Knowledge:

- Store role, tone, routing rules, collision rules, and "do not invent links".
- Explain what each guide is for.

Q&A:

- Store edge cases and natural user questions.
- Do not duplicate the full link table unless the platform needs exact examples.

## Required Handoff

```markdown
# DM Automation

carousel:
keyword:
guide_url:
matching_rule:
trigger_name:
dm_text:
public_reply:
automation_status:
automation_runtime:
automation_proof:
collision_check:
consent_scope:
dedupe_key:
rate_limit:
retention_policy:

## Links

## Knowledge

## Q&A
```

## Activation Proof

For a configured workflow, `automation_status: active` means all of these are true:

- Route exists in the configured route store.
- Route validation passes in the deployment environment.
- The configured HTTPS health endpoint reports a ready, non-dry-run service with no current error.
- A controlled synthetic test, sent only to an approved test account, returns the configured success status for the exact keyword.
- Dedupe and rate-limit checks pass.
- Logs exclude message bodies, access tokens, and unnecessary profile data.
- Retention and deletion behavior match the published privacy notice.

If any item is missing, use `automation_status: blocked`, not `active`.
