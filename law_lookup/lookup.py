# law_lookup/lookup.py

import re
import webbrowser
from aqt.reviewer import Reviewer
from anki.hooks import wrap

class LawLookup:
    def __init__(self):
        pass  # Add suitable regex
    
    def get_expression_slices(self, text):
        pass  # Slice expression so we can insert strings into URL
    
    def get_reference(self, text):
        expression_slices = self.get_expression_slices()        
        # Insert slices into url and open the url
    
    def on_card_show(self, card):
        front_card = card.q()
        self.get_reference(front_card)
        
    def install_hooks(self):
        Reviewer._showQuestion = wrap(Reviewer._showQuestion, self._on_reviewer_show_question, "after")
        
    def _on_reviewer_show_question(self, reviewer):
        card = reviewer.card
        self.on_card_show(card)