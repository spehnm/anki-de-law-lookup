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
        """Loads the law map json, which contains the format the citated law
        is quoted in the URL

        Returns:
            json: contains the format
        """
        script_dir = os.path.dirname(__file__)
        json_path = os.path.join(script_dir, "law_mapping.json")
        with open(json_path, "r") as map_file:
            return json.load(map_file)
    
    def get_text_on_front_card(self, card):
        return card.q()
    
    def tokenize_front_card(self, card):
        """Uses the tokenizer module to tokenize the front side of our card

        Args:
            card: gets the front side of our card using the anki-api

        Returns:
            list: containing strings following the regex from our tokenizter module
        """
        text = self.get_text_on_front_card(card)
        return tok.tokenizer_german_legal_texts(text)
    
    def get_first_reference(self, tokens):
        """Gets the first reference that startswith '§' or 'Art.'

        Args:
            tokens (list): list containing tokens that follow our regex rules from the tokenizer
            module

        Returns:
            string or None: If we have a citated reference we extract the first from our front card,
            otherwise we don't extract anything
        """
        for token in tokens:
            if token.startswith('§') or token.startswith('Art.'):
                return token
        return None
    
    def get_expression_slices(self, first_reference):
        """Slices our first token into parts we can later insert into the URL

        Args:
            first_reference (string): string containing a legal reference

        Returns:
            string, string, bool: get two strings to later insert them into the URL and
            one boolean value to account for the possibility that some citation starts with 'Art.'
            and not with '§'
        """
        parts = first_reference.split()
        uses_paragraph_symbol = True
        if len(parts) >= 3:
            section_number = parts[1]  # Gets '1' from '§ 1 BGB' or 'Art. 1 GG'
            law = parts[-1]  # Gets 'BGB' from '§ 1 BGB' or 'GG' from 'Art. 1 GG'
            if parts[0] != '§':  # Effectively, this checks for the 'Art.'
                uses_paragraph_symbol = False
            return section_number, law, uses_paragraph_symbol
        return None, None, None
    
    def law_map_lookup(self, law):
        """Looks up the citated law in a json that contains the
        actual type of how the law is formatted in the URL.

        Args:
            law (string): gets the string from the
            get_expression_slices methode (2nd return value)

        Returns:
            string: depending on if the law was found in the
            json it returns the corresponding string to insert
            it into the URL later, otherwise it just returns
            the original string
        """
        return self.law_map.get(law, law)
    
    def get_reference(self, section_number, law, uses_paragraph_symbol):
        """Opens website using the expression slices

        Args:
            section_number (string): contains the 'section' (e.g. 1, 1a)
            law (string): contains the actual law (e.g. GG, BGB)
            uses_paragraph_symbol (bool): accounts for citations of laws not using '§'
            but rather use 'Art.'
        """
        law_code = self.law_map_lookup(law)
        if law_code:  # Check if law_code is found in the mapping
            if uses_paragraph_symbol:
                url = f"https://www.gesetze-im-internet.de/{law_code}/__{section_number}.html"
            else:
                url = f"https://www.gesetze-im-internet.de/{law_code}/art_{section_number}.html"
            webbrowser.open(url)
    
    def install_hooks(self):  # wraps our functionality into anki
        Reviewer._showQuestion = wrap(Reviewer._showQuestion, self._on_reviewer_show_question, "after")
    
    def _on_reviewer_show_question(self, reviewer):  # time to trigger the functionality
        card = reviewer.card
        self.current_card = card
    
    def setup_shortcut(self):
        # Register the shortcut '#'
        shortcut = QShortcut(QKeySequence("#"), mw)
        shortcut.activated.connect(self.open_reference)
    
    def open_reference(self):  # Wraps our methods together
        if self.current_card:
            card = self.current_card
            tokens = self.tokenize_front_card(card)
            first_reference = self.get_first_reference(tokens)
            if first_reference:
                section_number, law, uses_paragraph_symbol = self.get_expression_slices(first_reference)
                if section_number and law:  # Only check for this, so it opens even if it's an 'Artikel' not a '§'
                    self.get_reference(section_number, law, uses_paragraph_symbol)
