import json
import os
from utils import with_embedding

SAYINGS = [
    "Good morning",
    "Today's weather is nice",
    "Would you like to have lunch with me?",
    "What's your plan next?",
    "Would you like to have dinner with me?",
    "Good night",
    "(The next day comes)",
]

TURNS = 10


def read_stabilizer(self):
    name = self.chara["name"]
    if not os.path.exists(f"characters/{name}/stabilizer.json"):
        stabilize(self)
    with open(f"characters/{name}/stabilizer.json", "r") as f:
        stabilizer = json.load(f)
    self.history = stabilizer["history"]
    self.real_history = stabilizer["real_history"]


def stabilize(self):
    for saying in SAYINGS:
        if saying == SAYINGS[-1]:
            self.user_input(saying, nohuman=True)
        else:
            self.user_input(saying)
        mid_results = []
        results = []
        while True:
            for i in range(TURNS):
                mid = self.get_response()
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
            for i in range(TURNS):
                self.add_response(mid_results[mid_index])
                res = self.real_history[-1]
                results.append(res)
                self.history.pop()
                self.real_history.pop()

            for i, result in enumerate(results):
                print(f"{i + 1}: {result['content']}")
            final_index = input("\nWhich one is the best? ")
            final_index = int(final_index) - 1
            if final_index in range(len(results)):
                break

        self.history.append(
            with_embedding(
                {
                    "role": "assistant",
                    "content": mid_results[mid_index],
                }
            )
        )
        self.real_history.append(results[final_index])

    name = self.chara["name"]
    stabilizer = {}
    stabilizer["history"] = self.history
    stabilizer["real_history"] = self.real_history
    with open(f"characters/{name}/stabilizer.json", "w") as f:
        json.dump(stabilizer, f, indent=4)
