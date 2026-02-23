# Epic 05: Quality and Type Safety

## Goals

1. Enable mypy strict mode and fix all resulting type errors
2. Improve type annotations across the codebase (return types, parameter types, generics)
3. Reduce code duplication in nwlistop models and archive base classes
4. Adopt @overload patterns from cfinterface where applicable
5. Clean up `# type: ignore` comments where possible

## Scope

- mypy configuration update and progressive error fixing
- Type annotation improvements across all modules
- Deduplication of common patterns in nwlistop
- Adoption of cfinterface typing patterns

## Tickets (Outline)

| Ticket     | Title                                                    | Effort   |
| ---------- | -------------------------------------------------------- | -------- |
| ticket-023 | Enable mypy strict mode and fix newave module errors     | 3 points |
| ticket-024 | Fix mypy strict mode errors in nwlistop module           | 5 points |
| ticket-025 | Reduce code duplication in nwlistop archive base classes | 3 points |
| ticket-026 | Clean up type ignore comments and add proper annotations | 2 points |

## Dependencies

- **Blocked By**: Epic 02 (TabularSection adoption reduces type issues)
- **Blocks**: None
