# Novem Digital — Site Map (source for HubSpot migration)

Source: `unzipped/` (16 unzipped HTML pages, self-contained with inline CSS).

## Brand tokens (from homepage `:root`)
**Dark (default)** — `--green #7BFAB5`, `--blue #60BCD6`, `--gun #1E343F`, `--gun-mid #243C48`, `--gun-dark #111A1F`, `--text #E8F4F0`, `--muted #8BBCCA`, `--bg #111A1F`, `--surf #1E343F`, `--border #2C4250`.
**Light** — `--green #60BCD6`, `--blue #2A7FA0`, `--text #1E343F`, `--bg #F4F6F4`, `--surf #FFFFFF`.
**Fonts** — Headings: Titillium Web (300/400/600/700 + italic). Body: DM Sans (variable 300–700).
**Radius/Motion** — pill `--r 9999px`, ease `200ms cubic-bezier(.16,1,.3,1)`.

## Global navigation
Logo → `/` · Platform → `/how-it-works/` · Industries → `/industries/` · TCRO → `/tcro/` · Partners → `/partners/` · Resources → `/resources/` · About → `/about/` · Login → (placeholder `#`) · Get a Demo → `/get-a-demo/`.

## Footer
Industries, Platform, Resources, About, Data Sources, Get in Touch columns. Phone `+1 833 668 3647`. Email `connect@novemdigital.com`. LinkedIn `https://www.linkedin.com/company/novem-digital/`.

## Pages and slugs
| # | Slug | Title | Notes |
|---|------|-------|-------|
| 01 | `/` | Novem Digital — Digital Risk Platform | Hero, proof, TCRO intro, partners, FAQ, CTA |
| 02 | `/how-it-works/` | Platform | "The warning…" hero, FAQ |
| 03 | `/industries/` | Industries | 4 segments (Commercial, Seniors, Data Centers, Recreational) |
| 04 | `/tcro/` | TCRO | Calculator anchor `#calculator`, methodology |
| 05 | `/partners/` | Partner Ecosystem | Links to `/become-a-partner/` |
| 06 | `/resources/` | Resources | Filterable card grid (data-type) |
| 06a | `/resources/bc-events/` | BC Events Campus case study | |
| 06b | `/resources/bethany-riverview/` | Bethany Riverview case study | |
| 06c | `/resources/lrhg/` | LRHG Pioneer Lodge case study | |
| 06d | `/resources/telus-garden/` | LEED Platinum tower case study | |
| 06e | `/resources/case-study-sample/` | Mixed-use portfolio sample | Duplicate of #13 |
| 06f | `/resources/blog-sample/` | Predictive vs Preventive blog | Duplicate of #15 |
| 06g | `/resources/whitepaper-sample/` | Predictive Ops Imperative WP | Duplicate of #14 |
| 06h | `/resources/press-release-sample/` | Whetsel PR | Duplicate of #16 |
| 06i | `/resources/pr-whetsel/` | Whetsel PR | Duplicate of 06h |
| 06j | `/resources/pr-jay/` | Jay PR | |
| 07 | `/about/` | About | Team + advisory board |
| 08 | `/careers/` | Careers | Open roles section `#open-roles` |
| 08b | `/careers/apply/` | Express Interest | Duplicate of #12 |
| 09 | (system 404) | Page Not Found | Wire to HubSpot system 404 |
| 10 | `/get-a-demo/` | Get a Demo | **Form: demoForm** |
| 11 | `/become-a-partner/` | Become a Partner | **Form: partnerForm** |
| 12 | `/careers/apply/` | Express Interest | **Form: careersForm** |
| 13 | (template) | Case Study | Source for HubDB-backed CS template |
| 14 | (template) | Whitepaper | Source for WP template |
| 15 | (template) | Blog post | Source for blog template |
| 16 | (template) | Press release | Source for PR template |

## Forms (3 to create in HubSpot, native)

### Demo Form (`/get-a-demo/`) — hidden `lead_source="Demo Page"`
firstname* · lastname* · email* · jobtitle* · company* · phone · asset_class* (Commercial & Mixed Use / Seniors & Wellness / Data Centers / Recreational & Venues / Mixed Portfolio) · number_of_buildings* (1–5 / 6–20 / 21–50 / 50+) · country* (Canada / United States / Europe / Other) · message · **Submit: Request a Demo**

### Partner Form (`/become-a-partner/`) — hidden `lead_source="Partners Page"`
firstname* · lastname* · email* · jobtitle* · company* (Organization) · partner_type* (Insurance Carrier / MGA / Broker / Hardware & IoT / Technology & Platform / Other) · country* (Canada / United States / United Kingdom / Germany / France / Netherlands / Other) · message · **Submit: Apply to Partner**

### Careers Form (`/careers/apply/`) — hidden `lead_source="Careers - Express Interest"`
firstname* · lastname* · email* · jobtitle* (Current Title) · area_of_interest* (Engineering / Product, Data Science / AI, Sales / BD, Marketing, Operations, Finance, Other) · linkedin_url · message* · **Submit: Express Interest**

## CTA targets — placeholders to fix
- Industries final CTA `Get a Demo` → `#` → must be `/get-a-demo/`
- TCRO `Download the Framework` → `#` → needs a real asset URL
- Templates 13/14/15/16 + matching 06e/06f/06g/06h/06i `Get a Demo` → `#` → `/get-a-demo/`
- Header `Login` → `#` (decide: real URL or remove)
- Get-a-Demo "Privacy Policy" link → `#`
- Footer Industries column anchors `#segments` (broken) → `/industries/#commercial-mixed-use` etc.

## Slug normalization
Homepage nav uses no trailing slash (`/industries`); 404 page uses trailing (`/industries/`). Pick one (recommend trailing slash to match HubSpot convention).

## Duplicates to resolve
- Page 13 ≡ Page 06e (case study sample)
- Page 14 ≡ Page 06g (whitepaper sample)
- Page 15 ≡ Page 06f (blog sample)
- Page 16 ≡ Page 06h ≡ Page 06i (Whetsel PR)
- Page 08b ≡ Page 12 (careers apply)

Recommended: pages 13–16 become **template files only** (used by HubDB-backed dynamic pages); the published URLs live under `/resources/*` and `/careers/apply/`.
