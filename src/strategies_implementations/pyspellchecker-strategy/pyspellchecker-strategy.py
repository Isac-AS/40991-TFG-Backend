import pickle
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
        spell_checked_text = " ".join(
            [spanish_spell_checker.correction(token) for token in text.split()])
        return {'output': spell_checked_text}


if __name__ == '__main__':
    # Get strategy input
    strategy_input = sys.argv[1]
    # Run execute command
    strategy_output = UsingPySpellChecker.execute(strategy_input)
    # Serialize the output
    serialized_output = pickle.dumps(strategy_output)
    # Return serialized output through stdout
    sys.stdout.buffer.write(serialized_output)
