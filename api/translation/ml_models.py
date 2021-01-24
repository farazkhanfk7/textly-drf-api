import numpy as np
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from tqdm.notebook import tqdm
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
from api.translation.helpers import german,english

#HyperParameters
# Encoder
input_size_encoder = len(german.vocab)
encoder_embedding_size = 300
hidden_size = 1024
num_layers = 2
encoder_dropout = 0.5

# Decoder

input_size_decoder = len(english.vocab)
decoder_embedding_size = 300
decoder_dropout = 0.5
output_size = len(english.vocab)



class EncoderLSTM(nn.Module):
    def __init__(self,input_size,embedding_size,hidden_size,num_layers,p):
        super(EncoderLSTM,self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout = nn.Dropout(p)
        self.tag = True
        self.embedding = nn.Embedding(input_size,embedding_dim=embedding_size) # (5376,300)
        self.LSTM = nn.LSTM(embedding_size,hidden_size,num_layers,dropout = p)
    
    def forward(self,x):
        embedding = self.dropout(self.embedding(x))
        outputs,(hidden_state,cell_state) = self.LSTM(embedding)
        return hidden_state,cell_state


class DecoderLSTM(nn.Module):
    def __init__(self,input_size,embedding_size,hidden_size,num_layers,p,output_size):
        super(DecoderLSTM,self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout = nn.Dropout(p)
        self.output_size = output_size
        self.embedding = nn.Embedding(input_size,embedding_dim=embedding_size)
        self.LSTM = nn.LSTM(embedding_size,hidden_size,num_layers,dropout = p)
        self.fc = nn.Linear(hidden_size,output_size)
    
    def forward(self,x,hidden_state,cell_state):
        # .unsqueeze() for dimension expansion
        # Shape of x (1, 32) [1, batch_size]
        x = x.unsqueeze(0)
        # Shape -----------> (1, 32, 300) [1, batch_size, embedding dims]
        embedding = self.dropout(self.embedding(x))
        # Shape --> outputs (1, 32, 1024) [1, batch_size , hidden_size]
        # Shape --> (hs, cs) (2, 32, 1024) , (2, 32, 1024) [num_layers, batch_size size, hidden_size] (passing encoder's hs, cs - context vectors)
        outputs,(hidden_state,cell_state) = self.LSTM(embedding,(hidden_state,cell_state))
        # Shape --> predictions (1, 32, 4556) [ 1, batch_size , output_size]
        predictions = self.fc(outputs)
        # Shape --> predictions (32, 4556) [batch_size , output_size]
        predictions = predictions.squeeze(0) # .squeeze() for dimension compression
        return predictions,hidden_state,cell_state


class Seq2Seq(nn.Module):
  def __init__(self, EncoderLSTM, DecoderLSTM):
    super(Seq2Seq, self).__init__()
    self.EncoderLSTM = EncoderLSTM
    self.DecoderLSTM = DecoderLSTM

  def forward(self, source, target, tfr=0.5):
    # Shape - Source : (10, 32) [(Sentence length German + some padding), Number of Sentences]
    batch_size = source.shape[1]

    # Shape - Source : (14, 32) [(Sentence length English + some padding), Number of Sentences]
    target_len = target.shape[0]
    target_vocab_size = len(english.vocab)
    
    # Shape --> outputs (14, 32, 5766) 
    outputs = torch.zeros(target_len, batch_size, target_vocab_size).to(device)

    # Shape --> (hs, cs) (2, 32, 1024) ,(2, 32, 1024) [num_layers, batch_size size, hidden_size] (contains encoder's hs, cs - context vectors)
    hidden_state, cell_state = self.EncoderLSTM(source)

    # Shape of x (32 elements)
    x = target[0] # Trigger token <SOS>

    for i in range(1, target_len):
      # Shape --> output (32, 5766) 
      output, hidden_state, cell_state = self.DecoderLSTM(x, hidden_state, cell_state)
      outputs[i] = output
      best_guess = output.argmax(1) # 0th dimension is batch size, 1st dimension is word embedding
      x = target[i] if random.random() < tfr else best_guess # Either pass the next word correctly from the dataset or use the earlier predicted word

    # Shape --> outputs (14, 32, 5766) 
    return outputs