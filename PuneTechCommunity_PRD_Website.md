# Product Requirements Document
## Pune Tech Community — Website

**Version:** 1.0
**Date:** July 18, 2026
**Owner:** [Your name]
**Status:** Draft
**Related:** Companion to Mobile App PRDs (Phase 1 & Phase 2)

---

## 1. Overview

### 1.1 Background
Pune Tech Community currently has no owned web presence — discovery and engagement happen entirely on third-party platforms (Meetup, LinkedIn, YouTube). A mobile app is in progress for members who are already engaged, but a public website is needed as the front door for new discovery, SEO, sponsor credibility, and cross-promotion into the app.

### 1.2 Problem Statement
Prospective members and sponsors searching for "Pune tech community," "Azure meetup Pune," etc. have no branded destination — they land on Meetup or LinkedIn, which are generic, ad-cluttered, and don't reflect the community's identity. There's also no single place to point sponsors, speakers, or press for credible information about the community.

### 1.3 Goal
Launch a public, SEO-friendly website that serves as the community's front door: showcases events (upcoming and past), speakers, and video content; builds credibility with sponsors; and funnels visitors into event RSVPs and app downloads.

### 1.4 Success Metrics
| Metric | Target (90 days post-launch) |
|---|---|
| Organic search sessions/month | 500+ |
| Event page → RSVP click-through rate | 15%+ |
| App download clicks from website | 200+/month |
| Avg. session duration | 90+ seconds |
| Sponsor inquiry form submissions | 3+/month |
| CFP ("Submit a Talk") form submissions | 5+/month |

---

## 2. Scope

### 2.1 In Scope (v1)
1. Homepage
2. Events Listing Page (upcoming + past)
3. Event Detail Page
4. Speaker Directory + Speaker Profile pages
5. Video/Content Library
6. About / Community page (incl. organizer team, CFP callout)
7. Sponsor page (tiers, benefits, contact form)
8. Global navigation, footer, app cross-promotion (App Store / Google Play badges)
9. Basic CMS so organizers can add/edit events, speakers, and sponsors without a developer
10. Basic SEO setup (metadata, sitemap, structured data for events)

### 2.2 Out of Scope (v1)
- User accounts / login on the website (RSVP and check-in remain app/Meetup-driven, or a lightweight guest-RSVP form only — see open questions)
- Community feed, DMs, groups (these live in the app per Phase 2)
- Payment processing (no paid tickets in v1)
- Multi-language support
- Blog/articles section (may be a fast-follow)

---

## 3. Users & Personas

| Persona | Primary Goal on Site |
|---|---|
| **Prospective member** (found via Google/social) | Understand what the community is, find next event, RSVP or download app |
| **Existing member** | Quick lookup of event details, rewatch a past talk, share a link with a colleague |
| **Speaker (prospective)** | Learn about the community, submit a talk via CFP |
| **Sponsor (prospective)** | Evaluate credibility (past events, audience size), see sponsorship tiers, make contact |
| **Organizer** | Publish/edit events, speakers, sponsors via CMS without needing a developer |
| **Press/partner** | Quick facts: what the community is, who runs it, scale (members, events) |

---

## 4. Features & Requirements

### 4.1 Homepage
**Requirements:**
- FR1.1: Hero section with headline, subtext, primary CTA ("See upcoming events") and secondary CTA ("Join the community" → links to Meetup/app)
- FR1.2: Stats strip (member count, events hosted, speakers featured) — pulled from CMS/manually updated
- FR1.3: Upcoming Events preview (next 3 events) with RSVP CTA per card
- FR1.4: Featured Talks preview (3 recent/popular videos)
- FR1.5: Sponsor logo strip
- FR1.6: Community highlights (photos/quotes carousel)
- FR1.7: Footer with social links (Meetup, LinkedIn, YouTube) and app store badges

**Acceptance criteria:** A first-time visitor can find the next event and RSVP or open the app within 2 clicks of landing.

---

### 4.2 Events Listing Page
**Requirements:**
- FR2.1: Toggle between Upcoming and Past events
- FR2.2: Filter by topic tag (Azure, AI, Power Platform, M365) and format (in-person/virtual)
- FR2.3: Search by keyword
- FR2.4: Each card: banner thumbnail, title, date, format badge, RSVP button (upcoming) or "Watch Recording" link (past)
- FR2.5: Pagination or infinite scroll for past events archive

**Acceptance criteria:** Visitor can filter to a specific topic and find a relevant event in under 10 seconds.

---

### 4.3 Event Detail Page
**Requirements:**
- FR3.1: Banner, title, date/time, location or virtual join info, full description
- FR3.2: Agenda/track schedule with speaker names and time slots
- FR3.3: Speaker cards linking to Speaker Profile
- FR3.4: Sponsor section grouped by tier
- FR3.5: Sticky "Register" CTA — links to Meetup event page (v1) or opens guest RSVP form (see open question 8.1)
- FR3.6: Social share buttons (LinkedIn, X, WhatsApp, copy link)
- FR3.7: Structured data (schema.org Event markup) for SEO/Google Events surfacing

**Acceptance criteria:** Event pages are indexable and eligible for Google's event rich results.

---

### 4.4 Speaker Directory & Profile
**Requirements:**
- FR4.1: Directory grid: photo, name, title/company, filterable by topic
- FR4.2: Speaker profile: photo, bio, social links, list of past talks linking to video library entries
- FR4.3: CMS support for organizers to add a new speaker profile tied to an event submission

**Acceptance criteria:** Every past speaker has a profile page reachable from both the directory and their session's event page.

---

### 4.5 Video/Content Library
**Requirements:**
- FR5.1: Grid of past session recordings pulled from the PuneTechCommunity YouTube channel (via YouTube Data API or manual CMS entry)
- FR5.2: Filter by topic and speaker
- FR5.3: Embedded playback (YouTube embed) without leaving the site
- FR5.4: Each video links back to its Event Detail and Speaker Profile pages

**Acceptance criteria:** New videos published to YouTube appear on the site within 24 hours (automated) or same-day (manual CMS entry, v1 fallback).

---

### 4.6 About / Community Page
**Requirements:**
- FR6.1: Mission statement and community story/history
- FR6.2: Organizer team section (photos, names, roles, social links)
- FR6.3: "Call for Speakers" callout with CTA linking to a CFP form (Typeform/Google Form in v1, or in-app CFP once Phase 2 mobile ships)
- FR6.4: "Become a Sponsor" callout linking to Sponsor page

**Acceptance criteria:** Page clearly communicates who runs the community and two clear next actions (speak, sponsor).

---

### 4.7 Sponsor Page
**Requirements:**
- FR7.1: Sponsorship tiers (Platinum/Gold/Silver) with a benefits comparison table (logo placement, booth space, mentions, etc.)
- FR7.2: Current and past sponsor logo wall
- FR7.3: Contact form for sponsorship inquiries (routes to organizer email)

**Acceptance criteria:** A prospective sponsor can understand tier benefits and submit an inquiry without needing to email directly.

---

### 4.8 Global Navigation & Footer
**Requirements:**
- FR8.1: Sticky top nav: logo, Events / Speakers / Videos / About / Sponsors, prominent "Join / RSVP" button
- FR8.2: App Store and Google Play badges in nav or footer (activates once mobile app is live)
- FR8.3: Footer: social links, contact email, copyright, sitemap links

---

### 4.9 CMS / Content Management
**Requirements:**
- FR9.1: Organizers can create/edit/publish Events, Speakers, and Sponsors without developer involvement (headless CMS such as Sanity/Contentful/Notion-as-CMS, or a simple admin panel)
- FR9.2: Draft/publish states for events (so upcoming events can be prepped before going live)
- FR9.3: Image upload for banners, speaker photos, sponsor logos
- FR9.4: Role-based CMS access limited to organizer team

**Acceptance criteria:** An organizer can publish a new event (with speaker and sponsor assignments) without writing code or contacting a developer.

---

### 4.10 SEO & Analytics
**Requirements:**
- FR10.1: Meta titles/descriptions per page, Open Graph tags for social sharing previews
- FR10.2: XML sitemap and robots.txt
- FR10.3: schema.org structured data for Events and Person (speakers)
- FR10.4: Google Analytics (or privacy-friendly alternative) integrated
- FR10.5: Fast page load — target Lighthouse performance score 85+

---

## 5. User Flows

1. **Discover → RSVP:** Google search "Azure meetup Pune" → land on Event Detail (SEO) → Register CTA → Meetup/guest RSVP
2. **Explore content:** Homepage → Video Library → filter by "AI" → watch embedded talk → click through to speaker profile
3. **Speaker interest:** About page → "Submit a Talk" CTA → CFP form
4. **Sponsor interest:** Homepage sponsor strip → Sponsor page → compare tiers → submit inquiry form
5. **Cross-promotion to app:** Any page footer/nav → App Store/Google Play badge → app install

---

## 6. Non-Functional Requirements

- **Responsive design:** Fully responsive across desktop, tablet, and mobile breakpoints
- **Performance:** Lighthouse performance score 85+, LCP < 2.5s
- **Accessibility:** WCAG AA compliance (contrast, alt text, keyboard navigation)
- **SEO:** Server-rendered or statically generated pages (e.g., Next.js) for crawlability — avoid client-only rendering for core content pages
- **Hosting:** Scalable static/JAMstack hosting (Vercel/Netlify) suitable for traffic spikes around event announcements
- **Brand consistency:** Shares design system (colors, type, components) with the mobile app

---

## 7. Dependencies

- YouTube Data API (video library sync)
- CMS platform (Sanity, Contentful, Notion-as-CMS, or custom admin)
- Meetup API or manual sync (if RSVP continues to route through Meetup in v1)
- Form/email service for CFP and sponsor inquiry forms (e.g., Formspree, native CMS forms)
- Analytics tooling
- Shared design tokens/assets from the mobile app design system (Claude Design output)

---

## 8. Open Questions

1. **RSVP handling:** Does "Register" on the website redirect to Meetup (fastest to ship), or should we build a native guest-RSVP form on the site (no login required) to reduce Meetup dependency sooner?
2. Should the CFP form live only on the website in v1, or do we wait and route it to the in-app CFP once mobile Phase 2 ships?
3. Who owns ongoing CMS content updates (organizer team bandwidth)?
4. Do we need a blog/resources section for SEO long-tail content (e.g., "Azure AI trends"), or is that a later phase?
5. Should sponsor inquiry submissions integrate with a CRM, or is a routed email sufficient for current volume?

---

## 9. Milestones (Indicative)

| Milestone | Target |
|---|---|
| Website design finalized (Claude Design) | Week 2 |
| CMS/backend setup + content model | Week 4 |
| Homepage, Events Listing, Event Detail built | Week 6 |
| Speaker Directory, Video Library built | Week 8 |
| About, Sponsor pages + forms built | Week 9 |
| SEO setup, analytics, QA | Week 10 |
| Launch | Week 11 |

---

## 10. Relationship to Mobile App

The website and app share the same content backbone (events, speakers, sponsors) where feasible — ideally a single CMS/backend feeds both, avoiding duplicate data entry for organizers. The website is optimized for **discovery and credibility** (SEO, sponsor-facing, no-login browsing); the app is optimized for **engaged-member utility** (RSVP, check-in, networking, community feed). Cross-promotion should run in both directions: website → app download, app → shareable event links for social/website reach.
