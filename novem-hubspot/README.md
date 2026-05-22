# novem-hubspot

HubSpot CMS theme for Novem Digital. Migrates 16 static HTML pages into a HubSpot Content Hub project with reusable modules, native HubSpot Forms, and a HubDB-driven Resources section.

## What's here

```
novem-hubspot/
├── hsproject.json                          ← HubSpot project descriptor
├── HUBSPOT_RUNBOOK.md                      ← Portal-side checklist (items 1–13)
├── hubdb/
│   ├── resources_schema.md                 ← HubDB table reference
│   ├── resources_schema.csv                ← Column listing
│   └── case_study_custom_object.md         ← Optional CRM Custom Object spec
└── src/novem-theme/
    ├── theme.json                          ← Theme manifest
    ├── fields.json                         ← Theme-level settings (brand, nav, forms, HubDB, footer)
    ├── css/main.css                        ← All shared styles, brand tokens, dark/light theme
    ├── js/main.js                          ← Theme toggle, mobile drawer, scroll, reveal, filter
    ├── images/                             ← Logo, banner, team photos (copied from source)
    ├── templates/
    │   ├── layouts/base.html               ← Base layout (extends-able)
    │   ├── partials/header.html            ← Top nav + mobile drawer
    │   ├── partials/footer.html            ← Footer (7 columns)
    │   ├── system/error_page.html          ← 404
    │   ├── home.html                       ← /
    │   ├── platform.html                   ← /how-it-works/
    │   ├── industries.html                 ← /industries/
    │   ├── tcro.html                       ← /tcro/
    │   ├── partners.html                   ← /partners/
    │   ├── about.html                      ← /about/
    │   ├── careers.html                    ← /careers/
    │   ├── resources.html                  ← /resources/  (HubDB-driven listing)
    │   ├── resource-detail.html            ← /resources/<slug>  (dynamic HubDB page)
    │   ├── resource-case-study.html        ← static sample (optional, not bound to HubDB)
    │   ├── resource-whitepaper.html        ← static sample (optional)
    │   ├── resource-blog.html              ← static sample (optional)
    │   ├── resource-press-release.html     ← static sample (optional)
    │   ├── get-a-demo.html                 ← /get-a-demo/  → Demo Form
    │   ├── become-a-partner.html           ← /become-a-partner/  → Partner Form
    │   └── careers-apply.html              ← /careers/apply/  → Careers Form
    └── modules/
        ├── hero.module/                    ← Hero with stat sidebar
        ├── cta-band.module/                ← Bottom CTA
        ├── faq.module/                     ← Accordion FAQ
        ├── segment-card.module/            ← 4-up industries grid
        ├── stat-block.module/              ← 4-up stats strip
        ├── resource-card.module/           ← HubDB cards (any type, with filter)
        └── hubspot-form.module/            ← Native HubSpot Form embed
```

## Quick start

```bash
# one-time tooling
brew install node
npm install -g @hubspot/cli@latest

# auth (interactive — needs a Personal Access Key from
#   Settings → Integrations → Private Apps → Create
#   scopes: cms.* + crm.* + hubdb)
cd novem-hubspot
hs auth

# upload theme to your portal
hs project upload

# (optional) watch + auto-upload on save
hs watch src/novem-theme
```

After upload, follow [HUBSPOT_RUNBOOK.md](HUBSPOT_RUNBOOK.md) for the portal-side steps (forms, meetings, HubDB table, page creation).

## How content flows

| Layer | Where it lives | Who edits |
|---|---|---|
| Brand tokens (colors, fonts) | `css/main.css` + `theme.json` | Developer |
| Header nav / footer / logo | `partials/` + `theme.fields.json` brand+navigation+footer groups | Marketing in Design Manager → Theme settings |
| Page hero text, CTAs, sections | Theme modules called from each page template | Marketing in Page Editor |
| Resources (case studies, etc.) | `resources` HubDB table | Anyone with HubDB access |
| Form submissions | 3 native HubSpot Forms | Marketing in Forms tool |

## Pages NOT in the theme that need creating

- Privacy Policy and Cookie Policy pages — referenced by the Get-a-Demo footer + cookie banner; create as standard HubSpot pages.
- Terms of Service — if applicable.
- Login destination — the header `Login` link points to `#` by default; set the real URL in **Theme settings → Navigation → Login URL** or remove the link from `partials/header.html`.

## Known placeholders fixed during migration

- Every `href="#"` in source page bodies was rewritten to `/get-a-demo/` during template generation (see [build_templates.sh](../build_templates.sh)). Review each template and adjust if a particular CTA should point somewhere else (e.g. TCRO's "Download the Framework" should point to the actual PDF in Files once uploaded).
- Footer Industries column anchors now point to `/industries/#commercial-mixed-use` etc. — make sure those anchor IDs exist in the Industries page sections (they're set via the segment-card module's "Anchor slug" field).

## Source material

The original 16 static pages are unzipped in [../unzipped/](../unzipped/). The site map and content inventory is in [../SITEMAP.md](../SITEMAP.md).
