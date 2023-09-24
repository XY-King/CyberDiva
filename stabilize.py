import json

SAYINGS = [
    "Good morning",
    "Today's weather is nice", 
    "Would you like to have lunch with me?",
    "What's your plan next?", 
    "Would you like to have dinner with me?",
    "Good night", 
    "(The next day comes)"
]

TURNS = 3

def stabilize(self):
    for saying in SAYINGS:
        mid_results = []
        results = []
        while True:
            for i in range(TURNS):
                if saying == SAYINGS[-1]:
                    self.user_input(saying, nohuman=True)
                else:
                    self.user_input(saying)
                response = self.get_response()
                self.add_response(response=response)

                mid = self.history[-1]
                final = self.real_history[-1]
                mid_results.append(mid)
                results.append(final)

                self.history = []
                self.real_history = []
            for i, result in enumerate(results):
                print(f"{i + 1}: {result['content']}")
            index = input("\nWhich one is the best? ")
            index = int(index) - 1
            if index in range(len(results)):
                break
        self.history.append(mid_results[index])
        self.real_history.append(results[index])

    name = self.chara["name"]
    stabilizer = {}
    prefix_length = len(self.history) - len(self.real_history)
    stabilizer["history"] = self.history[prefix_length:]
    stabilizer["real_history"] = self.real_history
    with open(f"characters/{name}/stabilizer.json", "w") as f:
        json.dump(stabilizer, f, indent=4)
        