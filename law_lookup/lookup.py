import webbrowser
import json
import os
from . import tokenizer_german_legal_jargon as tok
from aqt.reviewer import Reviewer
from aqt import mw
from aqt.qt import QShortcut, QKeySequence
from anki.hooks import wrap

class LawLookup:
    def __init__(self):
        self.install_hooks()
        self.setup_shortcut()
        self.current_card = None
        self.law_map = self.load_law_mapping()
    
    def load_law_mapping(self):
        script_dir = os.path.dirname(__file__)
        json_path = os.path.join(script_dir, "law_mapping.json")
        with open(json_path, "r") as map_file:
            return json.load(map_file)
    
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
    
    def law_map_lookup(self, law):
        # Lookup the corresponding value in law_mapping.json
        return self.law_map.get(law, None)
    
    def get_reference(self, section_number, law):
        law_code = self.law_map_lookup(law)
        url = f"https://www.gesetze-im-internet.de/{law_code}/__{section_number}.html"
        webbrowser.open(url)
    
    def install_hooks(self):
        Reviewer._showQuestion = wrap(Reviewer._showQuestion, self._on_reviewer_show_question, "after")
    
    def _on_reviewer_show_question(self, reviewer):
        card = reviewer.card
        self.current_card = card  # Save the current card
    
    def setup_shortcut(self):
        # Register the shortcut #
        shortcut = QShortcut(QKeySequence("#"), mw)
        shortcut.activated.connect(self.open_reference)
    
    def open_reference(self):
        # Ensure that a card is currently being reviewed
        if self.current_card:
            card = self.current_card
            tokens = self.tokenize_front_card(card)
            first_reference = self.get_first_reference(tokens)
            if first_reference:
                section_number, law = self.get_expression_slices(first_reference)
                if section_number and law:
                    self.get_reference(section_number, law)
