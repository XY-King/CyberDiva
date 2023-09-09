# Re_CharacterAI
A New-era implementation of interaction between human and imaginary characters.

## Running sample character
### Configuration
- fill in your openai api key in the `api_key` field in `config.json`
- fill in your nickname (for the character to call you) and setting of yourself (imagined relationship with the character) in `user.json`. Use `CHARACTER` as the character's name in the description of relationship.
### Live2D setup
- install `Live2DViewerEX` on your computer via Steam
- open `Live2DViewerEX`, click `File` -> `Import Model Data` -> `Import Model Data (JSON)`. Use the `model.json` file in `live2d/shirokane_rinko/`. Then, switch to this character.
- toggle the `Remote access`-`Start service` switch in `Live2DViewerEX` to `ON`.
### Run
- Open a command line window under the root directory of this project
- run `python script.py`
- start chatting with the character! You will type in the command line window and see the response in the Live2D window
- type `exit` to exit the conversation

## How to create your own character
## CONFIGURATION
### OpenAI settings
- fill in your openai api key in the `api_key` field in `config.json`
- language of conversation and the GPT engine to use can be changed in `config.json`. Engines with `-16k` suffix are recommended for long conversations.
### Character settings
- fill in the name of the character and the name of the live2d in `chara.json`
  
## ASSETS
### Characters
Put the character's json file under `/characters` directory. The json file name should be `{CHARACTER'S_NAME}.json`. 
The json file should contain the following fields:
- `is_embedded`: if the character's json file is created or changed since the last run, set this to `false`. Otherwise, set this to `true` (default).
- `name`: the name of the character
- `introduction`: the introduction of the character
- `response_depth`: how much information will there be in the character's response. `1` is recommended for child-like characters. `2` or higher is recommended for normal characters. `3` or higher is recommended for characters who are particularly intellectual or wise.

**IMPORTANT: Fields that can show the way of speaking of the character, background story of the character, etc is REQUIRED to be included in the json file.**

For these fields, the key should be the name of the field, and the value should be a list of strings that you prepared.

For example: "examples_of_sayings": ["example 1", "example 2", "example 3"]

More detailed information can be found in the three sample characters' json files under `/characters` directory. Ignore the `xxx_embedded.json` files, which are for program use only and will be automatically generated from the original json files when the program is run.

### Live2D
Put the Live2D directory under the `/live2d` directory. The Live2D directory name should be `{LIVE2D_NAME}`.

The Live2D directory should be in Cubism 2 format. Essential files include:
- `model.json`
- `model.moc`
- texture image file
- `physics.json`
- `motions` directory

**IMPORTANT: The `motion` field in `model.json` must be filled. The reference to motion files should be meaningful.**

This is to make the live2d react with the character's response.

To get interaction with your character when running this program, you should have purchased and installed `Live2DViewerEX` on your computer via Steam.

In `Live2DViewerEX`, open the character you want to use, and click `File` -> `Import Model Data` -> `Import Model Data (JSON)`. Use the `model.json` file in the character's Live2D directory. Then, switch to this character.

**IMPORTANT: Toggle the `Remote access`-`Start service` switch in `Live2DViewerEX` to `ON`.**

A sample Live2D directory is provided under `/live2d` directory of `Shirokane Rinko` in the game BangDream, only for sample use.

### User
Fill in your nickname (for the character to call you) and setting of yourself (imagined relationship with the character) in `user.json`.

## How to run
- Open a command line window under the root directory of this project
- run `python script.py`
- start chatting with the character! You will type in the command line window and see the response in the Live2D window
- type `exit` to exit the conversation