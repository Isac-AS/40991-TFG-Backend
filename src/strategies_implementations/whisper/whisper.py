import whisper
import logging
import pickle
import sys
#from ..strategy import Strategy

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
            logging.info("Starting transcription...")
            model = whisper.load_model("medium")
            result = model.transcribe(path)
            logging.info("Finished transcribing.")
            return result["text"]
            
        except Exception as e:
            logging.error("Error while attempting transcription.")
            logging.error(e)
            return "Error durante la transcripción."

if __name__ == '__main__':
    data = sys.argv[1]
    print(data)
    #audio_file_path = pickle.loads(data)
    #print(audio_file_path)
    transcription = WhisperSpeechToTextStrategy.execute(data)
    print(transcription)