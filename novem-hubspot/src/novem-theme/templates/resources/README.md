# Resource Center Sub-Templates

Each file in this directory is a HubSpot page template for a single resource
(blog post, case study, press release, or the TCRO white paper). The marketing
team creates one HubSpot Website Page per resource using these templates.

## How to activate a resource in HubSpot

1. Go to **Marketing → Website → Website Pages → Create → Website page**.
2. In the template picker, search for the template by its label (e.g. 
   `Blog: Total Cost of Risk Ownership vs Cost of Risk`).
3. Set the page URL to `/resources/<slug>/` (the slug column below).
4. Publish.

Templates have `isAvailableForNewContent: false` because each is bound to
exactly one resource — they should not be picked accidentally for unrelated
pages. If you want to reuse a layout for a different resource, duplicate the
template file, change its label, and update the title/meta/body in place.

## Template index

| Template file | URL slug | Type |
|---|---|---|
| `resources/total-cost-of-risk-ownership-white-paper.html` | `/resources/total-cost-of-risk-ownership-white-paper/` | white-paper |
| `resources/dementia-care-continuous-commissioning.html` | `/resources/dementia-care-continuous-commissioning/` | case-study |
| `resources/seniors-living-outbreak-prevention.html` | `/resources/seniors-living-outbreak-prevention/` | case-study |
| `resources/events-campus-claim-prevention.html` | `/resources/events-campus-claim-prevention/` | case-study |
| `resources/mixed-use-office-tower-commissioning.html` | `/resources/mixed-use-office-tower-commissioning/` | case-study |
| `resources/seniors-housing-insurance-savings.html` | `/resources/seniors-housing-insurance-savings/` | case-study |
| `resources/tcro-vs-cost-of-risk.html` | `/resources/tcro-vs-cost-of-risk/` | blog |
| `resources/data-governance-financial-control.html` | `/resources/data-governance-financial-control/` | blog |
| `resources/reactive-to-predictive-maintenance.html` | `/resources/reactive-to-predictive-maintenance/` | blog |
| `resources/7-criteria-digital-risk-platform.html` | `/resources/7-criteria-digital-risk-platform/` | blog |
| `resources/insurance-no-longer-fixed-line-item.html` | `/resources/insurance-no-longer-fixed-line-item/` | blog |
| `resources/make-data-pay.html` | `/resources/make-data-pay/` | blog |
| `resources/tcro-capital-planning.html` | `/resources/tcro-capital-planning/` | blog |
| `resources/tcro-in-the-real-world.html` | `/resources/tcro-in-the-real-world/` | blog |
| `resources/tcro-dashboard-for-boards.html` | `/resources/tcro-dashboard-for-boards/` | blog |
| `resources/esg-to-tcro.html` | `/resources/esg-to-tcro/` | blog |
| `resources/hidden-wage-cost-of-invisible-risk.html` | `/resources/hidden-wage-cost-of-invisible-risk/` | blog |
| `resources/ai-in-the-built-environment.html` | `/resources/ai-in-the-built-environment/` | blog |
| `resources/tcro-implementation-checklist-cfos.html` | `/resources/tcro-implementation-checklist-cfos/` | blog |
| `resources/best-digital-risk-platforms-2026.html` | `/resources/best-digital-risk-platforms-2026/` | blog |
| `resources/tcro-roi-seniors-housing.html` | `/resources/tcro-roi-seniors-housing/` | blog |
| `resources/tcro-roi-events-entertainment.html` | `/resources/tcro-roi-events-entertainment/` | blog |
| `resources/tcro-roi-office-mixed-use.html` | `/resources/tcro-roi-office-mixed-use/` | blog |
| `resources/pr-accelerated-commissioning-office-tower.html` | `/resources/pr-accelerated-commissioning-office-tower/` | press-release |

_24 templates total — generated from `.build/build_resources_v2.py`._