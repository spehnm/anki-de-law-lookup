import re
import webbrowser
from . import tokenizer_german_legal_jargon as tok
from aqt.reviewer import Reviewer
from anki.hooks import wrap

class LawLookup:
    def __init__(self):
        self.install_hooks()
    
    def get_text_on_front_card(self, card):
        return card.q()
    
    def tokenize_front_card(self, card):
        text = self.get_text_on_front_card(card)
        return tok.tokenizer_german_legal_texts(text)
    
    def get_first_reference(self, tokens):
        for token in tokens:
            if token.startswith('§'):
                return token
        return None  # If no token starts with '§', we do not have any reference
    
    def get_expression_slices(self, first_reference):
        parts = first_reference.split()
        if len(parts) >= 3:
            section_number = parts[1]  # Gets '1' from '§ 1 BGB'
            law = parts[-1]  # Gets 'BGB' from '§ 1 BGB'
            return section_number, law
        return None, None
            
    def get_reference(self, section_number, law):
        law = law.lower()
        url = f"https://www.gesetze-im-internet.de/{law}/__{section_number}.html"
        webbrowser.open(url)
    
    def on_card_show(self, card):
        tokens = self.tokenize_front_card(card)
        first_reference = self.get_first_reference(tokens)
        if first_reference:
            section_number, law = self.get_expression_slices(first_reference)
            if section_number and law:
                self.get_reference(section_number, law)
        
    def install_hooks(self):
        Reviewer._showQuestion = wrap(Reviewer._showQuestion, self._on_reviewer_show_question, "after")
        
    def _on_reviewer_show_question(self, reviewer):
        card = reviewer.card
        self.on_card_show(card)
