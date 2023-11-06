# CyberDiva
A New-era implementation of interaction between human and imaginary characters. Utilizing GPT series models and Live2D.

## Running sample character: Shirokane Rinko (Rinko)
### Preparation
- fill in your openai api key in the `api_key` field in `json/config.json`
- fill in your nickname (for the character to call you) and setting of yourself (imagined relationship with the character) in `json/user.json`. 
### Run
- Open a command line window under the root directory of this project
- Run `python main.py`
- Chat with the character in the window that pops up. You can drag the window by dragging the purple circle.

## PROGRAM CONFIGURATION
### OpenAI settings
- Fill in your openai api key in the `api_key` field in `json/config.json`
- GPT engine to use can be changed in `json/config.json`. 
| Model                  | Pros and Cons                                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------------------------- |
| gpt-instruct-turbo-3.5 | Default model chosen. Responds very fast and features lively conversations.                             |
| text-davinci-003       | Responds slower, but behaves better on tasks that can be considered as inappropriate. (e.g. light porn) |

### Character settings
- fill in the name of the character in `json/chara.json`. The character should exist under `/characters` directory.
  
## CUSTOMIZATION
### How to create your own character
Create a directory with the name of the character under `/characters` directory, e.g. `/characters/Rinko`.
Then, put the following files/directory under the directory:
- `model.json`: Configuration of the character
- `examples.json`: Examples of interaction with the character
- `live2d`: Live2D directory of the character

### model.json
The `model.json` file should contain the following fields:
- `name`: Name of the character
- `introduction`: Introduction of the character. You shall consider the background, personality, and tone of the character in this field.
- Other fields that can show the **way of speaking**, background story, knowledge, etc of the character. E.g. `sample dialogues exemplifying personality and tone`, `background stories`, etc. The content of these fields should be **list** of string.

**IMPORTANT: such fields are HIGHLY RECOMMENDED to create a lively character and make the character behave in a desirable way.**
See the characters under `/characters` directory for examples.

### examples.json
The `examples.json` file should be lists of dicts, each dict containing the following fields:
- `message`: The message sent to the character
- `fields`: The fields describing character's state, including `THOUGHT` and `ACTION`
- `performance`: The response of the character

This file is important for you to have a stable conversation with the character. 

You do not need to create such files at the beginning of character creation by yourself. When chosen a character without this file, you only need to follow the instructions in the window to create this file.

### live2d/
The Live2D directory should be in Cubism 2 format. Essential files include:
- `model.json`
- `model.moc`
- `physics.json`
- `motions` directory
- texture image file

**IMPORTANT: The `motion` field in `model.json` must be filled. The reference to motion files should be a description of the motion to be played.**

For example:
```characters/Rinko/live2d/model.json
...
"motions": {
    "feel angry, pull her own sleeves, looking away to show her disatisfication": [
        {
            "file": "motions/angry01.mtn"
        }
    ],
    "showing goodbye, holding her hands together, looking down, nodding": [
        {
            "file": "motions/bye01.mtn"
        }
    ],
...
}
...
```

[BangdreamLive2DExtractor](https://github.com/KinXY/BangdreamLive2dExtractor) is a great tool to extract Live2D files from Bangdream game and naming the motions of the Live2D model.