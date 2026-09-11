# Public Beta Checklist

A candidate may be technically ready while still being legally blocked.

## Technical gates

- [ ] repository beta-candidate regression passes;
- [ ] RC-readiness report passes its internally checkable gates and still reports external gates truthfully;
- [ ] stabilization surface remains frozen at 9 profiles / 14 semantic modules unless a documented corrective migration is required;
- [ ] exact candidate commit is recorded by `scripts/release/candidate_evidence.py` from a clean, non-shallow checkout;
- [ ] full-history credential/key scan passes on that exact candidate commit;
- [ ] `pse doctor --deep` passes in candidate environment;
- [ ] Windows CI passes on candidate commit;
- [ ] macOS CI passes on candidate commit;
- [ ] Linux CI passes on candidate commit;
- [ ] installed-wheel registry/discovery passes;
- [ ] security regression passes;
- [ ] release/tamper regression passes;
- [ ] README EN/VI version/status synchronized;
- [ ] public API/schema matrix matches runtime;
- [ ] repository contains no confidential downstream material.

## Legal/commercial gates

- [x] Legal Architecture v1 captured from maintainer decisions;

- [ ] community/source-available license reviewed and finalized;
- [ ] final `LICENSE` committed;
- [ ] citation/attribution obligation reviewed for enforceability and practicality;
- [ ] commercial-use boundary reviewed;
- [ ] contributor rights / dual-licensing permission finalized;
- [ ] commercial licensing contact channel published;
- [ ] warranty/liability/jurisdiction language reviewed where applicable.

## Release gate

Only when all required boxes are complete may the maintainer create and advertise a public licensed beta tag.
