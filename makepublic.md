---
layout: default
title: Tell the world
description: Tell the world you're on the team — list Tuebor on your LinkedIn and put yourself on the roster.
eyebrow: 03 / Pledge · Make it public
display_title: "Tell the world you're on the team."
permalink: /howto/makepublic
---

You took the pledge. You backed a Michigan company. Tuebor is Michigan's next sports team — now tell people you're on it. Two steps.

## 01. List Tuebor on your LinkedIn.

This is your pledge proof. The public commitment.

- Go to your profile page on [LinkedIn](https://www.linkedin.com/in/) and click the **+** sign to list a new job (note: this is not a 'group' but actually listed as a job on LinkedIn). Look for [Tuebor](https://linkedin.com/company/tuebororg).
- **Role:** Pledge Investor
- **Description:** Through Tuebor.org, I take the pledge to invest in at least one State of Michigan-based business per year.

![LinkedIn post example](/assets/images/linkedin-post.png)

To make sure this new 'job' isn't the first listing in order on your profile, you can drag it up and down by first clicking the pencil icon ✎ and then use the up-down arrow symbol ↕:

![LinkedIn arrow example](/assets/images/linkedin-arrow.png)

## 02. Add yourself to the roster.

Get on the public roster at [tuebor.org/roster/](/roster/). Send us your story and we'll add you, too.

<aside class="sample-card-wrap" aria-label="Sample roster card">
  <div class="pledgee-card pledgee-card--grid sample-card">
    <div class="card">
      <div class="card-inner">
        <header class="card-frame">
          <span class="card-mark">Tuebor<span class="card-mark-dot">.</span></span>
          <span class="card-year">&rsquo;{{ 'now' | date: '%y' }}</span>
        </header>
        <figure class="card-photo">
          <svg class="sample-card-halftone" viewBox="0 0 80 100" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
            <defs>
              <pattern id="sample-halftone-dots" x="0" y="0" width="4" height="4" patternUnits="userSpaceOnUse">
                <circle cx="2" cy="2" r="1.1" fill="currentColor"/>
              </pattern>
            </defs>
            <rect width="80" height="100" fill="var(--tan)" opacity="0.35"/>
            <rect width="80" height="100" fill="url(#sample-halftone-dots)"/>
            <path d="M40 38c5.5 0 10-4.5 10-10s-4.5-10-10-10-10 4.5-10 10 4.5 10 10 10zm0 6c-9 0-22 4.5-22 13.5V72h44v-14.5C62 48.5 49 44 40 44z" fill="var(--paper)" opacity="0.85"/>
          </svg>
        </figure>
        <footer class="card-band">
          <strong class="pledgee-name">Your<br>name here</strong>
          <span class="pledgee-meta">Your city</span>
        </footer>
      </div>
    </div>
  </div>
  <p class="sample-card-caption">A sample card.<br>Yours could go here.</p>
</aside>

### What we need

- **Your name and city** in Michigan.
- **Your LinkedIn URL.** This is your pledge proof — see step 01 above.
- **A high-resolution headshot.** Bigger is better. We render it as a halftone portrait, so a sharp, well-lit photo gives the best result.
- **150–300 words on why you took the pledge.** First person. Your own voice.
- **The Michigan companies you've backed** (year, company, optional link). Mark each entry public or private. Only the public ones appear on your profile.

Click the button below — it opens a new email with the template pre-filled. Fill in your bits, attach your headshot, and send.

{% capture mailbody %}Hi Tuebor,

I took the pledge. Here is my info for the roster.

— BASICS —
Name:
City (in Michigan):
LinkedIn URL:

— STORY —
(150–300 words, first person, your own voice. Why Michigan. Why the pledge.)


— MICHIGAN COMPANIES BACKED —
(One per line: year · company · optional URL · public or private)
Examples:
2024 · Acme Inc. · https://acme.com · public
2025 · [stealth co] · — · private


— PHOTO —
I am attaching a high-resolution headshot to this email.
(If you would rather share a Dropbox/Drive link, paste it here: )


Thanks,

{% endcapture %}

<p style="margin-top:40px;">
  <a class="btn primary js-mailto" href="#" data-user="pledge" data-domain="tuebor.org" data-subject="Tuebor pledge submission" data-body="{{ mailbody | escape }}">Submit your pledge <span class="arrow">→</span></a>
</p>

After you send, expect a reply within a few days confirming your profile is live at `tuebor.org/roster/your-name`. If anything looks off, tell us and we'll fix it.
