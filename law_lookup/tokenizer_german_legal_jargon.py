# Use my old GitLab snippet for tokenizing: https://gitlab.com/-/snippets/3622982
# Mind that this snipped did contain a bug that is fixed here (see Bugfix #1 below)

import re

def token_merger(tokens, merge_word):
    """Merge two tokens via merge_word and pops out the latter word since it got linked

    Args:
        tokens (list): list filled with regular expressions from the tokenizer_german_legal_texts function
        merge_word (string): this string serves as linking element

    Returns:
        list: tokens now contains several via merge_word linked elements
    """
    for index in range(len(tokens) - 1):       
        try:
            
            # Define variables to merge via indices
            current_element = tokens[index]             
            next_element = tokens[index + 1]
                    
            # Merge tokens via "merge_word"
            if next_element.startswith(merge_word):
                tokens[index] = current_element + " " + next_element
                tokens.pop(index + 1)
                
        except IndexError:
            pass
        
    return tokens

def token_merge_iteration(tokens):
    """Merges tokens for each word in merge_word list
    (containing all citation rules from the Federal Administrative Court of Germany)

    Args:
        tokens (list): list filled with regular expressions from the tokenizer_german_legal_texts function
    """
    merge_words = ["Abs.", "Satz", "Nr.", "Var.", "Teils.",
                   "Halbs.", "Buchstabe", "Doppelbuchstabe", "Alt."]
    for i in merge_words:
        token_merger(tokens, i)
        
def tokenizer_german_legal_texts(text):
    """Creates legal-context-sensitive tokens
    
    Args:
        text (string): text that contains legal jargon

    Returns:
        tokens (list):  returning list only contains legal-context elements that remain in their citational context
        
    """
    
    """Create list that contains specific regular expressions in the argument according
    to the citation guideline of the Federal Administrative Court of Germany:
    https://www.bverwg.de/rechtsprechung/urteile-beschluesse/zitierungen (last time checked: 13.11.2023)"""
    tokens = re.findall(r'Art.\s*\S+|'  # Catch <Art.>< ><character(s)>
                        r'§§\s*\S+|'  # Catch <§§>< ><character(s)>
                        r'§\s*\S+|'  # Catch <§>< ><character(s)>
                        r'Abs.\s*\S+|'   # Catch <Abs.>< ><character(s)>
                        r'Satz\s*\S+|'  # Catch <Satz>< ><character(s)>
                        r'Halbs\.\s*\S+|'  # Catch <Halbs.>< ><character(s)>
                        r'Teils\.\s*\S+|'  # Catch <Teils.>< ><character(s)>
                        r'Nr\.\s*\S+|'  # Catch <Nr.>< ><character(s)>
                        r'Alt\.\s*\S+|'  # Catch <Alt.>< ><character(s)>
                        r'Var\.\s*\S+|'  # Catch <Var.>< ><character(s)>
                        r'Buchstabe\s*\S+|'  # Catch <Buchstabe>< ><character(s)>
                        r'Doppelbuchstabe\s*\S+|'  # Catch <Doppelbuchstabe>< ><character(s)>
                        r'und|'  # Catch <und>
                        r'bis|'  # Catch <bis>
                        r'\S+'  # Catch what's left
                        , text)    
              
    # Merge tokens if they are related in german legal syntax using the citation guideline above
    for index in range(len(tokens) - 1):  
        try:
            
            # Define variables to merge via indices
            current_element = tokens[index]            
            next_element = tokens[index + 1]        
            element_after_next_element = tokens[index + 2]
            
            # Merge tokens via the conjuctions "bis" and "und"
            if next_element.startswith("bis"):
                tokens[index] = current_element + " " + next_element + " " + element_after_next_element
                tokens.pop(index + 1), tokens.pop(index + 1)
            if next_element.startswith("und"):
                tokens[index] = current_element + " " + next_element + " " + element_after_next_element
                tokens.pop(index + 1), tokens.pop(index + 1)   
        except IndexError:
            pass
        
    token_merge_iteration(tokens)
    
    for index in range(len(tokens) - 1):       
        try:
            # Define variables to merge via indices
            current_element = tokens[index]             
            next_element = tokens[index + 1]        
            # Merge tokens via "§"
            if current_element.startswith("§") or current_element.startswith("Art."): # Bugfix #1
                tokens[index] = current_element + " " + next_element
                tokens.pop(index + 1)
        except IndexError:
            pass
    return tokens
