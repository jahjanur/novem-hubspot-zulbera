# HubSpot portal runbook — Novem Digital

Pairs every item in the launch checklist with the exact portal location and any matching theme field. Work top-to-bottom. Things marked **(code already done)** are wired in the theme — you only need to fill in IDs / paths in Design Manager → Theme settings.

> **Order matters for the code side**: do step 14 (local CLI + upload) first, then 6/8 (forms + meetings), then paste the form GUIDs and HubDB table ID into theme settings, then publish pages.

---

## 1. Account & Access
- **Settings → Account & Billing → Account Information** — confirm portal is **Novem Digital's Customer account**.
- **Settings → Account & Billing → Products & Add-ons** — confirm **Content Hub Professional or Enterprise** (required for HubDB + custom modules).
- **Settings → Users & Teams** — confirm your seat has **Super Admin** + access to: Design Manager, HubDB, Custom Objects, Forms, Workflows, Settings.

## 2. Domain & Hosting
- **Settings → Website → Domains & URLs → Connect a domain** → connect production domain.
- Verify SSL is **Active** (green check in the same panel).
- Set the primary domain (radio button).
- For any staging subdomains, **Settings → Website → Pages → System → robots.txt** → add `User-agent: * / Disallow: /` block for those hosts only.

## 3. Brand Kit
- **Settings → Account Defaults → Brand Kit** → upload light/dark logos, brand colors, default fonts.
- **Suggested colors** (already present in `css/main.css`):
  - Spring Green `#7BFAB5` · Maximum Blue `#60BCD6` · Gunmetal `#1E343F` · Cultured `#F4F6F4`
- **Suggested fonts**: Headings — Titillium Web · Body — DM Sans

## 4. Users & Permissions
- **Settings → Users & Teams → Add user** → add each teammate; assign permission sets per role.

## 5. CRM Custom Properties
- **Settings → Objects → Contacts → Manage properties → Create property** — create:
  - `page_path` (single-line text)
  - `form_name` (single-line text)
  - `campaign` (single-line text)
  - `offer` (single-line text)
  - `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term` (single-line text, all)
  - `lead_source` (dropdown — values: Demo Page, Partners Page, Careers - Express Interest) ← **the 3 forms set this automatically**
- **Settings → Objects → Custom Objects** → Case Study object → see [hubdb/case_study_custom_object.md](hubdb/case_study_custom_object.md) for the full spec. **Optional** — HubDB already covers the marketing-page need; only build the Custom Object if you want CRM associations (deals/contacts).

## 6. Email & Subscriptions
- **Settings → Marketing → Email** → sending domain → add DNS records (DKIM, SPF) at your DNS provider, then verify.
- Subscription Types: keep HubSpot defaults plus add `Resources Updates` and `Customer Communications`.
- Email footer: set the office address and unsubscribe link template.

## 7. Forms — **(code already done)**
- **Marketing → Lead Capture → Forms → Create form → Regular form** → build the three forms below. Use the exact internal field names so the form module picks them up:

### Form 1 — **Demo Form**
| Field | Type | Required |
|---|---|---|
| firstname | First name | yes |
| lastname | Last name | yes |
| email | Email | yes |
| jobtitle | Job title | yes |
| company | Company | yes |
| phone | Phone | no |
| asset_class | Dropdown (Commercial & Mixed Use / Seniors & Wellness / Data Centers / Recreational & Venues / Mixed Portfolio) | yes |
| number_of_buildings | Dropdown (1-5 / 6-20 / 21-50 / 50+) | yes |
| country | Dropdown (Canada / United States / Europe / Other) | yes |
| message | Multi-line text | no |
| lead_source | Hidden, default value `Demo Page` | yes |

Submit button label: **Request a Demo** · Spam protection: HubSpot built-in · GDPR consent: ON.

### Form 2 — **Partner Form**
firstname, lastname, email, jobtitle, company (label "Organization"), partner_type (dropdown: Insurance Carrier / MGA / Broker / Hardware & IoT / Technology & Platform / Other), country (dropdown: CA / US / UK / DE / FR / NL / Other), message. Hidden `lead_source = Partners Page`. Button: **Apply to Partner**.

### Form 3 — **Careers Form**
firstname, lastname, email, jobtitle (label "Current Title"), area_of_interest (dropdown: Engineering / Product, Data Science / AI, Sales / Business Development, Marketing, Operations, Finance, Other), linkedin_url (URL), message (required, label "Tell us about yourself"). Hidden `lead_source = Careers - Express Interest`. Button: **Express Interest**.

After each form is created, grab its **GUID** from the form's URL and paste into:
**Design Manager → `novem-theme` → Settings → Forms** →
- `Demo Form GUID`
- `Partner Form GUID`
- `Careers Form GUID`
- `HubSpot Portal ID` (your account-wide ID, top-right of the portal)

The 3 form-page templates ([get-a-demo.html](src/novem-theme/templates/get-a-demo.html), [become-a-partner.html](src/novem-theme/templates/become-a-partner.html), [careers-apply.html](src/novem-theme/templates/careers-apply.html)) already call the form module with `form_choice="demo"|"partner"|"careers"` — they will pick up the IDs automatically.

## 8. Meetings (native HubSpot)
- **Sales → Meetings → Create meeting link** → make one per path: Demo · Platform · TCRO · Partner.
- For each link: connect Google or Outlook calendar (native integration, not third party).
- Set routing rules (round-robin or by-contact-owner).
- Paste the public URLs into theme settings → Navigation → Demo CTA URL (or use the URL inside CTA-band modules per page).

## 9. Tracking (native only)
- **Settings → Tracking & Analytics → Tracking Code** → confirm the embed snippet is reported as **Active** for the production domain.
- The theme already loads `{{ standard_header_includes }}` / `{{ standard_footer_includes }}` — HubSpot injects the tracking script there. No third-party tags to add.
- Use **Reports → Analytics Tools** (Traffic Analytics, Page Performance) — skip GTM/GA4/Clarity per the brief.

## 10. Privacy & Consent
- **Settings → Privacy & Consent → Cookies** → enable banner; set regional behavior (EU, UK, Canada, US).
- Configure cookie categories (Necessary, Analytics, Functionality, Advertising).
- **Settings → Privacy & Consent → Data Retention** → set retention rules for marketable contacts.
- Paste your Privacy Policy page URL into the placeholder shown in the Get-a-Demo footer (page edit screen — there is a rich-text block under the form for the consent line).

## 11. SEO
- **Settings → Website → Pages → Templates** → default meta description and default social image.
- **Canonical URLs** → enable in Settings → Website → Pages.
- **XML sitemap** → auto-generated; verify at `/sitemap.xml` after pages are published.
- **robots.txt** → Settings → Website → Pages → System → robots.txt.

## 12. Workflows
- **Automation → Workflows → Create folder** → `Demo Requests`, `Partner Inquiries`, `Careers`, `Resource Downloads`.
- Inside each folder, create a contact-based workflow triggered by **Form submission = <the form>** with:
  - Internal notification email to sales/HR
  - Set `lifecyclestage` → MQL (or appropriate stage)
  - Add to a HubSpot static list named after the form

## 13. Files & Assets
- **Marketing → Files and Templates → Files → New folder** → `/images`, `/videos`, `/documents`, `/case-studies`.
- Upload the source assets from [src/novem-theme/images/](src/novem-theme/images/) (already copied for you from the unzipped source).

## 14. Local Code Environment Setup — **(use the project in this directory)**

```bash
brew install node                         # if not installed
npm install -g @hubspot/cli@latest

cd novem-hubspot                          # this directory
hs auth                                   # Personal Access Key from Settings → Integrations → Private Apps → Create
                                          # name it 'Novem CLI', scopes: cms.* + crm.* + hubdb
hs project upload                         # uploads /src to Design Manager
```

After upload:
1. **Design Manager → `novem-theme` → Settings** → fill in:
   - Brand → logo, phone, email
   - Header navigation → menu items
   - Forms → portal ID + 3 form GUIDs
   - HubDB → resources table ID
   - Footer → description + legal line
2. **Marketing → Files and Templates → HubDB → Create table** → name `resources`, columns per [hubdb/resources_schema.md](hubdb/resources_schema.md). Toggle **Allow public API access** ON and **Use for dynamic pages** ON.
3. **Content → Website Pages → Create new page** → for each page below pick the matching template and publish to the listed path:

| Path | Template | Notes |
|---|---|---|
| `/` | `home.html` | Home |
| `/how-it-works/` | `platform.html` | |
| `/industries/` | `industries.html` | |
| `/tcro/` | `tcro.html` | |
| `/partners/` | `partners.html` | |
| `/resources/` | `resources.html` | Listing — HubDB-driven |
| `/about/` | `about.html` | |
| `/careers/` | `careers.html` | |
| `/get-a-demo/` | `get-a-demo.html` | Form page |
| `/become-a-partner/` | `become-a-partner.html` | Form page |
| `/careers/apply/` | `careers-apply.html` | Form page |
| `/resources/<dynamic>` | `resource-detail.html` | **Page Settings → Advanced Options → Dynamic Pages** → select `resources` HubDB table |

4. **Settings → Website → Pages → System Pages** → set the 404 page to **`error_page.html`** (under `templates/system/`).

5. Publish, smoke-test the Demo form (it should create a contact), and you're live.
