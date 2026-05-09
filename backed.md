---
layout: default
title: Companies backed
description: Every Michigan company publicly backed by a Tuebor pledgee. Not investment advice — just a public record of where Michigan investors are putting money to work.
eyebrow: 05 / Backed
display_title: Companies backed.
permalink: /backed/
prose_full: true
---

{%- comment -%}
Build a flat list of rows, then collect unique companies and re-iterate to
render one row per company with all backers grouped.

Sort key layout (string-sortable, ascending):
  company_lc | year | last_name_lc | company | url | name | slug | year

year sorts ascending so oldest investment lists first within a company group.
last_name_lc breaks ties when two pledgees backed in the same year.
{%- endcomment -%}

{%- assign published = site.pledgees | where: "published", true -%}
{%- assign rows_raw = "" -%}
{%- for p in published -%}
  {%- if p.backed -%}
    {%- for b in p.backed -%}
      {%- if b.public -%}
        {%- assign year_int = b.year | default: 0 | plus: 0 -%}
        {%- assign url = b.url | default: "" -%}
        {%- assign company = b.company -%}
        {%- assign company_lc = company | downcase -%}
        {%- assign last_lc = p.last_name | downcase -%}
        {%- capture rows_raw -%}{{ rows_raw }}{{ company_lc }}|{{ year_int }}|{{ last_lc }}|{{ company }}|{{ url }}|{{ p.name }}|{{ p.slug }}|{{ year_int }}
{% endcapture -%}
      {%- endif -%}
    {%- endfor -%}
  {%- endif -%}
{%- endfor -%}
{%- assign rows = rows_raw | strip | split: "
" | sort -%}

{%- comment -%}
Build unique-company list. parts[0]=company_lc, parts[3]=company, parts[4]=url.
Captures the first occurrence (which after sort is the oldest year).
{%- endcomment -%}
{%- assign seen_keys = "" -%}
{%- assign companies_raw = "" -%}
{%- for row in rows -%}
  {%- assign parts = row | split: "|" -%}
  {%- assign key = parts[0] -%}
  {%- assign sentinel = "@@" | append: key | append: "@@" -%}
  {%- unless seen_keys contains sentinel -%}
    {%- assign seen_keys = seen_keys | append: sentinel -%}
    {%- capture companies_raw -%}{{ companies_raw }}{{ key }}|{{ parts[3] }}|{{ parts[4] }}
{% endcapture -%}
  {%- endunless -%}
{%- endfor -%}
{%- assign companies = companies_raw | strip | split: "
" -%}

<div class="backed">
  {%- assign company_count = companies | size -%}
  <p class="backed-lede"><strong>{{ company_count }}</strong> Michigan {% if company_count == 1 %}company{% else %}companies{% endif %} publicly backed by a Tuebor pledgee.<br><a href="{{ '/roster/' | relative_url }}">See the roster</a> · <a href="{{ '/howto/makepublic' | relative_url }}">Add yourself</a>.</p>

  <p class="backed-disclaimer">This is a public record, not investment advice. Each pledgee makes their own investment decisions. Tuebor is not an investment advisor and does not collect fees or enter the flow of money. See our <a href="{{ '/legal-disclaimer.html' | relative_url }}">legal disclaimer</a>.</p>

  <table class="backed-table">
    <thead>
      <tr>
        <th class="col-company">Company</th>
        <th class="col-pledgee">Backed by</th>
      </tr>
    </thead>
    <tbody>
      {%- for c in companies -%}
        {%- assign cparts = c | split: "|" -%}
        {%- assign ckey = cparts[0] -%}
        {%- assign cname = cparts[1] -%}
        {%- assign curl = cparts[2] -%}
        <tr>
          <td class="col-company">
            {%- if curl != "" -%}
              <a href="{{ curl }}" target="_blank" rel="noopener">{{ cname }}</a>
            {%- else -%}
              {{ cname }}
            {%- endif -%}
          </td>
          <td class="col-pledgee">
            {%- assign first = true -%}
            {%- for row in rows -%}
              {%- assign rparts = row | split: "|" -%}
              {%- if rparts[0] == ckey -%}
                {%- unless first -%}, {% endunless -%}
                <a href="{{ '/roster/' | append: rparts[6] | relative_url }}">{{ rparts[5] }}</a> <span class="year">({{ rparts[7] }})</span>
                {%- assign first = false -%}
              {%- endif -%}
            {%- endfor -%}
          </td>
        </tr>
      {%- endfor -%}
    </tbody>
  </table>
</div>
