from charaChat import get_index

test = "hello [world] [hello] world"
print(get_index("[", test))
print(get_index("]", test))