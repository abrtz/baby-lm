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

Download the evaluation repository and update both scripts (`eval_blimp.sh` and `eval_ewok.sh`) with: \
 change `--model hf` to `--model hf-mlm` \
 change `backend="causal"` to `backend="mlm"`

Run each evaluation the terminal from the root directory of the evaluation repository (`evaluation-pipeline-2024`):

`./eval_blimp.sh <path_to_model>`

`./eval_ewok.sh <path_to_model>`

`<path_to_model>` should be the absolute path to the English BabyLM model folder.

The results are stored under the `results` directory in the `evaluation-pipeline-2024` root directory.


## Spanish BabyLM

### Training

`BabyTraining_ES.ipynb`

Run this notebook on Colab to train an LM with 7M tokens of Rioplatense Spanish data.


The dataset used is the articles and comments dataset from PIUBA (Pérez et al., 2023).

Same as with the English model above, the dataset is already cleaned in earlier steps before training. Therefore, it is not necessary to run the `data_to_csv()` function in the first cell.

The notebook can be run from the following cell onwards to train the LM:
`df = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/baby-lm/data/ES_sentences.csv")` 

### Evaluation

#### Fill Mask

`BabyEvaluation_ES.ipynb`

After training the model, check whether the model trained with the Fill Mask Pipeline (HuggingFace).

#### EWoK

After checking the perfomance of the English model on BLiMP and EWoK, and due to the challenges posed by language-specific focus of BLiMP, EWoK is chosen to evaluate the Rioplatense Spanish model.

**Data creation**

Given the performance of the English model, the following categories are created for Spanish:

- material-dynamics
- material-properties
- social-relations

The datasets are created following the EWoK paper (Ivanova et al., 2024) and tutorial (https://github.com/ewok-core/ewok/tree/main)

The files and templates are provided under the `data/es-ewok` directory in password-protected zips following the recommendation of the authors. The password is the same as the original EWoK password-protected datasets (i.e., ewok). 

Note: Due to the same reason, only the final files are provided and not the templates created with the tutorial.

**Evaluation**

Same as with the English model, the evaluation is done following the Evaluation Pipeline of the 2024 BabyLM challenge: (https://github.com/babylm/evaluation-pipeline-2024?tab=readme-ov-file)

Before running the evaluation, make the following changes in the repository:

- Replace the files under `ewok_filtered` folder with the generated Spanish jsonl files.

- Under `lm_eval/tasks/ewok_filtered` folder, open the file `generate_configs.py` and change `all_subtasks` to the subtasks relevant for Spanish only with the name given in ES: `"material-dinamico", "material-propiedades" "social-relaciones"`. 
Remove any .yaml file remaining from the English evaluation.


Run the evaluation on the terminal from the root directory of the evaluation repository (`evaluation-pipeline-2024`):

`./eval_ewok.sh <path_to_model>`

`<path_to_model>` should be the absolute path to the Rioplatense Spanish BabyLM model folder.

The results are stored under the `results` directory in the `evaluation-pipeline-2024` root directory.




