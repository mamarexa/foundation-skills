# Second step: restyling the file with other tools

<!-- Shared by business-plan-writer and pitch-deck-writer. Both copies must stay identical:
     skills/tests/test_scripts.py checks it. -->

This skill's renderer does one job well: it produces a clean, correct `.docx` / `.pptx` whose
numbers come straight from Foundation's engine. For **advanced changes**, hand the finished
file to a document tool as a **second step**. Advanced changes include:

- applying the founder's own brand template, fonts, colours or slide master;
- converting charts to native, editable Office charts;
- tracked changes and comments for a co-founder or advisor;
- heavier visual design.

## The rule for any second step

1. **Only the design changes.** The text and **every number** stay exactly as rendered. The
   restyling tool must be told this explicitly.
2. **Keep the original.** Save the restyled file under a new name.
3. **Verify the numbers afterwards:**
   ```
   python scripts/check_numbers.py business-plan.docx business-plan-branded.docx
   python scripts/check_numbers.py pitch-deck.pptx pitch-deck-branded.pptx
   ```
   Anything reported as missing or new means the restyle changed content. Fix it, or deliver
   the original instead. Never deliver a restyled file that fails this check.
4. Run the writing-style pass again (`references/writing-style.md`) if the tool rewrote any
   text.

## Which tool to use, by environment

Use what the founder's environment already has. Check what's actually available before
promising it, because these products change often.

| You're running in | Word (.docx) second step | PowerPoint (.pptx) second step |
|---|---|---|
| **Claude** (claude.ai, Claude Desktop, Claude Code with Anthropic's skills) | Anthropic's built-in **`docx`** skill: editing an existing file, templates, tracked changes, comments, validation | Anthropic's built-in **`pptx`** skill: editing from a template, native charts, curated palettes, rendered QA |
| **ChatGPT / Codex** (OpenAI) | ChatGPT's built-in document handling (its code environment ships document skills, and ChatGPT can edit Word files). In Codex CLI, check `~/.codex/skills` and the OpenAI plugins directory for a document skill, otherwise use an open-source one (below) | ChatGPT's built-in slides/presentation handling. In Codex, as for Word |
| **Google** (Gemini app, Gemini in Workspace, Gemini CLI) | Open the `.docx` in **Google Docs** and use Gemini in Docs to restyle, then download as .docx. Gemini CLI reads SKILL.md skills but ships no Office skill, so use an open-source one (below) | Import the `.pptx` into **Google Slides** and use Gemini in Slides (restyle, apply a theme), then download as .pptx. Gemini CLI: as for Word |
| **Microsoft 365 Copilot** | Copilot in Word, with the organisation's templates | Copilot and Designer in PowerPoint, applying the organisation's template or slide master |
| **Cursor** (and other editors that read SKILL.md: Copilot in VS Code, OpenCode…) | No built-in Office skill. Use the `--template` option below, or an open-source skill | No built-in Office skill. Use an open-source skill (below) |
| **Anything else** | The `--template` option below | An open-source skill (below) |

### Open-source options that work across agents (checked September 2026)

- **PowerPoint:**
  - [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) (MIT). Fills an existing
    `.pptx` template with new content while keeping its design. Works with Claude Code,
    Cursor, Codex and Gemini CLI.
  - [kangdacool/pptx-editing-skill](https://github.com/kangdacool/pptx-editing-skill) (MIT).
    Careful edits to an existing deck without losing hand edits or speaker notes.
  - [siril9/presentation-skill](https://github.com/siril9/presentation-skill) (MIT).
    Source-first deck generation with layout QA.
- **Word:** no mature open-license skill was found. Use this skill's own template support,
  which rebuilds the plan inside the founder's `.docx` (their styles, fonts, page setup,
  header and footer):
  ```
  python scripts/build_docx.py plan.json business-plan.docx --facts facts.json --template founder-template.docx
  ```
  Otherwise use [Harshuqt/office-agent-skills](https://github.com/Harshuqt/office-agent-skills)
  (Apache-2.0, early stage), or open the file in Word, Google Docs or LibreOffice and apply the
  template's styles there.

Install community skills only from sources the founder trusts. Read a skill's SKILL.md and
scripts before running it, as with any code.
