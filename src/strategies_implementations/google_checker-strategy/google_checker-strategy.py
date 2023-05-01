import json
import sys
from google_spell_checker import GoogleSpellChecker


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
        spell_checker = GoogleSpellChecker(lang="es")
        spell_checked_result = spell_checker.check(text)
        # A true in that literal means the spelling was correct so the text is returned
        if (spell_checked_result[0] == True):
            return {'output': text}
        # Otherwise, the correction is returned
        if spell_checked_result[1] is None:
            return {'output': text}
        return {'output': spell_checked_result[1]}


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
