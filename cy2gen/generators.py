import json
import numpy as np
import uuid
from pydub import AudioSegment

class CytoidLevelGenerator:
    def __init__(self, bpm, fbt, ebt, time_base=480):
        self.bpm = bpm
        self.fbt = fbt
        self.ebt = ebt
        self.time_base = time_base

    def generate_chart(self, pattern="tap", note_start_side="right", output_path="../contents/ex.json"):
        end_time_ms = self.ebt * 1000 # when will note generation end
        start_time_ms = self.fbt * 1000 # when will note generation start
        us_per_beat = 60 * 1_000_000 / self.bpm
        tick_ms = (us_per_beat / self.time_base) / 1000 # one tick represent how many ms
        page_length = self.time_base * 2 # how many ticks there are in one page

        note_end_tick = round(end_time_ms / tick_ms)
        note_start_tick = round(start_time_ms / tick_ms)

        # generate page_list
        page_list = []
        direction = -1 # start from judgement line scanning downward
        current_tick = 0
        while current_tick < note_end_tick:
            page_list.append({
                "start_tick": current_tick,
                "end_tick": current_tick + page_length,
                "scan_line_direction": direction
            })
            direction *= -1
            current_tick += page_length

        # confirm chart pattern
        if pattern in ["bullet", "stream"]:
            if note_start_side == "left":
                pattern = f"l{pattern}"
            elif note_start_side == "right":
                pattern = f"r{pattern}"

        # generate note_list according to the pattern
        if pattern == "tap": # just casually tapping some quarters
            note_list = []
            note_id = 0

            # positioning note according to page_list
            for page_idx, page in enumerate(page_list):
                start_tick = page["start_tick"]
                end_tick = page["end_tick"]

                if end_tick < note_start_tick: # skip the first several pages
                    continue

                # find out chart local offset
                if start_tick <= note_start_tick <= end_tick:
                    tick_diff = note_start_tick - start_tick
                    offset = tick_diff * tick_ms / 1000

                tick_positions = [start_tick, (start_tick + end_tick) // 2] # generate quarters
                for tick in tick_positions:
                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick,
                        "x": float(np.random.uniform(0.08, 0.92)), # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1

        elif pattern == "drill": # semiquavers forming a vertical line
            note_list = []
            note_id = 0
            x_i_prev = None

            # positioning note according to page_list
            for page_idx, page in enumerate(page_list):
                start_tick = page["start_tick"]
                end_tick = page["end_tick"]

                if end_tick < note_start_tick:  # skip the first several pages
                    continue

                # find out chart local offset
                if start_tick <= note_start_tick <= end_tick:
                    tick_diff = note_start_tick - start_tick
                    offset = tick_diff * tick_ms / 1000

                while True:
                    x_i = float(np.random.uniform(0.08, 0.92))
                    if x_i_prev is None or abs(x_i_prev - x_i) > 0.15:
                        break

                tick_positions = [round(start_tick + i * (end_tick - start_tick) / 8) for i in range(8)]
                for tick in tick_positions:
                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick,
                        "x": x_i,
                        # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1
                x_i_prev = x_i

        elif pattern == "rbullet": # semiquavers but alternatively 2 in left and 2 in right
            note_list = []
            note_id = 0
            x_r_prev = None
            x_l_prev = None
            # positioning note according to page_list
            for page_idx, page in enumerate(page_list):
                start_tick = page["start_tick"]
                end_tick = page["end_tick"]

                # skip the first several pages
                if end_tick < note_start_tick:
                    continue

                # find out chart local offset
                if start_tick <= note_start_tick <= end_tick:
                    tick_diff = note_start_tick - start_tick
                    offset = tick_diff * tick_ms / 1000

                # confirm note positions for left and right side
                while True:
                    x_r = float(np.random.uniform(0.3, 0.92))
                    x_l = float(np.random.uniform(0.08, 0.7))
                    if (x_r_prev is None and x_l_prev is None and x_r - x_l > 0.3) or (abs(x_r - x_l > 0.15) and abs(x_r - x_r_prev) > 0.08 and abs(x_l - x_l_prev) > 0.08 and x_r > x_l):
                        break

                tick_positions = [round(start_tick + i * (end_tick - start_tick) / 2) for i in range(2)]
                for tick in tick_positions:
                    # right hand-side notes
                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick,
                        "x": x_r,
                        # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1

                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick + (end_tick - start_tick) / 8,
                        "x": x_r,
                        # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1

                    # left hand-side notes
                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick + (end_tick - start_tick) / 4,
                        "x": x_l,
                        # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1

                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick + 3 * (end_tick - start_tick) / 8,
                        "x": x_l,
                        # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1

                x_r_prev = x_r
                x_l_prev = x_l

        elif pattern == "lbullet": # bullet starting from left side
            note_list = []
            note_id = 0
            x_r_prev = None
            x_l_prev = None

            # positioning note according to page_list
            for page_idx, page in enumerate(page_list):
                start_tick = page["start_tick"]
                end_tick = page["end_tick"]

                # skip the first several pages
                if end_tick < note_start_tick:
                    continue

                # find out chart local offset
                if start_tick <= note_start_tick <= end_tick:
                    tick_diff = note_start_tick - start_tick
                    offset = tick_diff * tick_ms / 1000

                # confirm note positions for left and right side
                while True:
                    x_r = float(np.random.uniform(0.3, 0.92))
                    x_l = float(np.random.uniform(0.08, 0.7))
                    if (x_r_prev is None and x_l_prev is None and x_r - x_l > 0.3) or (abs(x_r - x_l) > 0.15 and abs(x_r - x_r_prev) > 0.08 and abs(x_l - x_l_prev) > 0.08 and x_r > x_l):
                        break

                tick_positions = [round(start_tick + i * (end_tick - start_tick) / 2) for i in range(2)]
                for tick in tick_positions:
                    # right hand-side notes
                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick,
                        "x": x_l,
                        # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1

                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick + (end_tick - start_tick) / 8,
                        "x": x_l,
                        # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1

                    # left hand-side notes
                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick + (end_tick - start_tick) / 4,
                        "x": x_r,
                        # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1

                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick + 3 * (end_tick - start_tick) / 8,
                        "x": x_r,
                        # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1
                x_r_prev = x_r
                x_l_prev = x_l

        elif pattern == "rstream": # semiquavers alternating by left and right hand-side
            note_list = []
            note_id = 0
            x_r_prev = None
            x_l_prev = None

            # positioning note according to page_list
            for page_idx, page in enumerate(page_list):
                start_tick = page["start_tick"]
                end_tick = page["end_tick"]

                # skip the first several pages
                if end_tick < note_start_tick:
                    continue

                # find out chart local offset
                if start_tick <= note_start_tick <= end_tick:
                    tick_diff = note_start_tick - start_tick
                    offset = tick_diff * tick_ms / 1000

                # confirm note positions
                while True:
                    x_r = float(np.random.uniform(0.3, 0.92))
                    x_l = float(np.random.uniform(0.08, 0.7))
                    if (x_r_prev is None and x_l_prev is None and x_r - x_l > 0.3) or (abs(x_r - x_l) > 0.15 and abs(x_r - x_r_prev) > 0.08 and abs(x_l - x_l_prev) > 0.08 and x_r > x_l):
                        break

                tick_positions = [round(start_tick + i * (end_tick - start_tick) / 4) for i in range(4)]
                for tick in tick_positions:
                    # right hand-side notes
                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick,
                        "x": x_r,
                        # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1

                    # left hand-side notes
                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick + (end_tick - start_tick) / 8,
                        "x": x_l,
                        # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1
                x_r_prev = x_r
                x_l_prev = x_l

        elif pattern == "lstream": # stream but start from left
            note_list = []
            note_id = 0
            x_r_prev = None
            x_l_prev = None

            # positioning note according to page_list
            for page_idx, page in enumerate(page_list):
                start_tick = page["start_tick"]
                end_tick = page["end_tick"]

                # skip the first several pages
                if end_tick < note_start_tick:
                    continue

                # find out chart local offset
                if start_tick <= note_start_tick <= end_tick:
                    tick_diff = note_start_tick - start_tick
                    offset = tick_diff * tick_ms / 1000

                # confirm note positions
                while True:
                    x_r = float(np.random.uniform(0.3, 0.92))
                    x_l = float(np.random.uniform(0.08, 0.7))
                    if (x_r_prev is None and x_l_prev is None and x_r - x_l > 0.3) or (abs(x_r - x_l) > 0.15 and abs(x_r - x_r_prev) > 0.08 and abs(x_l - x_l_prev) > 0.08 and x_r > x_l):
                        break

                tick_positions = [round(start_tick + i * (end_tick - start_tick) / 4) for i in range(4)]
                for tick in tick_positions:
                    # right hand-side notes
                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick,
                        "x": x_l,
                        # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1

                    # left hand-side notes
                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick + (end_tick - start_tick) / 8,
                        "x": x_r,
                        # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1
                x_r_prev = x_r
                x_l_prev = x_l

        elif pattern == "jack": # quavers tapping simultaneously by left and right hand
            note_list = []
            note_id = 0
            x_r_prev = None
            x_l_prev = None

            # positioning note according to page_list
            for page_idx, page in enumerate(page_list):
                start_tick = page["start_tick"]
                end_tick = page["end_tick"]

                # skip the first several pages
                if end_tick < note_start_tick:
                    continue

                # find out chart local offset
                if start_tick <= note_start_tick <= end_tick:
                    tick_diff = note_start_tick - start_tick
                    offset = tick_diff * tick_ms / 1000

                # confirm note positions
                while True:
                    x_r = float(np.random.uniform(0.3, 0.92))
                    x_l = float(np.random.uniform(0.08, 0.7))
                    if (x_r_prev is None and x_l_prev is None and x_r - x_l > 0.3) or (abs(x_r - x_l) > 0.15 and abs(x_r - x_r_prev) > 0.08 and abs(x_l - x_l_prev) > 0.08 and x_r > x_l):
                        break

                tick_positions = [round(start_tick + i * (end_tick - start_tick) / 4) for i in range(4)]
                for tick in tick_positions:
                    # right hand-side notes
                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick,
                        "x": x_r,
                        # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1

                    # left hand-side notes
                    note_list.append({
                        "page_index": page_idx,
                        "type": 0,
                        "id": note_id,
                        "tick": tick,
                        "x": x_l,
                        # randomly positioning quarters(deciding their x value, from 0 most left-side to 1 most right-side)
                        "hold_tick": 0,
                        "next_id": 0
                    })
                    note_id += 1
                x_r_prev = x_r
                x_l_prev = x_l

        else:
            raise ValueError("Invalid chart pattern") # you may enter some patterns that are not supported yet

        # combine final results
        result = {
            "format_version": 3,
            "time_base": self.time_base,
            "start_offset_time": 0,
            "page_list": page_list,
            "tempo_list": [{
                "tick": 0,
                "value": us_per_beat
            }],
            "note_list": note_list
        }

        # write into .json
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        return offset

    def generate_level(self, title="Unknown", artist="Unknown", illustrator="Unknown", difficulty="HARD", output_path="../contents/level.json"):
        # generate level.json according to its official format
        level_data = {
            "schema_version": 2,
            "version": 1,
            "id": f"{title.strip().lower}autogen{uuid.uuid4()}",
            "title": title,
            "artist": artist,
            "illustrator": illustrator,
            "charter": 'AutoGeneratedbyAMR17',
            "music": {
                "path": "audio.mp3"
            },
            "music_preview": {
                "path": "pv.mp3"
            },
            "background": {
                "path": "BG.png"
            },
            "charts": [
                {
                    "type": "extreme" if difficulty == "CHAOS" else "hard" if difficulty == "HARD" else "easy",
                    "name": difficulty,
                    "difficulty": 5 if difficulty == 'EASY' else 15 if difficulty == 'CHAOS' else 10,
                    "path": "ex.json"
                }
            ]
        }
        # write into .json file
        with open(output_path, 'w', encoding="utf-8") as f:
            json.dump(level_data, f, ensure_ascii=False, indent=2)

class MusicConverter:
    def __init__(self, input_path = "../contents/audio.mp3"):
        self.input_path = input_path

    def convert_pv(self, start_time = 25000, duration = 20000):
        # generate pv.mp3 which is a preview before playing the chart
        audio = AudioSegment.from_file(self.input_path)
        preview = audio[start_time:(start_time + duration)]
        preview.export("../contents/pv.mp3", format="mp3")