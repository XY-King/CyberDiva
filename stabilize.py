import json
import os
from utils import with_embedding
import time

SAYINGS = [
    {"time": "2023/10/03 8:00", "content": "Good morning"},
    {"time": "2023/10/03 8:01", "content": "Today's weather is nice"},
    {"time": "2023/10/03 12:00", "content": "Would you like to have lunch with me?"},
    {"time": "2023/10/03 13:00", "content": "What's your plan next?"},
    {"time": "2023/10/03 18:00", "content": "Would you like to have dinner with me?"},
    {"time": "2023/10/03 24:00", "content": "Good night"},
    {"time": "2023/10/04 8:00", "content": "(The next day comes)"},
]

THOUGHT_TURNS = 5
TONE_TURNS = 10


def read_stabilizer(self):
    name = self.chara["name"]
    if not os.path.exists(f"characters/{name}/stabilizer.json"):
        stabilize(self)
    with open(f"characters/{name}/stabilizer.json", "r") as f:
        stabilizer = json.load(f)
    self.history = stabilizer["history"]


def stabilize(self):
    for saying_data in SAYINGS:
        saying = saying_data["content"]
        if saying_data == SAYINGS[-1]:
            self.user_input(saying, nohuman=True, timing=saying_data["time"])
        else:
            self.user_input(saying, timing=saying_data["time"])
        mid_results = []
        results = []
        while True:
            for i in range(THOUGHT_TURNS):
                if self.setting["model"] == "gpt-4":
                    # sleep for 10 second to avoid the 429 error
                    time.sleep(10)
                mid = self.get_response(is_stable=False)
                mid_results.append(mid)

            for i, result in enumerate(mid_results):
                print(f"{i + 1}: {result}\n")
            mid_index = input("\nWhich one is the best? ")
            mid_index = int(mid_index) - 1
            if mid_index in range(len(mid_results)):
                break
        # output the result to a file and wait for the user to modify it
        with open("mid_results.txt", "w") as f:
            f.write(mid_results[mid_index])
        input(
            "Please modify the result in mid_results.json and press enter to continue"
        )
        with open("mid_results.txt", "r") as f:
            mid_results[mid_index] = f.read()
        while True:
            for i in range(TONE_TURNS):
                self.add_response(mid_results[mid_index], is_stable=False)
                res = self.history[-1]
                results.append(res)
                self.history.pop()

            for i, result in enumerate(results):
                print(f"{i + 1}: {result['content']}")
            final_index = input("\nWhich one is the best? ")
            final_index = int(final_index) - 1
            if final_index in range(len(results)):
                break

        self.history.append(results[final_index])

    name = self.chara["name"]
    stabilizer = {}
    stabilizer["history"] = self.history
    with open(f"characters/{name}/stabilizer.json", "w") as f:
        json.dump(stabilizer, f, indent=4)
