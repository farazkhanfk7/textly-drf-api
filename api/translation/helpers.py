# Helper functions for translation model 
import spacy
import torch
from torchtext.data import Field,BucketIterator
from torchtext.datasets import Multi30k
import torchtext

spacy_german = spacy.load('de')
spacy_english = spacy.load('en')


def tokenize_german(text):
    return [token.text for token in spacy_german.tokenizer(text)]

def tokenize_english(text):
    return [token.text for token in spacy_english.tokenizer(text)]


german = Field(
    tokenize = tokenize_german,
    lower = True,
    init_token = '<sos>',
    eos_token = '<eos>'
)
english = Field(
    tokenize = tokenize_english,
    lower = True,
    init_token = '<sos>',
    eos_token = '<eos>'
)

train_data,valid_data,test_data = Multi30k.splits(exts=('.de','.en'),fields=(german,english))

german.build_vocab(train_data,max_size=10000,min_freq = 3)
english.build_vocab(train_data,max_size=10000,min_freq = 3)


def translate_sentence(model, sentence, german, english, device, max_length=50):
    spacy_ger = spacy.load("de")

    if type(sentence) == str:
        tokens = [token.text.lower() for token in spacy_ger(sentence)]
    else:
        tokens = [token.lower() for token in sentence]
    tokens.insert(0, german.init_token)
    tokens.append(german.eos_token)
    text_to_indices = [german.vocab.stoi[token] for token in tokens]
    sentence_tensor = torch.LongTensor(text_to_indices).unsqueeze(1).to(device)

    # Build encoder hidden, cell state
    with torch.no_grad():
        hidden, cell = model.EncoderLSTM(sentence_tensor)

    outputs = [english.vocab.stoi["<sos>"]]

    for _ in range(max_length):
        previous_word = torch.LongTensor([outputs[-1]]).to(device)

        with torch.no_grad():
            output, hidden, cell = model.DecoderLSTM(previous_word, hidden, cell)
            best_guess = output.argmax(1).item()

        outputs.append(best_guess)

        # Model predicts it's the end of the sentence
        if output.argmax(1).item() == english.vocab.stoi["<eos>"]:
            break

    translated_sentence = [english.vocab.itos[idx] for idx in outputs]
    return translated_sentence[1:]