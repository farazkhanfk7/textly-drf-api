import torch
from transformers import BertTokenizer
from transformers import BertForSequenceClassification
from pytorch_transformers import GPT2Tokenizer, GPT2LMHeadModel
from textblob import TextBlob



def check_grammer(sentence : str) -> str:
    """
    Runs grammer_check model and returns Correct/Incorrect.
    :param sentence: sentence taken from serializer.data.
    :return: Correct or Incorrect
    """
    output_dir = './models/grammer_check'
    tokenizer = BertTokenizer.from_pretrained(output_dir)
    model_loaded = BertForSequenceClassification.from_pretrained(output_dir)

    sent = sentence
    encoded_dict = tokenizer.encode_plus(
                            sent, 
                            add_special_tokens = True,
                            max_length = 64,
                            pad_to_max_length = True,
                            return_attention_mask = True,
                            return_tensors = 'pt',
                    )
            
    input_id = encoded_dict['input_ids']

    attention_mask = encoded_dict['attention_mask']
    input_id = torch.LongTensor(input_id)
    attention_mask = torch.LongTensor(attention_mask)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_loaded = model_loaded.to(device)
    input_id = input_id.to(device)
    attention_mask = attention_mask.to(device)

    with torch.no_grad():
        outputs = model_loaded(input_id, token_type_ids=None, attention_mask=attention_mask)

    logits = outputs[0]
    index = logits.argmax()
    if index == 1:
        result = "Gramatically correct"
    else:
        result = "Gramatically in-correct"

    return result


def check_sentiment(sentence : str) -> str:
    """
    Runs sentiment_analysis model and returns Positive/Negative.
    :param sentence: sentence taken from serializer.data.
    :return: Positive or Negative
    """
    output_dir = './models/sentiment'
    tokenizer = BertTokenizer.from_pretrained(output_dir)
    model_loaded = BertForSequenceClassification.from_pretrained(output_dir)

    sent = sentence
    encoded_dict = tokenizer.encode_plus(
                        sent, 
                        add_special_tokens = True,
                        max_length = 64,
                        pad_to_max_length = True,
                        return_attention_mask = True,
                        return_tensors = 'pt',
                   )
        
    input_id = encoded_dict['input_ids']

    attention_mask = encoded_dict['attention_mask']
    input_id = torch.LongTensor(input_id)
    attention_mask = torch.LongTensor(attention_mask)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_load = model_loaded.to(device)
    input_id = input_id.to(device)
    attention_mask = attention_mask.to(device)

    with torch.no_grad():
        outputs = model_load(input_id, token_type_ids=None, attention_mask=attention_mask)

    logits = outputs[0]
    index = logits.argmax()

    if index == 1:
        result = "Positive"
    else:
        result = "Negative"

    return result
    
def get_textgen(sentence : str) -> str:
    """
    Runs text_generation GPT2 model and returns generated text.
    :param sentence: sentence taken from serializer.data.
    :return: Generated text.
    """
    output_dir = './models/text_gen'
    tokenizer = GPT2Tokenizer.from_pretrained(output_dir)
    model = GPT2LMHeadModel.from_pretrained(output_dir)
    tokens = tokenizer.encode(sentence)
    tokens_tensor = torch.tensor([tokens])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokens_tensor = tokens_tensor.to(device)
    model.to(device)
    with torch.no_grad():
        outputs = model(tokens_tensor)
        predictions = outputs[0]
    predicted_index = torch.argmax(predictions[0,-1,:]).item()
    predicted_text = tokenizer.decode(tokens + [predicted_index])
    return predicted_text
    

def get_correct_sentence(data : dict) -> str:
    """
    Use TextBlob to correct spellings.
    :param data: data generated by serializer.data.
    :return: Corrected text.
    """
    try:
        sentence = data["sentence"]
        words = [i for i in sentence.split()]
        corrected_words = [str(TextBlob(i).correct()) for i in words]
        final_sentence = ' '.join(corrected_words)
        return final_sentence
    except Exception:
        raise KeyError
    


def get_grammer_gif(sentence : str) -> str:
    if sentence == "Gramatically correct":
        return f"https://tetranoodle.com/wp-content/uploads/2018/07/tick-gif.gif"

    else:
        return f"https://www.hireteacher.com/site_assets/img/wrong.gif"


def get_sentiment_gif(sentence : str) -> str:
    if sentence == "Positive":
        return f"https://i.pinimg.com/originals/82/b8/f5/82b8f50de512d0df16f4036c99d8de3e.gif"

    else:
        return f"https://i.pinimg.com/originals/c4/07/04/c4070448ce8174b2b3e121081ddbbee5.gif"