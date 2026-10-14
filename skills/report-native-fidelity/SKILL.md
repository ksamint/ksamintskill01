---
name: report-native-fidelity
description: Reconstruct PDF or PowerPoint report pages as source-bound native HTML and SVG, with full text and layout verification, review ledgers, and offline packages. Use when the user requires editable/selectable objects or word-by-word fidelity; ordinary OCR extraction does not establish this standard.
---

# Report Native Fidelity

## Contract

Preserve the user's document scope, page order, anchors and originals. Write a separate reconstruction unless replacement is authorized. Distinguish extraction coverage, native-object coverage, and verified fidelity. Never report one as proof of another.

A native page uses selectable HTML text, semantic tables, and SVG shapes, paths, chart elements, labels and connectors. Photographs remain image assets. A full-page image, transparent OCR overlay, rasterized chart or text converted only to paths is not a completed native reconstruction. Non-photographic raster content remains an explicit unresolved item until rebuilt. Keep reference page renders outside the reconstructed body.

Account for readable source text including footnotes, diagram labels, table cells, captions and text inside pictures. Preserve spelling, punctuation, numerals, units and language; do not silently correct the author's wording. Normalize only the search index. Record unreadable material instead of inventing it.

## Source and object extraction

1. Inventory source files, SHA-256 fingerprints, actual page counts and aliases. Keep byte-identical duplicates linked to every source name. Different revisions and alternate layouts are distinct records. Filename dates are not evidence of body dates.
2. Prefer original PPTX object/text/chart data where available. Inspect grouping, themes, transforms, crop, notes and embedded chart data; notes are separate content. Compare the displayed slide with the supplied PDF, because an editable source may be another revision.
3. For PDF, extract text, font/style/position, vector paths, clipping, layers and embedded images. Readable vector text stays text. Scan-only regions require OCR plus native rebuilding of non-photographic content. A chart cannot pass because surrounding text was extracted.
4. Bind every rendered object to a stable identifier, source fingerprint, actual page, source bounding box and object kind. Record extraction/reconstruction method and uncertainty. Preserve coordinate units and page size so a reviewer can locate the original region.
5. For charts record title, axis, scale, unit, legend, labels, series and displayed values. Prefer embedded data; values read from geometry are estimates, with method and uncertainty. Do not imply hidden data points, causal claims or results absent from the original. A visual match alone does not validate numeric meaning.
Photograph classification does not exempt watermarks, labels, signs or captions from text coverage. Inspect photo edges at source resolution; a source crop is not an OCR omission. Never complete a clipped account name or logo from familiarity. In review receipts, a confirmed photo requires `embedded_text_status: none_visible` with a coverage note, or `native_rebuilt` with `embedded_text_object_ids` referring to native text objects. Unreviewed or unresolved embedded text blocks acceptance.

6. Rebuild diagrams and mind maps with native text, nodes and connections, preserving hierarchy, direction and labels. Use source assets for photographs, retaining crop and attribution. Raster textures or logos need explicit classification; do not label a text-heavy picture as a photograph to bypass reconstruction.

Start with representative pages covering every present content kind, then continue the entire authorized scope. Use fingerprints and per-page checkpoints to resume work. Reuse verified extraction and reader components rather than building another application framework.

## Two independent visual reads

For each text region, retain source location, both independent readings, reader/model identity, timestamp, comparison, corrections and final state. Independence means the second reader reads the original region without the first transcription or proposed correction. Running the same OCR twice, comparing extracted text copies, or reviewing only an OCR transcript is not independent visual verification.

- **Round 1:** read the source image and reconcile every region against the reconstruction. Check all characters, punctuation, symbols, numbers, units, periods, proper nouns and table cells. Sweep for regions extraction missed entirely.
- **Round 2:** independently transcribe/read the original region; compare only afterward. Resolve differences by returning to the original at sufficient resolution. Record whether a correction concerns OCR, reconstruction or source ambiguity.
- **Layout review:** compare rendered and original full pages for placement, wrapping, layer order, crop, fonts, graphic topology and reading order. Screenshot metrics locate problems but cannot replace visual review.
- **Adjudication:** preserve conflicting readings and chosen source evidence. If still unreadable or disputed, mark unresolved. Never choose a plausible number merely to remove a discrepancy.

Use region states `pending`, `pass`, `unresolved`, or `not_applicable`, with reasons for the latter. A page passes text verification only when all applicable regions passed both reads, the coverage sweep is complete, and no discrepancy remains. Blank and photograph-only pages still require independent coverage confirmation. Keep text, object and layout states separate; any pending/unresolved applicable item prevents overall acceptance.

An older review is reusable only when its source fingerprint, region and required independent records match. Report denominators and reviewed region/page counts. Machine verification is not human certification or a guarantee of zero errors.

## Acceptance and offline delivery

Before reporting completion, check duplicate IDs, fingerprints, page bounds, missing objects, invalid references, missing assets and page order. Require a source record for every original page and alternate layout. Check numeric/text anchors and chart relationships, then inspect all rendered pages. Table rows/columns must remain associated with the correct labels.

Verify in both `file://` and local HTTP: selection, multilingual/numeric search, page/source jumps, long scrolling, thumbnails, mobile navigation, local fonts, image links and methods/summaries. Serve and package locally unless deployment was authorized.

When splitting delivery, use compatible relative paths across:

1. **HTML/data package:** native pages/SVG, full text, semantic tables, metadata, search data, fonts and review records.
2. **Image package:** photographs and necessary image assets. Required for the full reconstructed visual presentation when those assets exist, even if text search works without it.
3. **Optional original package:** unmodified PDFs/PPTX and other originals for recoverability and comparison.

Validate ZIP CRC, hashes, references and combined extraction. Measure final sizes rather than promising a compression ratio. Lossy previews cannot claim pixel-exact source recovery. Native HTML reconstruction does not promise original PPTX edit structure. Report outstanding pages and regions alongside partial deliverables.

## Local tool reuse

For the current repository, inspect implementation and `--help` before invoking tools:

- `/Users/af/cpro01/0thebrain01/datavisual01/scripts/report_to_html.py`: existing extraction, reader generation, annotations, methodologies, source maps and `--check` bundle checks.
- Sibling `report_methodologies.py` and `report_visuals.py`: source-bound analysis and visuals; their existence does not certify source verification.
- Sibling `report_pack_split.py` and `check_report_pack_split.py`: existing three-package workflow. Inspect completeness claims and adapt validation for native pages before reuse.
- Sibling `report_native.py`: `--from-reader INPUT --output NEW_FOLDER` creates source-bound extraction checkpoints; optional `--reviews RECEIPTS.json` and `--replacements PAGES.json` bind visual readings and authored native scenes. `--check NEW_FOLDER --require-verified` blocks acceptance while any page is pending. `report_to_html.py --native-from INPUT --output NEW_FOLDER` routes to the same implementation.
- Sibling `report_native_vision.py`: independent source-image transcription through an explicitly selected HTTPS vision model using an in-memory `LLM_API_KEY`. Its raw results are unverified diagnostic readings, not review receipts. Compare model outputs against readable original regions before selecting a cloud provider; a generic benchmark ranking does not establish accuracy for these documents.
- Sibling `report_native_mineru.py`: source-bound page splitting and resume-safe Precision VLM batches through the existing Data Merge wrapper. Preserve `plan.json` actual-page maps and batch checkpoints. Retry only confirmed failed pages in smaller chunks; unknown submission outcomes must be recovered, never blindly reposted. Responses may omit `data_id`, so retain filename matching. `coverage.json` combines successful retries without counting pages twice; cloud completion is not visual verification. Keep TLS validation enabled when result download fails.
- For missing Unicode font tables, a PDF texttrace Unicode→glyph-ID mapping may be used only when unambiguous for that exact embedded font. Compare each mapped glyph outline and advance after repair; preserve deterministic outputs and record the source mapping. For letters supplied only as original vector outlines, a Unicode-mapped font may preserve those contours as selectable text after independent character/boundary reading. This is distinct from displaying text solely as SVG paths; validate actual selection, glyph shape, position and source contour coverage before passing. The representative table builder at `native/replacements/build-d10.py` documents this case.
- Bind added reconstruction fonts and image crops through replacement `asset_bindings` with their SHA-256 values; changed bytes block acceptance. Keep source crops separate from an asserted completed native chart.
- Verify browser font loading before layout review. PDF fonts can contain malformed browser metadata or incomplete Unicode subsets even when extracted text is correct. Preserve original assets, check any repaired mappings/outlines, and rebind review fingerprints after rendering changes.
- `report_pack_split.py` refuses final native packages until the strict native gate passes. It retains native scene hashes, separates raster images, and excludes cloud task input archives. The older lossy preview packer refuses native projects because it cannot safely rewrite native asset bindings.

On another machine, find the user's equivalent converter instead of requiring these paths. Installing this skill does not mean any report has passed.
