# LPG image database, 2026-10-10

The owner directed that LPG use fair use as its project basis. Store that basis independently of original source licenses and attributions. It supersedes treating a missing permissive license as an automatic acquisition blocker. It does not turn an image match into a verified design, erase attribution, or establish a public-domain claim. This database creation does not deploy reference images into the public app.

## Delivered build

`LPG_Image_Database_2026-10-10.zip` contains SQLite, original image files, display copies, thumbnails, source archives, attribution, JSON imports, schema, README and hash inventory.

- 1,138 original LPG UIDs preserved; 3 separate report candidates, for 1,141 records.
- 101 existing jurisdictions preserved, including US territories and the existing Canadian/Mexican scope.
- 91 acquired assets: 88 recovered Washington gallery files plus all 3 report-linked photographs. Gallery assets include site graphics and other unclassified files; they are not 91 verified plate designs.
- 54 canonical LPG records have candidate image links; 1,084 still have none. The 291 existing schematics are not counted as acquired photographs.
- 164 aspect-preserving JPEG derivatives; no upscaling or generated replacement imagery.
- 59 plate-to-asset associations, all candidate/conflict; 0 approved app images.
- Database integrity, foreign keys, exact original UID preservation and all packaged asset/derivative hashes passed validation.

## Corrections to the supplied report

The report is an outline plus three samples, not a 56-jurisdiction image database. Its Puerto Rico row calls the image a 2023 standard, but the source identifies Mayagüez 2010 and dates the photograph to 2015. Arkansas source credits SuperSonic337, not Mattes. Puerto Rico's photograph is CC BY 2.0 DE alongside a separate public-domain assertion about the depicted object. Date ranges remain claims, not confirmed era fields. A single temporary Wikimedia rate-limit failure was retried successfully.

## Rebuild

```
python tools/fetch_report_images.py --out REPORT_IMAGE_INPUTS
python tools/build_lpg_database.py --evidence EXTRACTED_WA_ARCHIVE --report-images REPORT_IMAGE_INPUTS --report INPUT_REPORT.md --out NEW_OUTPUT_FOLDER
```

Dependencies: Python 3, SQLite (stdlib), Pillow. The builder is offline. The input Washington archive is `plate-image-evidence-batch01-WA.zip`; the uploaded report is `deep-research-report (5).md`. Retrieve saved evidence when scratch has been pruned. Source catalog baseline: GitHub main `809ce4e627f1e0cca440600d548291d58dcc9dc9`.

## Import contract

`exports/lpg-import.json` contains all rows with candidate/conflict status and relative image paths. `exports/approved-app-images.json` is empty until identity and human visual checks are recorded; do not silently replace the live catalog with report candidates. `coverage` and `issues` SQL views/tables provide the next work queue. Keep the archive's folder structure intact.

Next: reconcile the report samples with canonical design/era records, expand acquired image coverage and build the late-stage visual comparison workflow. No new APK or live database migration was performed in this task.
