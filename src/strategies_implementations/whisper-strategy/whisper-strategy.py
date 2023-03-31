import json
import whisper
import logging
import sys


class WhisperSpeechToTextStrategy():

    @classmethod
    def execute(cls, path: str) -> str:
        """
        Implementation of the speech to text part of the pipeline using whisper.
        :param path: Path to the audio file
        :type path: str
        :return: Whisper's transcription of the audio file
        :rtype: str
        """
        try:
            model = whisper.load_model("medium")
            result = model.transcribe(path)
            return {'output': result["text"]}

        except Exception as e:
            logging.error("Error while attempting transcription.")
            logging.error(e)
            return "Error durante la transcripción."


if __name__ == '__main__':
    # Get strategy input
    standard_input = input()
    input_dict = json.loads(standard_input)
    strategy_input = input_dict['input']
    # Run execute command
    strategy_output = WhisperSpeechToTextStrategy.execute(strategy_input)
    # Serialize the output
    serialized_output = json.dumps(strategy_output)
    # Return serialized output through stdout
    print(serialized_output)