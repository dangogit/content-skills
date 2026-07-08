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
Do: send private DM
Public reply: שלחתי לך בפרטי
Collision notes: <none or explanation>
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

## Links

## Knowledge

## Q&A
```

## Activation Proof

For the user's current workflow, `automation_status: active` means all of these are true:

- Route exists in `tools/instagram-cta-automation/routes.json`.
- Route is synced to `<host>:~/instagram-cta-automation/routes.json`.
- Local and the remote host `npm run validate:routes` pass.
- the remote host service `com.<user>.instagram-cta-automation` is listening on `127.0.0.1:18787`.
- Health endpoint returns `dry_run:false`, `poll_enabled:true`, and `last_error:null`.
- Synthetic dry-run with the exact keyword returns `status:"sent"`.

If any item is missing, use `automation_status: blocked`, not `active`.
