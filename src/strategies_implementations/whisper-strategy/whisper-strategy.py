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
            return result["text"]
            
        except Exception as e:
            logging.error("Error while attempting transcription.")
            logging.error(e)
            return "Error durante la transcripción."

if __name__ == '__main__':
    path_to_recording = sys.argv[1]
    transcription = WhisperSpeechToTextStrategy.execute(path_to_recording)
    print(transcription)