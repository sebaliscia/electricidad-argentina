# Resumen de validación v0.10.0

Estado general: **PASS**.

Controles: 30 PASS; 0 PASS_WITH_LIMITATION; 0 NOT_APPLICABLE; 0 FAIL.

| Control | Estado | Detalle |
|---|---|---|
| baseline_sha256 | PASS | dc5f5348f5f82f78ec252cbc607703543f7186702bea790c6606c329e30749dc |
| baseline_zip_integrity | PASS | entries=801; bad=None |
| baseline_internal_manifest | PASS | checked=800; mismatches=0 |
| pdf_pages | PASS | 46 |
| pdf_a4 | PASS | all pages |
| pdf_portrait | PASS | all pages |
| pdf_metadata_title | PASS | Electricidad argentina: cambio, límites y decisiones |
| pdf_metadata_author | PASS | Sebastián Liscia |
| pdf_fonts_embedded | PASS | fonts=7; not_embedded=[] |
| pdf_links | PASS | 74 |
| pdf_bookmarks | PASS | 18 |
| pdf_selectable_text | PASS | characters=93695 |
| front_order_letter | PASS | Carta del autor: Es aquí el autor quien les escribe. El auto |
| author_letter_literal | PASS | reference_chars=12522; pdf_chars=12522 |
| front_order_toc_before_body | PASS | toc=12949; chapter1=13096 |
| required_scope_sentence | PASS | count=1 |
| eleven_chapters | PASS | missing=[] |
| buenos_aires_literal | PASS | literal category present |
| pdf_no_raw_tokens_or_filenames | PASS | hits=[] |
| scope_forbidden_sections_absent | PASS | hits=[] |
| figure_count | PASS | 28 |
| map_count | PASS | 4 |
| figure_interpretation_complete | PASS | failures=[] |
| canonical_metrics_present | PASS | rows=100 |
| regional_structural_nuclear_zeros | PASS | rows=16 |
| scenario_boundary | PASS | rows=4 |
| node_crosswalk_counts | PASS | {"MATCHED_SPATIAL_AND_NAME": 94, "MATCHED_SPATIAL_ONLY": 6, "MISSING_COORDINATES": 3, "NO_CONFIDENT_MATCH": 308} |
| figure_png_integrity | PASS | count=28; bad=[] |
| release_manifest | PASS | listed=213; physical=214; mismatches=0 |
| zero_active_fail | PASS | files=[] |
