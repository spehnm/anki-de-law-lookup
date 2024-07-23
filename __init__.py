# __init__.py

from .lookup import LawLookup

# Initialize LawLookup object
law_lookup = LawLookup()

# Hook in Anki's review process
law_lookup.install_hooks()
