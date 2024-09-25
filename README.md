# Baby LM for English and Rioplatense Spanish

This repository contains code to train a language model with limited data. Following the BabyLM Challenge (Warstadt et al., 2023), a model is trained with English data and another one with Rioplatense Spanish data, both in the news domain. 

**How to run this repository:**

Download this repository and place it in your Google Drive under a folder called `Colab Notebooks`.

## English BabyLM

`BabyTraining_EN.ipynb`

Run this notebook on Colab to train an LM with 7B tokens of English data.

The dataset used is version 1.0.0. of the CNN/DailyMail Dataset (See et al., 2017).

Since the dataset is already cleaned in this repository, it is not necessary to run the `data_to_csv()` function in the first cell.

The notebook can be run from the following cell onwards to train the LM:
`df = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/baby-lm/data/EN_sentences.csv")` 


## Spanish BabyLM

*In progress*




