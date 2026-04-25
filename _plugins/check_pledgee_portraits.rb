# Guard plugin: fail the build if a pledgee's `portrait:` path doesn't resolve
# to a file on disk. Catches "forgot to run _dither.py" before deploy.
Jekyll::Hooks.register :site, :post_read do |site|
  coll = site.collections["pledgees"]
  next unless coll

  coll.docs.each do |doc|
    next if doc.data["published"] == false
    portrait = doc.data["portrait"]
    if portrait.nil? || portrait.to_s.strip.empty?
      raise "check_pledgee_portraits: #{doc.relative_path} is missing a `portrait:` field."
    end
    rel = portrait.sub(%r{^/}, "")
    disk_path = File.join(site.source, rel)
    unless File.exist?(disk_path)
      raise "check_pledgee_portraits: #{doc.relative_path} references #{portrait}, but no file exists at #{disk_path}. Run `python assets/images/_dither.py`."
    end
  end
end
