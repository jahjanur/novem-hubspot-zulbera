# Optional: Case Study Custom Object

The Checklist (step 5) mentions a Case Study Custom Object. The HubDB approach
above already covers the case-study use case for marketing pages. Use a CRM
Custom Object **only if** Case Studies need to associate with deals/contacts in
the CRM (e.g. tracking which prospects viewed which case study).

If you do want it, create it in **Settings → Objects → Custom Objects → Create
custom object** with these properties:

| Property name | Type | Notes |
|---|---|---|
| `title` | single-line text | Required, used as the object's Primary display label |
| `slug` | single-line text | Unique, kept in sync with the HubDB row slug |
| `client` | single-line text | |
| `industry` | dropdown select | Commercial & Mixed Use, Seniors & Wellness, Data Centers, Recreational & Venues |
| `summary` | multi-line text | |
| `body` | rich text | |
| `results` | rich text | |
| `publish_date` | date picker | |
| `seo_title` | single-line text | |
| `seo_description` | multi-line text | |
| `og_image` | single-line text (URL) | Stores File Manager URL |

Associations to enable:
- Case Study ↔ Contact (many-to-many) — "Viewed case study"
- Case Study ↔ Deal (many-to-many) — "Discussed in deal"

The current theme does **not** read from the Custom Object — it reads from the
HubDB table. If you want the marketing pages to render from the Custom Object
instead, swap `hubdb_table_rows()` in `modules/resource-card/module.html` and
`resource-detail.html` for `crm_objects("case_study", ...)`.
