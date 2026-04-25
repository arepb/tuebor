---
layout: default
title: Roster
description: The people who have taken the Tuebor pledge — Michigan investors backing Michigan companies, one every year.
eyebrow: 04 / Roster
display_title: Roster.
permalink: /roster/
---

{% assign published = site.pledgees | where: "published", true %}
{% assign founders = published | where: "founder", true | sort: "last_name" %}
{% assign rest = published | where_exp: "p", "p.founder != true" | sort: "last_name" %}

<div class="roster">
  <p class="roster-lede">Here are the people who've taken the Tuebor pledge. Each card is a public commitment to back at least one Michigan business this year — and every year. <a href="{{ '/howto/makepublic' | relative_url }}">Add yourself</a>.</p>
  <div class="roster-grid">
    {% for p in founders %}
      {% include pledgee-card.html pledgee=p %}
    {% endfor %}
    {% for p in rest %}
      {% include pledgee-card.html pledgee=p %}
    {% endfor %}
  </div>
</div>
