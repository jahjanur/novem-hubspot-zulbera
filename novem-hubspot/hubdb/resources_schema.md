# `resources` HubDB table — schema reference

This file is the canonical reference for the HubDB table the theme expects.
The CSV in this directory is a column listing for humans — HubSpot does not
import HubDB tables directly from CSV, so create the table manually in the
portal (Marketing → Files and Templates → HubDB → Create table) using the
columns below.

| Column | Type | Notes |
|---|---|---|
| `title` | TEXT | Card title and detail-page H1. |
| `slug` | TEXT | Page path under `/resources/`. **Also set the row's Page Path field to this same value** so dynamic-page routing works. |
| `type` | SELECT | One of: `case-study`, `white-paper`, `blog`, `press-release`. Drives the badge color and label. |
| `client` | TEXT | Optional. Client/company name (case studies). |
| `industry` | TEXT | Optional. Tag shown in the card meta row. |
| `publish_date` | DATE | Optional. Shown in card and detail meta. |
| `summary` | TEXT | Card excerpt and detail-page lede paragraph. |
| `body` | RICHTEXT | Detail-page main content. |
| `results` | RICHTEXT | Optional. Rendered under a "Results" H2 (case studies). |
| `hero_image` | IMAGE | Card image and detail-page hero. |
| `stat1_num` / `stat1_label` | TEXT | Optional headline stat 1 (e.g. "$5M" / "Claim prevented"). |
| `stat2_num` / `stat2_label` | TEXT | Optional headline stat 2. |
| `stat3_num` / `stat3_label` | TEXT | Optional headline stat 3 (detail page only). |
| `seo_title` | TEXT | Optional override for the page's `<title>`. |
| `seo_description` | TEXT | Optional meta description. |
| `og_image` | IMAGE | Optional social-share image. Falls back to `hero_image`. |

## Settings to enable on the HubDB table

- **Allow public API access** → ON (required for HubL queries)
- **Use for dynamic pages** → ON
- **Dynamic Page route by** → `Page Path` (built-in)
- Set each row's **Page Path** equal to its `slug` value (e.g. `bc-events`).

## After creating the table

1. Copy the table's numeric ID from the URL or settings panel.
2. In Design Manager → `novem-theme` → **Theme settings** → **HubDB**, paste it into **Resources HubDB table ID**.
3. Create a page using the `resource-detail.html` template, then in
   **Page Settings → Advanced Options → Dynamic Pages** select the `resources` table.
   That single page will serve every row at `/{parent-path}/{slug}`.

## Seed rows — real content (import files in this directory)

The placeholder rows have been **replaced with the client's real content**. Import-ready
data is generated in this directory:

- **`resources_rows.csv`** — all 23 rows, one column per HubDB field (spreadsheet-friendly).
- **`resources_rows.json`** — same rows in HubDB Rows API shape (`{path, name, values:{…}}`),
  ready to POST to `/cms/v3/hubdb/tables/{tableId}/rows/draft/batch/create`.

`body` is rich HTML (the article content, **excluding** the lede — that lives in `summary` —
and **excluding** the headline stats, which live in `stat1..3`). Case-study `client` holds
the **anonymized descriptor** only (e.g. "A specialized dementia and long-term care facility
in Western Canada") — no real client names, per the client's confidentiality requirement.

Source of truth: the `.docx` files in `BLOG POSTS/` and `CASE STUDIES/` (anonymized
`Anon - …` copies only) plus the press-release text. Regenerate with `.build/gen.py`.

### Case studies (5)
| slug | client (anonymized) | title |
|---|---|---|
| `dementia-care-continuous-commissioning` | A specialized dementia & long-term care facility | Automated Continuous Commissioning Unlocks $200K+ at a Specialized Dementia Care Facility |
| `seniors-living-outbreak-reduction` | A regional seniors living operator (120-resident) | 65% Fewer Outbreak Weeks at a Regional Seniors Living Operator |
| `events-campus-claim-prevention` | A major Western Canadian events & entertainment campus | Preventing a $5M Claim at a Major Western Canadian Events Campus |
| `mixed-use-office-accelerated-commissioning` | A landmark mixed-use office tower | From 36 to 4 Months: Accelerated Commissioning at a Landmark Mixed-Use Office Tower |
| `seniors-housing-insurance-savings` | A Western Canadian independent seniors housing developer | 10% Insurance Savings and 30% Digital Infrastructure Savings for an Independent Seniors Housing Developer |

### Blog (17)
`tcro-vs-cost-of-risk`, `data-governance-financial-control`, `reactive-to-predictive-maintenance`,
`7-criteria-digital-risk-platform`, `insurance-no-longer-fixed-line-item`, `make-data-pay`,
`tcro-capital-planning`, `tcro-in-the-real-world`, `tcro-dashboard-for-boards`, `esg-to-tcro`,
`hidden-wage-cost-of-invisible-risk`, `ai-in-the-built-environment`, `tcro-implementation-checklist-cfos`,
`best-digital-risk-platforms-2026`, `tcro-roi-seniors-housing`, `tcro-roi-events-entertainment`,
`tcro-roi-office-mixed-use`.

### Press release (1)
| slug | title |
|---|---|
| `pr-accelerated-commissioning-office-tower` | From 36 Months to 4 Months: Novem Digital Helps Landmark Mixed-Use Office Tower Accelerate Building Systems Startup by Nearly 89% |

### White paper (0 — pending)
The TCRO white paper is being laid out in Canva by the client and will be added when delivered.
The `/resources/` listing shows a single "Coming Soon" white-paper card as a placeholder for it.
