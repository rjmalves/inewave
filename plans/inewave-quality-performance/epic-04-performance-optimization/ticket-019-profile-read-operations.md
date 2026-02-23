# ticket-019 Profile inewave read operations and identify bottlenecks

> **[OUTLINE]** This ticket requires refinement before execution.
> It will be refined with learnings from earlier epics.

## Objective

Profile the most common inewave read operations (reading pmo.dat, hidr.dat, and 5-10 representative nwlistop output files) to identify performance bottlenecks. Produce a profiling report that quantifies time spent in file I/O, parsing, DataFrame creation, and cfinterface infrastructure. This report informs the optimization work in tickets 020-022.

## Anticipated Scope

- **Files likely to be modified**: None (profiling scripts created in `benchmarks/` directory)
- **Key decisions needed**: Which files to profile (representative mix of SectionFile, RegisterFile, BlockFile); which profiling tool to use (cProfile + snakeviz, py-spy, or manual timing)
- **Open questions**:
  - Do we have large enough real-world test data to get meaningful profiling results?
  - After the TabularSection migration (Epic 02), what is the new performance baseline?
  - Where does the time go: cfinterface infrastructure, Line.read(), DataFrame construction, or I/O?

## Dependencies

- **Blocked By**: ticket-013
- **Blocks**: ticket-020, ticket-021

## Effort Estimate

**Points**: 3
**Confidence**: Low (will be re-estimated during refinement)
