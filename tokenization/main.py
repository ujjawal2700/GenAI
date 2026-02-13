import tiktoken
enc = tiktoken.get_encoding("o200k_base")
assert enc.decode(enc.encode("hello world")) == "hello world"
enc = tiktoken.encoding_for_model("gpt-4o")

print(enc.encode("hello my name is ujjawal mahawar."))

text = [24912, 922, 1308, 382, 337, 41699, 117209, 16747, 99155, 13]

output = enc.decode(text)
print(output)
