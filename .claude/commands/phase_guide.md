The user has requested a phase guide for: $ARGUMENTS

Parse $ARGUMENTS as: <phase_number> [subsection]
Examples: "0" → full Phase 0 guide. "0 config" → Phase 0 config subsection only. "4 features" → Phase 4 features subsection only.

Read CLAUDE.md fully to understand the project identity, tool stack, engineering patterns, phase plan, and module structure before writing anything.

Then produce a guide and write it to:
- Full phase: guides/phase_<N>_guide.md
- Subsection: guides/phase_<N>_<subsection>_guide.md

The guide must contain these sections:

## Objective
One paragraph: what this phase/subsection delivers and why it matters at this point in the project. Reference the vertical-slice or SOLID principle it advances.

## Prerequisites
What must already exist (from prior phases) before this work starts. List specific files, services, or ABCs that this phase depends on.

## Files to Create / Modify
Exact paths under the repo, with one-line description of each file's role. No files outside the module structure defined in CLAUDE.md.

## Implementation Order
Numbered steps in the order they must be built. Each step names the file, the class/function to write, the design pattern in use, and the SOLID principle it demonstrates. Flag any DSA or algorithmic consideration inline if relevant (e.g. O(n²) trap to avoid).

## Key Design Decisions
The non-obvious choices made in this phase — why this pattern over another, why this interface shape, what was explicitly rejected and why. Ground each decision in the project's Core Design Philosophy from CLAUDE.md.

## Tests to Write
Specific pytest cases for this phase: what to assert, what edge cases matter, what must NOT be tested (e.g. don't test framework internals).

## Definition of Done
Checklist. The phase/subsection is complete only when every item is checked. Last item is always: "PR opened on feature branch, not pushed to main."

## Connects To
How the output of this phase feeds into the next phase or subsection. Name the specific ABCs or interfaces that downstream phases will depend on.

Write the file, then confirm the path to the user.
