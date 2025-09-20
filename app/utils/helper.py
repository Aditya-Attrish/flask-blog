def generate_slug(title):
  """Generate a URL-friendly slug from the title"""
  import re
  slug = title.lower()
  slug = re.sub(r'[^a-z0-9]+', '-', slug)
  slug = re.sub(r'^-|-$', '', slug)
  return slug