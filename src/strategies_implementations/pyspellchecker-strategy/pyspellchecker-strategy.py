import json
import sys
from spellchecker import SpellChecker


class UsingPySpellChecker():

    @classmethod
    def execute(cls, text: str) -> str:
        """
        Implementation of the spell checking part of the pipeline using the
        pyspellchecker library.

        :param text: Text to perform the spell checking on
        :type text: str
        :return: Spell checked text
        :rtype: str
        """
        spanish_spell_checker = SpellChecker(language="es")
        split_text = text.split()
        corrected_text = [spanish_spell_checker.correction(token) if spanish_spell_checker.correction(token) is not None else token for token in split_text]
        spell_checked_text = " ".join(corrected_text)

        return {'output': spell_checked_text}


if __name__ == '__main__':
    # Get strategy input
    standard_input = input()
    input_dict = json.loads(standard_input)
    strategy_input = input_dict['input']
    # Run execute command
    strategy_output = UsingPySpellChecker.execute(text=strategy_input)
    # Serialize the output
    serialized_output = json.dumps(strategy_output)
    # Return serialized output through stdout
    print(serialized_output)
