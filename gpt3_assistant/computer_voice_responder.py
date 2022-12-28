import os
import subprocess
import logging
from gpt3_assistant.clients.google_text_to_speech_client import GoogleTextToSpeechClient
from gpt3_assistant.bases.responder import Responder


class ComputerVoiceResponder(Responder):
    def __init__(self, mp3_filename, lang=None, tld=None):
        self._mp3_filename = mp3_filename
        self._language = lang
        self._top_level_domain = tld
        self.text_to_speech_client = GoogleTextToSpeechClient(lang, tld)

    def respond(self, text_to_speak: str):
        """
        Speak the referenced text on the machine speakers.
        :param text_to_speak: the text to speak.
        :return: None
        """
        try:
            logging.debug(f"ComputerVoice.speak - '{text_to_speak}'")
            full_mp3_path = os.path.join(os.getcwd(), self._mp3_filename)
            self.text_to_speech_client.convert_text_to_mp3(text_to_speak, full_mp3_path)
            subprocess.call(["afplay", full_mp3_path])
        except Exception as e:
            print(f"Exception caught trying to speak: {e}")
        finally:
            self._cleanup_temp_files()

    def _cleanup_temp_files(self):
        """
        Remove all temporary files and cleanup before shutting down.
        :return: None
        """
        logging.debug(f"ComputerVoice.cleanup_temp_files - {self._mp3_filename}")

        # check if temporary file exists before trying to delete
        if os.path.exists(self._mp3_filename):
            os.remove(self._mp3_filename)