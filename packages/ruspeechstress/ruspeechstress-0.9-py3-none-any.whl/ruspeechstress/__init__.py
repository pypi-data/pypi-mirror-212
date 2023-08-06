import os
from .stress_detector import StressDetector, FEATURES
from .dataset import dataset
import numpy as np


def create_dataset(dataset_dir=None, dictionary_path=None):
    dataset(dataset_dir=dataset_dir, dictionary_path=dictionary_path, mode='collect_dataset')


def train_model(working_dir=os.getcwd(), clf=None):
    wav_path = os.path.join(working_dir, 'wav_tg_all')
    sd = StressDetector(wav_path, FEATURES)
    sd.get_features('./data/complete_features.tsv')
    evaluation = sd.train(clf())
    print(f'F1 Score: {np.mean(evaluation["f1"])}')


def extend_dictionary(dataset_dir=None, dictionary_path='/home/sivh/thesis/zaliznyak.txt'):
    dataset(dataset_dir=dataset_dir, dictionary_path=dictionary_path, mode='extend_dictionary')