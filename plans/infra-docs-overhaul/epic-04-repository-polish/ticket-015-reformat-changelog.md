# ticket-015 Reformat CHANGELOG to Keep a Changelog Standard

## Context

### Background

The current `CHANGELOG.md` uses simple `# version` headings with flat bullet lists. It lacks dates, category grouping (Added/Changed/Fixed/Deprecated/Removed), and comparison links between versions. The Keep a Changelog standard (https://keepachangelog.com/) is the widely adopted format that makes changelogs machine-parseable and human-readable.

### Relation to Epic

Third ticket in Epic 4 (Repository Polish). It brings the CHANGELOG to a professional standard, complementing the expanded README (ticket-013) and CONTRIBUTING (ticket-014).

### Current State

The file `/home/rogerio/git/inewave/CHANGELOG.md` contains:

- 28 version entries from `v0.0.98` through `1.13.0`
- Headings use `# version` format (some with `v` prefix, some without)
- Entries are flat bullet lists mixing Added/Changed/Fixed categories without labels
- No dates on any version
- No comparison links
- Versions `v0.0.1` through `v0.0.97` are not in the CHANGELOG (only `v0.0.98` onward)

Git tags are available for all versions with creation dates. The relevant date mapping for versions in the CHANGELOG (from v0.0.98 onward):

- v0.0.98: 2023-08-01, v1.0.0: 2023-08-02, v1.1.0: 2023-08-24, v1.1.1: 2023-08-25, v1.1.2: 2023-08-28
- v1.2.0: 2023-09-14, v1.2.1: 2023-09-14, v1.2.2: 2023-09-15, v1.3.0: 2023-09-15, v1.4.0: 2023-09-29
- v1.5.0: 2023-10-11, v1.5.1: 2023-12-22, v1.5.2: 2024-01-02, v1.5.3: 2024-01-02, v1.5.4: 2024-01-04
- v1.5.5: 2024-01-04, v1.5.6: 2024-01-05, v1.5.7: 2024-01-17, v1.6.0: 2024-02-19, v1.7.0: 2024-02-23
- v1.7.1: 2024-02-26, v1.7.2: 2024-03-01, v1.7.3: 2024-03-01, v1.7.4: 2024-04-12, v1.7.5: 2024-04-12
- v1.8.0: 2024-04-24, v1.8.1: 2024-05-08, v1.9.0: 2024-07-18, v1.9.1: 2024-07-18, v1.9.2: 2024-09-19
- v1.10.0: 2025-01-02, v1.10.1: 2025-07-09, v1.10.2: 2025-07-14, v1.10.3: 2025-08-04, v1.10.4: 2025-09-20
- v1.11.0: 2025-11-05, v1.11.1: 2025-11-10, v1.11.2: 2025-12-03, v1.12.0: 2026-02-02, v1.12.1: 2026-03-05
- 1.13.0: no tag yet (unreleased)

## Specification

### Requirements

1. Add the Keep a Changelog header block at the top of the file:

   ```
   # Changelog

   Todas as mudancas notaveis neste projeto serao documentadas neste arquivo.

   O formato e baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
   e este projeto adere ao [Versionamento Semantico](https://semver.org/lang/pt-BR/).
   ```

2. Convert version `1.13.0` (no git tag) to an `[Unreleased]` section or `[1.13.0] - Unreleased` section since it has not been released yet
3. Add dates to all other version headings using format `## [version] - YYYY-MM-DD`, sourced from git tag creation dates listed above
4. Normalize version prefix: use `[1.x.y]` format consistently (no `v` prefix in the heading, `v` prefix in comparison links)
5. Categorize existing bullet points under Keep a Changelog categories:
   - **Adicionado** (Added): new features, new file support, new classes
   - **Modificado** (Changed): dependency updates, refactors, format changes
   - **Corrigido** (Fixed): bug fixes (entries starting with "Correcao", "Fix", "Hotfix")
   - **Descontinuado** (Deprecated): deprecation notices
   - **Removido** (Removed): removed features
6. Add comparison links at the bottom of the file for all versions
7. Keep all entry text in Brazilian Portuguese as-is (do not rewrite entries)
8. Reformat ALL versions in the CHANGELOG (from v0.0.98 through 1.13.0)

### Inputs/Props

- Current file: `/home/rogerio/git/inewave/CHANGELOG.md`
- Git tag dates: listed in Context section above
- Repository URL for comparison links: `https://github.com/rjmalves/inewave`

### Outputs/Behavior

A reformatted `CHANGELOG.md` following Keep a Changelog format with dates, categories, and comparison links.

### Error Handling

Not applicable — static markdown file.

## Acceptance Criteria

- [ ] Given the file `/home/rogerio/git/inewave/CHANGELOG.md`, when inspected, then every released version heading follows the format `## [X.Y.Z] - YYYY-MM-DD` (e.g., `## [1.12.1] - 2026-03-05`)
- [ ] Given the file `/home/rogerio/git/inewave/CHANGELOG.md`, when inspected, then every version section has its bullet points grouped under at least one of the category subheadings: `### Adicionado`, `### Modificado`, `### Corrigido`, `### Descontinuado`, or `### Removido`
- [ ] Given the file `/home/rogerio/git/inewave/CHANGELOG.md`, when inspected, then the file contains a comparison links section at the bottom with entries like `[1.12.1]: https://github.com/rjmalves/inewave/compare/v1.12.0...v1.12.1`
- [ ] Given the file `/home/rogerio/git/inewave/CHANGELOG.md`, when inspected, then the version `1.13.0` is presented as unreleased (either `[Unreleased]` or `[1.13.0] - Unreleased`)
- [ ] Given the file `/home/rogerio/git/inewave/CHANGELOG.md`, when inspected, then all original entry text is preserved in Brazilian Portuguese (no entries deleted or translated)

## Implementation Guide

### Suggested Approach

1. Read the current `/home/rogerio/git/inewave/CHANGELOG.md`
2. Add the KAC header block at the top
3. For each version section:
   a. Change heading from `# version` to `## [version] - YYYY-MM-DD` using the date mapping from the Context section
   b. Classify each bullet point into the appropriate category:
   - Entries starting with "Correcao", "Fix", "Hotfix", "Correção" go under `### Corrigido`
   - Entries starting with "Suporte a", "Novo", "Introdução", "Adoção", "Total de", "Ativação" go under `### Adicionado`
   - Entries starting with "Atualização", "Refactor", "Gestão", "Conversão", "Padronização", "Descontinuado o uso de" go under `### Modificado`
   - Entries mentioning "marcadas como descontinuadas" or "deprecated" go under `### Descontinuado`
     c. Group bullets under the appropriate `### Category` subheading
4. For version `1.13.0` (no tag), use `## [1.13.0] - Unreleased` as the heading
5. Add comparison links section at bottom:
   ```
   [Unreleased]: https://github.com/rjmalves/inewave/compare/v1.12.1...HEAD
   [1.12.1]: https://github.com/rjmalves/inewave/compare/v1.12.0...v1.12.1
   ...
   [1.0.0]: https://github.com/rjmalves/inewave/compare/v0.0.98...v1.0.0
   [0.0.98]: https://github.com/rjmalves/inewave/releases/tag/v0.0.98
   ```

### Key Files to Modify

- `/home/rogerio/git/inewave/CHANGELOG.md` — reformat in place

### Patterns to Follow

- Use Portuguese category names: Adicionado, Modificado, Corrigido, Descontinuado, Removido (matching the Portuguese KAC translation at keepachangelog.com/pt-BR/)
- Keep entries in their original Portuguese text — do not rewrite or improve grammar
- Use `## [version]` (H2) for version headings, `### Category` (H3) for category subheadings (KAC standard)

### Pitfalls to Avoid

- Do NOT add dates to version 1.13.0 — it has no git tag and is unreleased
- Do NOT add entries for versions before v0.0.98 — those were not in the original CHANGELOG
- Do NOT rewrite or translate existing entry text — preserve exactly as written
- Do NOT use English category names (Added/Changed/Fixed) — use Portuguese per the project language convention
- Do NOT omit the comparison links section — it is an integral part of KAC format

## Testing Requirements

### Unit Tests

Not applicable — documentation file.

### Integration Tests

Not applicable.

### E2E Tests (if applicable)

Not applicable. Manual verification: confirm the file renders correctly as markdown and all comparison links use valid tag names.

## Dependencies

- **Blocked By**: None
- **Blocks**: None

## Effort Estimate

**Points**: 2
**Confidence**: High
