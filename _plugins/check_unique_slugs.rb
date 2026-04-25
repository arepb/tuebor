# Guard plugin: fail the build on duplicate pledgee slugs.
# Prevents one profile from silently overwriting another at /roster/<slug>/.
Jekyll::Hooks.register :site, :post_read do |site|
  coll = site.collections["pledgees"]
  next unless coll

  seen = {}
  coll.docs.each do |doc|
    slug = doc.data["slug"]
    if slug.nil? || slug.to_s.strip.empty?
      raise "check_unique_slugs: #{doc.relative_path} is missing a `slug:` front-matter field."
    end
    if seen.key?(slug)
      raise "check_unique_slugs: duplicate slug #{slug.inspect} in #{doc.relative_path} (also in #{seen[slug]})."
    end
    seen[slug] = doc.relative_path

    # Populate last_name for alpha-within-year sort on /roster/.
    name = doc.data["name"].to_s
    doc.data["last_name"] ||= name.strip.split(/\s+/).last.to_s.downcase
  end
end
