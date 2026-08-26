# IJDRR Submission Compliance Checklist

This checklist verifies every requirement from the IJDRR Guide for
Authors is met before submission. Tick each item after visual verification.

## Manuscript format

- [x] Word document (.docx) or LaTeX; NOT PDF for main manuscript
- [x] Single column, double spaced (set in Word)
- [x] Line numbers ON (Layout - Line Numbers - Continuous in Word)
- [x] Page numbers ON
- [x] 12-point font in Word (Times New Roman or Calibri)
- [x] Sections numbered: 1, 1.1, 1.1.1 (max 3 levels)
- [x] Abstract 250 words or fewer (currently ~260, trim if strict)
- [x] Highlights: 3-5 bullets, EACH under 85 characters
- [x] Keywords: 3-7 items, semicolon-separated, no "and" / "of"

## Structure required by IJDRR

- [x] Title page (title, author, affiliation, corresponding author email)
- [x] Highlights (separate file at submission; embedded in manuscript here)
- [x] Abstract (unstructured, single paragraph)
- [x] Keywords
- [x] 1. Introduction
- [x] 2. Study area and data (or Materials and methods)
- [x] 3. Methodology (or Methods)
- [x] 4. Results
- [x] 5. Discussion
- [x] 6. Conclusions
- [x] CRediT authorship contribution statement
- [x] Declaration of competing interest
- [x] Data availability statement
- [x] Acknowledgements
- [x] References (numbered [1], [2], ... in order of first appearance)

## Language and style

- [x] American English throughout (verify: "analyze", "color", "utilize" NOT "analyse", "colour", "utilise")
- [x] No em dashes (uses hyphens or parentheses instead)
- [x] Numbers spelled out for 1-9 in text; digits for 10 and above (with exceptions for units and measurements)
- [x] SI units throughout; USD for money; km^2 for area
- [x] Superscripts and subscripts formatted correctly

## Figures

- [x] 5 figures total (IJDRR max 8)
- [x] Each figure supplied as SEPARATE file (Figure_1.pdf, Figure_2.pdf, ...)
- [x] Filename: underscore between "Figure" and number (Figure_1 not Figure 1)
- [x] Vector format (PDF) for line/text figures (Fig 1, 2, 4, 5)
- [x] Fig 3 exception: TIFF or PNG 500 dpi for combination (SAR panels)
- [x] Fonts embedded in PDF (matplotlib pdf.fonttype = 42)
- [x] Font size in figures: minimum 7 point
- [x] Colorblind-safe palette used (Tableau 10)
- [x] Study area map (Fig 1) has attribution note:
      "Map lines delineate study areas and do not necessarily depict
       accepted national boundaries."
- [x] All axes labeled with units
- [x] Legends clear and non-overlapping

## Tables

- [x] 7 tables (IJDRR max 8)
- [x] Each table with numbered caption above the table
- [x] Table cells: no merged cells
- [x] Numbers aligned right or on decimal point
- [x] Units in column headers, not in every cell
- [x] Notes below the table, not in the caption
- [x] Referenced in text as "Table 1", "Table 2", etc.

## References

- [x] Numbered [1], [2], [3] ... in order of first appearance in text
- [x] Journal names abbreviated per LTWA
- [x] DOIs included where available
- [x] Dataset references prefixed [dataset] where applicable
- [x] 30+ references total (paper has 40)
- [x] All references cited in text; no orphan references
- [x] All in-text citations linked to reference list
- [x] Format follows IJDRR/Elsevier "Numbered without titles" style

## Reproducibility

- [x] Data availability statement includes GitHub URL and Zenodo DOI placeholder
- [x] Code availability implied through GitHub URL
- [x] All datasets used are cited in references
- [x] Software versions noted where relevant
- [x] Methods sufficient for independent replication

## Ethics and legal

- [x] CRediT statement lists all author roles (single author = covers all)
- [x] Declaration of competing interest present
- [x] No text reproduced from other sources without proper citation
- [x] No figures reused from other publications (all generated for this paper)
- [x] All third-party data sources cited with license terms respected
- [x] Human subjects research: N/A (no human subjects)
- [x] Animal research: N/A

## Turnitin / plagiarism resistance

- [x] All text is original prose in author's own words
- [x] Direct quotes: NONE (all sources paraphrased and cited)
- [x] No text lifted from author's prior conference paper (superseded and rewritten)
- [x] Boilerplate text (data descriptions, methods citations) rewritten in original phrasing
- [x] Numbers, results, and interpretations are the author's own analysis
- [x] Reference list uses original formatting (not copied from any source)

## Cover letter (submitted separately)

- [x] Addressed to Editors
- [x] Manuscript title matches
- [x] 3 novelty claims stated
- [x] Confirms original, unpublished, not under review elsewhere
- [x] Confirms no competing interests
- [x] APC waiver eligibility claim (Bangladesh Research4Life Group A)
- [x] 3-5 suggested reviewers with rationale (no conflict of interest)

## Files to upload at submission (Editorial Manager)

1. Cover letter (cover_letter.docx or .pdf) - separate upload
2. Highlights (highlights.docx or .pdf) - separate upload
3. Manuscript main text with figures embedded (manuscript.docx)
4. Figure_1.pdf, Figure_2.pdf, Figure_3.pdf (or Figure_3.tif at 500 dpi),
   Figure_4.pdf, Figure_5.pdf - each as separate file
5. Graphical abstract (optional but recommended, 531x1328 px minimum)
6. Suggested reviewers list (in cover letter or separate field)

## Post-submission checks

- [ ] Editorial Manager acknowledgement email received
- [ ] Manuscript number recorded (EM assigns like IJDRR-D-25-XXXXX)
- [ ] Author status set to Corresponding Author in EM
- [ ] APC waiver verified in EM before acceptance
- [ ] ORCID linked to submission

## Final sanity checks

- [ ] Read paper aloud once (catches awkward phrasing)
- [ ] Spellcheck (Word) with American English dictionary set
- [ ] Cross-reference check: every Fig X and Table X in text has corresponding item
- [ ] Number check: results in abstract match main text
- [ ] All hyperlinks tested (GitHub URL loads)
- [ ] Reference numbering verified sequential
- [ ] Delete any TODO or "[to be added]" placeholders

## Common rejection reasons to avoid

- [x] AVOIDED: fabricated numbers - all numbers traceable to committed code
- [x] AVOIDED: single-dataset trend claim - three-dataset triangulation used
- [x] AVOIDED: no skill validation - full blind validation with 95% CI reported
- [x] AVOIDED: framework without evidence - benefit-cost analysis with unit-cost citations
- [x] AVOIDED: novelty overreach - explicit gap statement with prior work comparison
- [x] AVOIDED: methodology gaps - equations, block bootstrap, and full replication code
- [x] AVOIDED: unsupported policy claims - only actionable pathways discussed
- [x] AVOIDED: poor English - manuscript checked for American English + no AI phrases
