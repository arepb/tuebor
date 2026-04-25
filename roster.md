---
layout: default
title: Roster
description: The people who have taken the Tuebor pledge — Michigan investors backing Michigan companies, one every year.
eyebrow: 04 / Roster
display_title: Roster.
permalink: /roster/
---

{% assign published = site.pledgees | where: "published", true %}
{% assign by_year = published | sort: "year_joined" %}
{% assign years = by_year | map: "year_joined" | uniq %}

<div class="roster">
  {% for yr in years %}
    {% assign in_year = by_year | where: "year_joined", yr | sort: "last_name" %}
    <section class="roster-year">
      <p class="roster-year-label">Joined {{ yr }}</p>
      <div class="roster-grid">
        {% for p in in_year %}
          {% include pledgee-card.html pledgee=p %}
        {% endfor %}
      </div>
    </section>
  {% endfor %}
</div>
