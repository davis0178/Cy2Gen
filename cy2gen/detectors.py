import numpy as np
np.float = float  # patch：fix madmom np.float error
np.int = int
from madmom.features.beats import RNNBeatProcessor, DBNBeatTrackingProcessor, BeatTrackingProcessor
from madmom.features.onsets import RNNOnsetProcessor, OnsetPeakPickingProcessor

class BPMDetector:
    def __init__(self, audio_path = "../contents/audio.mp3"):
        self.audio_path = audio_path

    def detect(self, difficulty):
        # calculate BPM
        act = RNNBeatProcessor()(self.audio_path)
        beat_proc = DBNBeatTrackingProcessor(fps=100)
        beats = beat_proc(act)
        intervals = np.diff(beats)
        bpm = 60.0 / np.median(intervals)

        # adjust bpm according to difficulty
        if difficulty == "CHAOS":
            if bpm > 280:
                while bpm > 280:
                    bpm /= 2
            if bpm < 180:
                while bpm < 150:
                    bpm *= 2

        elif difficulty == "HARD":
            if bpm > 200:
                while bpm > 200:
                    bpm /= 2

            if bpm < 100:
                while bpm < 100:
                    bpm *= 2

        elif difficulty == "EASY":
            if bpm > 100:
                while bpm > 100:
                    bpm /= 2

        # calculate beat activation functions
        onset_processor = RNNOnsetProcessor()
        activation = onset_processor(self.audio_path)

        # beat onset detection. adjust threshold to control sensitivity, combine beats between a short interval
        onset_picker = OnsetPeakPickingProcessor(threshold=0.5, combine=0.03)
        onsets = onset_picker(activation)


        first_beat = onsets[0]
        last_beat = onsets[-1]

        return first_beat, last_beat, round(float(bpm), 3)
