# Cy2Gen: Automatic Chart Generation for Rhythm Game Cytoid Based on Audio Analysis

**Yicen Liu**  
University of Michigan  
yicen@umich.edu

---

## Abstract

Cy2Gen is a tool designed to automate the creation of Cytoid rhythm game charts based on raw audio input. Using beat detection and onset tracking techniques from the `madmom` library, Cy2Gen identifies key rhythm structure—including the BPM, the first beat, and the last beat. Based on these parameters and user-selected attributes (such as difficulty and pattern), the system generates a complete `.cytoidlevel` beatmap package. This project aims to offer efficient practice for Cytus II/Cytoid players, lower the barrier of entry for rhythm game creators and explore the feasibility of AI-assisted chart generation in game design.

---

## 1. Motivation

Designing high-quality charts manually for rhythm games is time-consuming and requires significant musical knowledge and software skills. Existing solutions like BeatLearning primarily focus on PC rhythm game Osu! and require deep learning infrastructure. However, there is a lack of lightweight, extensible tools specifically for mobile rhythm games like Cytoid. Cy2Gen is a response to this gap, allowing both enthusiasts and developers to automatically generate playable content with minimal effort.

---

## 2. Approach

Cy2Gen’s architecture is structured in a modular pipeline as follows:

1. **User Input**: The user uploads an MP3 file and an optional background image, and specifies title, artist, difficulty, and pattern metadata.
2. **Beat Analysis**: Using `madmom`’s `RNNDownBeatProcessor`, the BPM, first beat time, and last beat time are detected.
3. **Chart Construction**:
   - Timing is calculated using `time_base = 480`(typical case in most of Cytoid charts) and BPM.
   - Pages and notes are generated with configurable patterns (e.g., starting sides, spread density).
   - Notes are placed in quantized positions aligned with detected downbeats. A suggested local chart offset is also provided for better player experience.
4. **Packaging**: The chart metadata (`level.json`) and notes data (`ex.json`) as well as uploaded mp3 itself(`audio.mp3`), generated song preview(`pv.mp3`) and chart background image(`BG.png`) are saved and zipped as a Cytoid-compatible file.

All code is implemented in Python 3.10+, and the main UI is provided through a Jupyter Notebook(`generate_cy2`) for ease of use.

---

## 3. Evaluation Criteria

- **Accuracy**: Precise estimation of chart's bpm based on RNN model.
- **Playability**: User specified difficulties making charts adjustable to different player skills.
- **Flexibility**: Ability to support multiple rhythmic patterns.
- **Automation**: End-to-end generation without extra tunings.

---

## 4. Timeline

| Date           | Milestone                                    |
|----------------|----------------------------------------------|
| Week 1         | Finish pipeline setup and `madmom` integration |
| Week 2         | Implement full chart generation logic        |
| Week 3         | Add customization (patterns, sides) and preview generator |
| Week 4         | Create submission-ready example folder and README |
| Final Week     | Poster presentation + optional Collab demo   |

---

## 5. Deliverables

- `generate_cy2.ipynb`: Main notebook for Cytoid chart generation.
- `converters.py`: Core modules for note mapping and level metadata generating.
- `detectors.py`: Core modules for BPM detection.
- `README.md`: Instructions and usage guide.
- `contents`: Cytoid level components ready to be packed into .cytoidlevel file.
- `outputs`: Cytoid-compatible ready-to-be-played chart files.

---

## 6. Acknowledgments

This project was inspired by:

- **BeatLearning** by sedthh: For defining modern rhythm game AI workflows.
- **Cytoid**: An open-source mobile rhythm game that enabled this research.
- **madmom**: For powerful music signal processing tools.
- **MUG-Diffusion**: For offering a innovative approach to chart generation via diffusion models.

Special thanks to the STATS507 professor Dr. Xian Zhang for project flexibility and support.

---

## 7. References
[1] Böck, S. & Schedl, M. (2012). "Enhanced beat tracking with context-aware neural networks". *Proc. of the 14th International Conference on Digital Audio Effects*.<br>
[2] sedthh (2024). "BeatLearning". [https://github.com/sedthh/BeatLearning](https://github.com/sedthh/BeatLearning)<br>
[3] Madmom documentation [https://madmom.readthedocs.io/en/latest/]<br>
[4] Cytoid Wiki: Creating a Level [https://github.com/Cytoid/Cytoid/wiki/a.-Creating-a-level]<br>
[5] Cytoid Assets Reference [https://github.com/Cytoid/Cytoid/tree/main/Assets/StaticResources/Sprites]<br>