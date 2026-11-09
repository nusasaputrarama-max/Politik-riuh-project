# Deployment Feasibility — POLITIK RIUH Token Site

- **Date:** 2026-11-09
- **Scope:** `apps/token-site/` only
- **Status:** FEASIBLE AS A STATIC PREVIEW / NOT AUTHORIZED TO DEPLOY
- **Repository:** `nusasaputrarama-max/Politik-riuh-project`
- **Branch for this proposal:** `audit/whitelist-and-token-site-review-2026-11-09`
- **Explicit exclusion:** `apps/web/` (the separate news portal) is not part of this deployment.

## 1. Executive decision

The current token site is a static HTML/CSS/JavaScript website with six HTML routes, one shared stylesheet, and one small mobile-navigation script. Its README reports zero package dependencies, no build step, no server, no environment variables, no forms, no analytics, and no runtime external requests. The owner-specific GitHub repository URL has been removed from all six public pages to preserve the anonymous-team identity.

**Recommended hosting candidate: GitHub Pages using a custom GitHub Actions workflow that uploads only `apps/token-site/`.**

This is a technically suitable path for a static project preview. It is not a whitelist backend, a wallet application, or a token launch. GitHub Pages cannot provide the server-side registration, task verification, private applicant data, or admin workflow required by the future whitelist.

No Pages setting, DNS record, repository deployment setting, workflow, or live artifact was changed while preparing this proposal.

## 2. Current site inventory and deployment boundary

Expected upload root:

```text
apps/token-site/
  index.html
  about.html
  token.html
  launch.html
  transparency.html
  roadmap.html
  styles.css
  main.js
  evidence/
  README.md
```

The Pages artifact must be built from this directory only. Do not upload the repository root, `apps/`, or `apps/web/`.

The site uses relative local links (for example `about.html` and `styles.css`), which is appropriate for a project Pages URL with a repository path prefix. Verify this against the deployed base path rather than assuming local-root behavior is sufficient.

The site must remain informational until separately approved. It must not contain:
- Applicant email addresses, wallet addresses, private contact data, or other personal data.
- API keys, credentials, signing material, private keys, seed phrases, or production secrets.
- A fake whitelist form, placeholder registration CTA, fabricated social links, fake metrics, or an unverified launch countdown.
- Wallet connection, signing, transactions, minting, purchase, or fund movement.

## 3. Recommended GitHub Pages workflow

Use GitHub Actions as the Pages publishing source. A branch-folder publishing source is not a fit for this repository layout because the site lives in `apps/token-site/`, not at the repository root or a root `docs/` directory. A custom workflow can package the selected subdirectory as the Pages artifact.

Recommended stages:

### A. Pull-request validation — no deployment

Trigger on pull requests that change:
- `apps/token-site/**`
- The token-site validation workflow itself.

Run:
1. HTML parsing for all six pages.
2. Exactly one `h1` per page and required landmarks.
3. Internal `href` and `src` target resolution.
4. JavaScript syntax check: `node --check apps/token-site/main.js`.
5. Source scan for accidental forms, fetch/XHR, local storage, analytics, wallet SDKs, signing/transaction calls, HTTP mixed content, secrets, and unsupported token facts.
6. Mobile/desktop screenshot generation and review.
7. WCAG AA contrast and keyboard/focus checks.

The PR workflow must not request Pages deployment permissions and must not publish an artifact.

### B. First deployment — manual and owner-approved

After the owner approves the final site content and deployment plan:
1. An authorized repository administrator enables GitHub Pages with **GitHub Actions** as the source.
2. A manually dispatched workflow checks out the approved `main` commit.
3. It runs the same validation suite.
4. It uploads only `apps/token-site/` using `actions/upload-pages-artifact` with `path: apps/token-site`.
5. A separate deploy job depends on the validation/upload job and uses `actions/deploy-pages`.
6. The deploy job has only the required `pages: write` and `id-token: write` permissions, plus `contents: read` where needed.
7. The deployment uses the `github-pages` environment. Add a branch restriction and required reviewer if those environment protections are available for this repository/plan.
8. Pin every third-party GitHub Action to a reviewed immutable commit SHA at implementation time; do not rely on floating tags in the final production workflow.

Suggested action roles:
- `actions/checkout`: check out the approved commit.
- `actions/configure-pages`: configure Pages metadata.
- `actions/upload-pages-artifact`: upload the static directory.
- `actions/deploy-pages`: deploy the uploaded artifact.

Do not enable automatic deployment on every push until the owner explicitly approves that operating model. A later push-to-main deployment can be considered only after the first deployment is verified and the Pages environment is protected.

## 4. URL, path, and HTTPS expectations

If GitHub Pages is enabled as a project site, the expected default URL pattern is:

```text
https://nusasaputrarama-max.github.io/Politik-riuh-project/
```

**This is a URL pattern only. It is not configured, published, reachable, or verified at the time of this document.**

The workflow output and repository Pages settings must provide the actual URL. Do not claim a URL is live based on the expected pattern.

GitHub Pages supports HTTPS for `github.io` sites and supports HTTPS enforcement. After deployment, verify:
- HTTPS certificate is valid.
- HTTP requests redirect to HTTPS if enforcement is enabled.
- The base URL and repository path prefix resolve correctly.
- All six HTML routes load.
- `styles.css` and `main.js` load with successful responses.
- There is no mixed-content request.
- No route leaks or accidentally serves files from `apps/web/`.

### Custom domain — optional later phase

A custom domain is not required for the first preview. If selected later:
1. The owner must control the domain.
2. Verify domain ownership in GitHub before attaching it to Pages.
3. Configure the correct DNS records with the domain provider.
4. Configure the custom domain in the repository Pages settings/API.
5. Wait for certificate provisioning and then enforce HTTPS.
6. Re-run the complete external route/asset check.

For a custom Actions workflow, do not assume that adding a `CNAME` file alone configures the domain; the custom domain must also be configured in Pages settings/API.

## 5. Public exposure and privacy

GitHub Pages sites are public by default. Treat every uploaded file as public, including when the repository visibility or plan differs from the expected configuration.

The current static site is suitable for public preview only after factual and language corrections. Do not use Pages to collect whitelist applications. A future whitelist requires a separately reviewed backend and storage provider with:
- Server-side authorization and admin roles.
- Email and public Solana wallet address validation.
- Task-verification capability boundaries (verified vs self-attested vs manual review).
- Rate limits, duplicate/abuse controls, and audit trail.
- Data minimization, retention schedule, deletion process, backup/restore, and breach response.
- No wallet connection or signing requirement for the Phase 1 registration form.

## 6. Pre-deployment acceptance gates

Do not deploy until all gates pass:

| Gate | Required evidence |
|---|---|
| Owner content approval | Approved Indonesian copy, POLITIK RIUH presents REFORMASI identity, risk disclosures |
| Facts discipline | Token remains marked not launched; no invented supply, mint, venue, date, holders, volume, treasury, partnership, or return claims |
| Language/accessibility | All six pages use `lang="id"`; natural Indonesian copy; keyboard/focus, contrast, reduced motion, semantic landmarks |
| Route integrity | All six routes and all internal CSS/JS links pass local smoke tests under the project path prefix |
| Scope isolation | Workflow artifact contains only `apps/token-site/`; no `apps/web/` files |
| Security/privacy | No secrets, applicant PII, wallet signing, transactions, forms, analytics, or external runtime requests |
| Reproducibility | Exact commit, workflow file, action SHAs, commands, exit codes, and test logs recorded |
| External verification | HTTPS certificate, redirect behavior, six routes, CSS/JS assets, console/network errors, and mobile/desktop screenshots checked from an external session |
| Rollback | Last known-good commit/artifact identified and rollback operator/procedure recorded |

A deployment is **VERIFIED** only after the external HTTPS checks succeed against the actual workflow output URL. Local preview, a GitHub repository link, a Pages URL pattern, or a green build alone is not deployment verification.

## 7. Rollback

For a static site:
1. Keep the last known-good deployment commit and workflow artifact identifier.
2. Revert the approved content/deployment commit.
3. Re-run the approved Pages workflow against the rollback commit.
4. Re-check all six routes and HTTPS externally.
5. If the site must be removed immediately, an authorized repository administrator can disable/unpublish Pages and confirm the old URL no longer serves the site.

Do not delete repository source or change unrelated `apps/web/` deployment settings as a rollback shortcut.

## 8. Current status

| Area | Status |
|---|---|
| Static source exists | VERIFIED in GitHub source |
| Six-page route inventory | VERIFIED in source |
| Local smoke/accessibility evidence | REPORTED in site README; not independently rerun in this proposal |
| GitHub Actions workflow | NOT PRESENT / no observed workflow runs |
| GitHub Pages configuration | NOT VERIFIED / not changed |
| Public HTTPS URL | NOT VERIFIED |
| Custom domain | NOT selected |
| Whitelist backend | NOT IMPLEMENTED |
| Token launch / mint | NOT LAUNCHED |

**Decision:** GitHub Pages is the recommended low-complexity host for an approved static preview of `apps/token-site/` only. It is not approval to publish, does not provide a whitelist backend, and does not change any token-launch authorization.

## 9. Primary references

- GitHub Docs — Using custom workflows with GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- GitHub Docs — Creating a GitHub Pages site: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
- GitHub Docs — Configuring a publishing source: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- GitHub Docs — Securing your GitHub Pages site with HTTPS: https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https
- GitHub Docs — Verifying a custom domain: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages
