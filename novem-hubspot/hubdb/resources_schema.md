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

## Seed rows to migrate from the source site

| slug | type | title | source file |
|---|---|---|---|
| `bc-events` | case-study | $5M Claim Prevented. $400K Gas Leak Found. Insurance Held Flat. | `06-Resources/06-Resources/bc-events/index.html` |
| `bethany-riverview` | case-study | Brand New Building. Hidden Failures. $93K Saved. | `06-Resources/06-Resources/bethany-riverview/index.html` |
| `lrhg` | case-study | Seven Years of Outbreaks. Stopped. | `06-Resources/06-Resources/lrhg/index.html` |
| `telus-garden` | case-study | 900 Issues. 4 Months. $10.1M Saved. | `06-Resources/06-Resources/telus-garden/index.html` |
| `case-study-sample` | case-study | Predictive Operations Across a Mixed-Use Portfolio | `06-Resources/06-Resources/case-study-sample/index.html` |
| `whitepaper-sample` | white-paper | The Predictive Operations Imperative | `06-Resources/06-Resources/whitepaper-sample/index.html` |
| `blog-sample` | blog | Why Predictive Operations Beat Preventive Maintenance | `06-Resources/06-Resources/blog-sample/index.html` |
| `press-release-sample` | press-release | Novem Digital Appoints Dr. Robert Whetsel as CTO | `06-Resources/06-Resources/press-release-sample/index.html` |
| `pr-whetsel` | press-release | Novem Digital Appoints Dr. Robert Whetsel as CTO | `06-Resources/06-Resources/pr-whetsel/index.html` |
| `pr-jay` | press-release | Novem Digital Appoints Grant R. Jay as CRO | `06-Resources/06-Resources/pr-jay/index.html` |

(Note: `case-study-sample`/`pr-whetsel` are duplicates of other rows — decide whether to publish or skip.)
