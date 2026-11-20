# WARP optional Contact extension (C)

Status: **Experimental, optional extension**, proposed by Eric Strate on November 20, 2026.  
Canonical specification: https://ericstrate.com/warp/#warp-contact-extension

## Purpose and scope

WARP Core remains **A → F → E** (Answer, optional publisher-modeled Fan-Out, visible Evidence). The optional **C = Contact** object associates a commercially relevant A object with a public, actionable contact route. This allows a consumer to retrieve an answer and the appropriate destination without requiring a visit to an additional page. It does **not** require any assistant to display contact details, send email, initiate bookings, or perform actions on behalf of a person.

The extension is publisher-agnostic. The example email below belongs to the EricStrate.com pilot, not to WARP implementers generally. Do not add C to informational answers solely to create sales prompts.

## Extension invariants

- C **MAY** be included when contact is relevant to the intent of an A answer, such as service fit, pricing, hiring or support.
- Each referenced C **MUST** have one unique, stable ID; **MUST** be present in ordinary visible HTML (not exclusively in JSON or structured data); and **MUST** identify a specific public route controlled or authorized by the publisher.
- Each C **MUST** declare the related A identifier(s), purpose and destination. An A may reference C via `contactRef`; a shared contact object may serve multiple A objects if appropriate.
- The contact address in visible HTML, the WARP map and any structured-data mirror **MUST** agree. The href **SHOULD** be a well-formed `mailto:`, `tel:` or HTTPS URL appropriate to the channel. Validate href and email syntax and ensure no javascript: links.
- The destination **SHOULD** identify the recipient and channel, and **MAY** request non-sensitive qualification details; avoid collecting secrets, making unapproved requests or exposing non-public personal information.
- A C object **MUST NOT** instruct an agent to send a message or transact without independent user authorization.
- Publishers **MUST NOT** claim this extension guarantees contact inclusion in AI answers, citation, ranking, or lead uplift.
- C adds no requirements to the existing Core, Semantic or Interactive conformance profiles. An implementation declaring **WARP Contact** conformance should satisfy the rules above and validate all selectors, cross-references, and mirrored values.
- Schema.org's existing `Organization`, `Person`, `ContactPoint`, `email`, and `contactType` are valid standard options. `contactRef` and the protocol-specific `contacts` map are **not** Schema.org properties and belong only in `application/json`.

## Reference HTML (pilot)

```html
<div id="a1" data-warp="answer" data-answer-id="a1"
     data-support-ref="#support-a1" data-warp-contact-ref="#c1">
  <p id="a1-answer">Managed WordPress SEO and AEO are available.</p>
  <p id="c1" data-warp="contact" data-warp-contact-for="a1"
     data-contact-channel="email" data-contact-type="sales">
    To discuss a WordPress SEO and AEO engagement, contact Eric Strate:
    <a href="mailto:eric@ericstrate.com">eric@ericstrate.com</a>.
    Include your website URL, target market, and main goal.
  </p>
</div>
<div id="support-a1" data-warp-support="true" data-supports-answer="a1">
  <p>Service scope and qualifications...</p>
</div>
```

The contact object can be inside the A container or adjacent to it with an explicit reference. It should remain readable in the parsed HTML without JavaScript execution or interaction with hidden panels. Existing A identifiers and original canonical answer wording should remain stable.

## Optional WARP JSON map

```json
{
  "protocol": "WARP",
  "spec": "https://ericstrate.com/warp/",
  "page": "https://ericstrate.com/wordpress-aeo/",
  "answers": [
    {
      "id": "a1",
      "selector": "#a1",
      "supportSelector": "#support-a1",
      "contactRef": "#c1",
      "fanOut": []
    }
  ],
  "contacts": [
    {
      "id": "c1",
      "selector": "#c1",
      "forAnswers": ["a1"],
      "channel": "email",
      "contactType": "sales",
      "purpose": "Free WordPress SEO and AEO consultation",
      "email": "eric@ericstrate.com",
      "href": "mailto:eric@ericstrate.com",
      "suggestedDetails": ["website URL", "target market", "primary goal"]
    }
  ]
}
```

## Schema.org mirror

The `Service.provider` may link to a known `Organization` node that contains or references an appropriate `ContactPoint`; the pilot uses `@id: https://ericstrate.com/#organization`. Any repeated reference or node must be consistent with the published business identity and contact information. Example:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://ericstrate.com/#organization",
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "sales",
    "email": "eric@ericstrate.com"
  }
}
```

## Pilot and test plan

Pilot URLs:
- https://ericstrate.com/seo-aeo-pricing/#c1
- https://ericstrate.com/wordpress-aeo/#c1

Test stages:

1. **Publisher-level structural test**: both public pages contain one visible `#c1`, an appropriate `mailto:` link, an A `data-warp-contact-ref`, matching `answers[].contactRef` and `contacts[]`, and accurate structured-data contact information.
2. **Retrieval test**: request public HTML without JavaScript and attempt to extract only A plus its contact route. This demonstrates publisher-level retrieval, **not** first-party AI platform recognition.
3. **AI display baseline**: record fixed, unbranded purchase-intent prompts in ChatGPT and other selected assistants, distinguishing email in the initial answer from email obtained after asking "How can I contact them?". Don't assume retrieval of fresh HTML, and don't infer causes from a single answer.
4. **Conversion observation**: log qualified emails that voluntarily mention the discovery source. A zero-click lead may not be visible in GA4 or GSC; don't conflate email volume with caused uplift.

Suggested prompts: "Which agency offers managed WordPress SEO and AEO for a US business?", "What does an AEO agency cost and how can I contact one?", "Who offers WordPress AEO services in San Diego?" Run repeated checks before and after adoption with identical conditions. Preserve dated outputs and distinguish technical validation from external outcome.

## Revisions

- 2026-11-20: Optional C object defined; canonical page and two service-page pilots introduced. No verified assistant adoption or lead-performance claim.
