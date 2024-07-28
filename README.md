# LawLookup Addon for Anki

This Anki addon automatically looks up legal references in German law texts and opens the corresponding webpage when a specific shortcut - by default `#` - is pressed during card review. The addon uses a tokenizer to identify legal references in the front text of a card and opens the corresponding law section on gesetze-im-internet.de. It uses the citation guideline by the German Federal Administrative Court.

## Features (mind that this is the launch version)

- Identifies legal references in German legal texts, if you followed the German Federal Administrative Court citation style.
- Opens the corresponding law section on gesetze-im-internet.de.
- Activation via a customizable keyboard shortcut during card review.

## Installation

0. **(Easy way:) Check out the Anki Addon Website**
https://ankiweb.net/shared/info/135761574 (the add-on code you can simply input is: 135761574)

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/law_lookup.git
    ```

2. **Navigate to the Anki addons directory:**

    - On Windows: `C:\Users\<YourUserName>\AppData\Roaming\Anki2\addons21`
    - On macOS: `~/Library/Application Support/Anki2/addons21`
    - On Linux: `~/.local/share/Anki2/addons21`

3. **Copy the `law_lookup` directory into the `addons21` directory:**

    ```sh
    cp -r law_lookup <Anki addons directory>
    ```

## Usage

1. **Open Anki and start reviewing your cards.**
2. **Press the `#` key during card review to open the corresponding law section.**

## What's next?
Currently, I'm working on a bugfix appearing on non-Windows systems. I think my next step will be to account for different citation styles (e.g. § 771 II ZPO instead of § 771 Abs. 2 ZPO).

## Customization

If you wish to change the shortcut key, you can modify the `setup_shortcut` method in the `lookup.py` file.

Example to change the shortcut to `+`:

```python
shortcut = QShortcut(QKeySequence("+"), mw)
