import os
from pocketsphinx import pocketsphinx
from sphinxbase.sphinxbase import *
import pyaudio

def recognition(keyphrase_function, key_phrase):

    modeldir = "data/files/sphinx/models"

    # Create a decoder with certain model
    config = pocketsphinx.Decoder.default_config()
    # Use the mobile voice model (en-us-ptm) for performance constrained systems
    config.set_string('-hmm', os.path.join(modeldir, 'en-us/en-us-ptm'))
    # config.set_string('-hmm', os.path.join(modeldir, 'en-us/en-us'))
    config.set_string('-dict', os.path.join(modeldir, 'en-us/cmudict-en-us.dict'))
    config.set_string('-keyphrase', key_phrase)
    config.set_string('-logfn', 'data/files/sphinx.log')
    config.set_float('-kws_threshold', 1)

    # Start a pyaudio instance
    p = pyaudio.PyAudio()
    # Create an input stream with pyaudio
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    # Start the stream
    stream.start_stream()

    # Process audio chunk by chunk. On keyword detected perform action and restart search
    decoder = pocketsphinx.Decoder(config)
    decoder.start_utt()
    # Loop forever
    while True:
        # Read 1024 samples from the buffer
        buf = stream.read(1024)
        # If data in the buffer, process using the sphinx decoder
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break
        # If the hypothesis is not none, the key phrase was recognized
        if decoder.hyp() is not None:
            keyphrase_function()
            # Stop and reinitialize the decoder
            decoder.end_utt()
            decoder.start_utt()