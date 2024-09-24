from datasets import load_dataset
import pandas as pd
import nltk
import os

def preprocess(text, punctuation_marks):
    """Remove the punctuation specified by the user.
    Return the same string without the unwanted characters.

    Parameters:
    - 'text' (str): string to process and remove characters from.
    - 'punctuation marks' (list): characters to be removed. It can be any number of characters."""

    for character in punctuation_marks: #iterating over the characters given in the parameter list 'punctuation_marks'
        text = text.replace(character, '') #the characters given will be removed from the string by replacing them with empty strings ''
    preprocessesed_text = text #assigning the variable text to a new variable so that it returns the text with all the instances of the punctuation marks removed.
    return preprocessesed_text


def tokenize_and_count(sentences):
    """
    Tokenize each sentence in a list of sentences and calculate the total number of tokens.
    Print the total number of tokens across all sentences in the list.

    Parameters:
    - 'sentences' (list of str): A list of sentences.
    """
    
    # Tokenizing each sentence
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    
    # Calculate the total number of tokens
    total_tokens = sum(len(tokens) for tokens in tokenized_sentences)

    print(f"Total number of tokens: {total_tokens}")

def data_to_csv(file_path, dataset_name="abisee/cnn_dailymail", dataset_version="1.0.0", dataset_split="train[:10000]", remove_chars=None):
    """
    Load a portion of a specified dataset version, process the articles by splitting them into sentences,
    clean the sentences by passing characters, count the total tokens in dataset,
    and save the sentences into a CSV file.

    Parameters:
    - file_path (str): The path where the CSV will be saved.
    - dataset_name (str): The name of the dataset to load (default is 'abisee/cnn_dailymail').
    - dataset_version (str): The version of the dataset to load (default is '1.0.0').
    - dataset_split (str): The split/portion of the dataset to load (default is 'train[:10000]').
    - remove_chars (list of str): List of characters to remove during preprocessing (default is None).
    """

    # Loading a portion of the dataset
    print(f"Loading dataset: {dataset_name}, version: {dataset_version}, split: {dataset_split}")
    ds = load_dataset(dataset_name, dataset_version, split=dataset_split)
    print("Dataset loaded")

    # Convert dataset to DataFrame
    df = pd.DataFrame(ds)

    # Separating sentences
    df['sentences'] = df['article'].apply(nltk.sent_tokenize)
    print("Articles separated into sentences")

    # Making a single list of all the sentences in each article
    sentences = sum(df['sentences'].tolist(), [])

    # Removing specified characters for cleaner text
    if remove_chars is None:
        remove_chars = []  # set to an empty list if no characters are specified
        cleaned_sentences = sentences
    
    else:
        cleaned_sentences = [preprocess(sent, remove_chars) for sent in sentences]
    print(f"Removed specified characters from sentences: {remove_chars}")

    #print the total number of tokens
    tokenize_and_count(cleaned_sentences)

    # Ensure the data directory exists
    if not os.path.exists("data"):
        os.mkdir("data")

    # Convert the list into a df and save to csv file
    df = pd.DataFrame(cleaned_sentences, columns=["sentences"])
    df.to_csv(f"data/{file_path}", index=False, encoding='utf-8')
    print(f"Data saved to {file_path}")
