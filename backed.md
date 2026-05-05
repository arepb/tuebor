---
layout: default
title: Companies backed
description: Every Michigan company publicly backed by a Tuebor pledgee. Not investment advice — just a public record of where Michigan investors are putting money to work.
eyebrow: 05 / Backed
display_title: Companies backed.
permalink: /backed/
prose_full: true
---

{%- assign published = site.pledgees | where: "published", true -%}
{%- assign rows_raw = "" -%}
{%- for p in published -%}
  {%- if p.backed -%}
    {%- for b in p.backed -%}
      {%- if b.public -%}
        {%- assign year = b.year | default: 0 -%}
        {%- assign url = b.url | default: "" -%}
        {%- capture rows_raw -%}{{ rows_raw }}{{ year }}|{{ b.company }}|{{ url }}|{{ p.name }}|{{ p.slug }}
{% endcapture -%}
      {%- endif -%}
    {%- endfor -%}
  {%- endif -%}
{%- endfor -%}
{%- assign rows = rows_raw | strip | split: "
" | sort | reverse -%}

<div class="backed">
  <p class="backed-lede">Every Michigan company publicly backed by a Tuebor pledgee. Sorted by year, newest first. <a href="{{ '/roster/' | relative_url }}">See the roster</a> · <a href="{{ '/howto/makepublic' | relative_url }}">Add yourself</a>.</p>

  <p class="backed-disclaimer">This is a public record, not investment advice. Each pledgee makes their own investment decisions. Tuebor is not an investment advisor and does not collect fees or enter the flow of money. See our <a href="{{ '/legal-disclaimer.html' | relative_url }}">legal disclaimer</a>.</p>

  <table class="backed-table">
    <thead>
      <tr>
        <th class="col-year">Year</th>
        <th class="col-company">Company</th>
        <th class="col-pledgee">Backed by</th>
      </tr>
    </thead>
    <tbody>
      {%- for row in rows -%}
        {%- assign parts = row | split: "|" -%}
        <tr>
          <td class="col-year">{{ parts[0] }}</td>
          <td class="col-company">
            {%- if parts[2] != "" -%}
              <a href="{{ parts[2] }}" target="_blank" rel="noopener">{{ parts[1] }}</a>
            {%- else -%}
              {{ parts[1] }}
            {%- endif -%}
          </td>
          <td class="col-pledgee"><a href="{{ '/roster/' | append: parts[4] | relative_url }}">{{ parts[3] }}</a></td>
        </tr>
      {%- endfor -%}
    </tbody>
  </table>
</div>
