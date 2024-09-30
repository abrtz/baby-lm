# Baby LM for English and Rioplatense Spanish

This repository contains code to train a language model with limited data. Following the BabyLM Challenge (Warstadt et al., 2023), a model is trained with English data and another one with Rioplatense Spanish data, both in the news domain. 

**How to run this repository:**

Download this repository and place it in your Google Drive under a folder called `Colab Notebooks`.

## English BabyLM

### Training

`BabyTraining_EN.ipynb`

Run this notebook on Colab to train an LM with 7M tokens of English data.

The dataset used is version 1.0.0. of the CNN/DailyMail Dataset (See et al., 2017).

The dataset is already cleaned in earlier steps before training. Therefore, it is not necessary to run the `data_to_csv()` function in the first cell.

The notebook can be run from the following cell onwards to train the LM:
`df = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/baby-lm/data/EN_sentences.csv")` 

### Evaluation

#### Fill Mask

`BabyEvaluation_EN.ipynb`

After training the model, check whether the model trained with the Fill Mask Pipeline (HuggingFace).

#### BLiMP and EWoK

The evaluation on BLiMP and EWoK is done following the Evaluation Pipeline of the 2024 BabyLM challenge: (https://github.com/babylm/evaluation-pipeline-2024?tab=readme-ov-file)

Download the evaluation repository and update both scripts (`eval_blimp.sh` and `eval_ewok.sh`) with:
 change --model hf to --model hf-mlm
 change backend="causal" to backend="mlm"

Run each evaluation the terminal from the root directory of the evaluation repository (`evaluation-pipeline-2024`):

`./eval_blimp.sh <path_to_model>`

`./eval_ewok.sh <path_to_model>`

`<path_to_model>` should be the absolute path to the English BabyLM model folder.

The results are stored under the `results` directory in the `evaluation-pipeline-2024` root directory.


## Spanish BabyLM

*In progress*




