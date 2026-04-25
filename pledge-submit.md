---
layout: default
title: Submit
description: Take the Tuebor pledge — invest in at least one Michigan business per year, and put yourself on the roster.
eyebrow: 05 / Submit
display_title: Be on the wall.
permalink: /pledge/submit/
---

You took the pledge. You backed a Michigan company. Now tell us — and the next pledgee — who you are.

We'll author your profile by hand and email you when it's live at `tuebor.org/roster/your-name`.

## What we need

- **Your name and city** in Michigan.
- **Your LinkedIn URL.** This is your pledge proof — the public commitment.
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

After you send, expect a reply within a few days confirming your profile is live. If anything looks off, tell us and we'll fix it.
