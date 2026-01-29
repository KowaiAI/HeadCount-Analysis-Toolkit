# DC Sex Offender Registry Investigation

## Summary

DC is one of only 4 U.S. jurisdictions that refuses to publish racial demographic data for its sex offender registry. Using HeadCount, we scraped 1,066 mugshots and manually categorized them.

**Finding:** DC's registry is **10x less white** than the national average.

---

## Data

| Race | Count | DC Registry | National Avg |
|------|-------|-------------|--------------|
| Black | 934 | 87.6% | 27% |
| White | 76 | 7.1% | 72% |
| Hispanic | 46 | 4.3% | — |
| Asian | 4 | 0.4% | — |
| Other | 6 | 0.6% | — |
| **Total** | **1,066** | | |

---

## Context

### Why This Matters

- DC population: ~38% white, ~45% Black
- DC registry: 7% white, 88% Black
- National registries: 72% white, 27% Black

White DC residents are **5x underrepresented** vs population and **10x underrepresented** vs national registry averages.

### Related Disparities

| Metric | Finding | Source |
|--------|---------|--------|
| DC felony convictions | 96% Black | DC Sentencing Commission 2022 |
| Arrest rates | Black residents at 10x rate | ACLU-DC 2018 |
| USAO-DC declinations | 56% of arrests declined | SAVRAA Report 2016 |

---

## Methodology

**Source:** sexoffender.dc.gov (public registry)

**Collection:** Selenium web scraper with pagination handling

**Sample:** 1,066 photographs (Class A and B offenders)

**Classification:** Manual visual categorization by apparent race

**Date:** January 2026

**Limitations:**
- Visual assessment may not match self-identification
- Class C offenders not included (in-person viewing only)
- Some low-quality images categorized as "other"

---

## Sources

1. Ackerman, A. R., & Sacks, M. (2012). "Can General Strain Theory Be Used to Explain the Overrepresentation of Minorities on American Sex Offender Registries?" *Journal of Criminal Justice*

2. DC Sentencing Commission. (2022). *Annual Report*

3. ACLU of DC. (2018). *Racial Disparities in DC Policing*

4. CSOSA Sex Offender Registry Metadata

5. U.S. Census Bureau, DC Population Estimates
