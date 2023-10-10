import json

stable = json.load(open('characters/Rinko/stabilizer.json', 'r', encoding='UTF-8'))
history = stable['history']

for msg in history:
    msg.pop('embedding')

with open('history.txt', 'w', encoding='UTF-8') as f:
    for msg in history:
        if msg["role"] == "user":
            role = 'Long'
        else:
            role = 'Rinko'
        f.write(f'{role}: {msg["content"]}\n\n')