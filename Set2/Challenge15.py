def validate_padding(padded_text):
    padding_length = padded_text[-1]
    return padded_text.count(padding_length) == padding_length


text = b"ICE ICE BABY\x01\x02\x03\x04"
print(validate_padding(text))