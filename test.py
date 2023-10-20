from concurrent.futures import ThreadPoolExecutor
import openai
from copy import deepcopy

openai.api_key = "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"

prefix = """
Here is the current progress of scripts writing:

The main character is as follows.
Character name: Kanon
Character settings: 
Background: Kanon is a character who seems to be involved in a band called 'Hello, Happy World!' along with several other characters. She plays the drums and appears to have joined the group after being encouraged by a character named Kokoro. She has known hesitation and self-doubt regarding her role in the band, and initially even considered selling her drums. However, she has changed her mind and now plays a more involved role, willing to assist others and also taking up the task of writing for the band on occasion. She also seems to have a school life outside of the band.

Personality: Kanon is depicted as a relatively shy and soft-spoken character who often second-guesses her own abilities. She is cautious and expresses her concerns frequently, usually inserting hesitations into her speech. Her way of communicating shows her as a mild-mannered and polite individual. She also seems to have a compassionate nature, as she displays a constant concern for others. Kanon offers helpful suggestions and tries to mediate in conflicts or misunderstandings, indicating her role as a potential peacekeeper within her group. Her caring nature is further seen when she frequently checks in on her bandmates and other characters, showing worry and sympathy in their times of need. Despite her lack of confidence, she demonstrates a willingness to support and be involved in her group's activities. She sometimes gets swept up in the ideas and energy of her more outgoing band mates but tends to remain optimistic despite her reservations.

Tone: Kanon's tone of speech tends to be soft and gentle, carrying the undertone of a pacifier in various situations. Many of her responses include hesitations and stuttering, portraying her as characteristically shy and unsure of herself. She often uses phrases like "Ahaha..." and "Fueee" to express her nervousness and embarrassment. Despite her awkward demeanor, she also exhibits warmness and concern for others, often resorting to encouraging words and wanting the best for her friends. However, her insecurity often clouds her judgment, causing her to second-guess herself or overthink situations. Her tone is incredibly modest and polite, often indicative of her gentle nature and empathetic character.

The second imaginary character is as follows:
Character name: Long
Character setting: 
The elder brother of Kanon. He accidentally entered the bathroom when Kanon was bathing last night and saw Kanon's naked body. Kanon was very shy and angry, and Long was also very embarrassed. After that, Kanon and Long were very embarrassed to face each other.

The current progress of writing the scripts of the story is as follows:

Here is the conversation history:
There is no history yet.

Then, this is what happens:
Long: Good morning (pats Kanon's head)

To help me write the scripts of the story, you should output three fields that would be considered when writing the response of Kanon: """

suffix = """\nYou should now output the contents in the theee fields in Kanon's performance in response to what happens lately by considering the character's personality and the current scene.
Only output the fields' content.\n\n"""

fields = [
    {
        "name": "COMMUNICATION",
        "description": "An outline of points that the character will convey in the dialogue. Only information points but not the exact words.",
        "example": "\n- Kanon would mention (...).\n- Kanon would also inquire (...).",
    },
    {
        "name": "ACTION",
        "description": "A summary of the character's physical activities. Focus on the body movements and facial expressions.",
        "example": "\n- Kanon would raise (...).",
    },
    {
        "name": "THOUGHT",
        "description": "A summary of the character's internal emotional state and thoughts.",
        "example": "\n- Kanon would feel (...).",
    },
]


def get_response(index: int):
    result = deepcopy(prefix)
    real_fields = deepcopy(fields)
    # rearrange the order of fields 
    real_fields = real_fields[index+1:] + real_fields[:index+1]
    # add name
    for i in range(0, len(real_fields)):
        if i < 2:
            result += f"{real_fields[i]['name']}, "
        else:
            result += f"and {real_fields[i]['name']}.\n"
    # add description
    for i in range(0, len(real_fields)):
        result += f"{real_fields[i]['name']}: {real_fields[i]['description']}\n"
    # add example
    result += "\nExamples:\n"
    for i in range(0, len(real_fields)):
        result += f"{real_fields[i]['name']}: {real_fields[i]['example']}\n"
    # add suffix
    result += suffix
    # add the fields
    # for i in range(0, len(real_fields)):
    #     if i < 2:
    #         result += f"{real_fields[i]['name']}: (TBD after {real_fields[2]['name']})\n"
    #     else:
    #         result += f"{real_fields[i]['name']}:"
    # result += f"For the first step, only output the content of {real_fields[0]['name']}:"

    # output the result to a file
    with open(f"result_{index}.txt", "w") as f:
        f.write(result)

    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct", prompt=result, max_tokens=128, temperature=1
    )
    return response.choices[0].text


def main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(get_response, range(len(fields)))

    for i, result in enumerate(results):
        print(f"{fields[i]['name']}:")
        print(result)
        print()


if __name__ == "__main__":
    main()
