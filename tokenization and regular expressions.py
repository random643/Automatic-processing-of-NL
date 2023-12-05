# -*- coding: utf-8 -*-
"""lab1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1moEXTD7HYrePaBz5v4R69qdDJ0YwgQA3
"""

import csv
import re
from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

from google.colab import data_table

from google.colab import drive



test_url = '/content/drive/MyDrive/Lab1/ishoniki/test.csv'
train_url = '/content/drive/MyDrive/Lab1/ishoniki/train.csv'

column_names = ["class", "title", "text"]
df_train = pd.read_csv(train_url, names=column_names)
df_test = pd.read_csv(test_url, names=column_names)

df_train

df_test

import re

def split_sentences(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s(?![a-z])', text)
    return '\n\n'.join(sentences)

import re

# Исходное предложение
sentence = 'Open Source Apps Developer. SugarCRM Releases Sugar.Sales 1.1 (TechWeb)","TechWeb - News - August 13, 2004. Paid Search Growth May Slow","A new Internet advertising forecast shows a slowdown in paid search listings in the next five years. Will the projection affect Google s prospects when it goes public? I often wrote to Dr.Storm at this address refds@gmail.com . What will Mk.Sim and his wife Ms.Sonya say to this?'

# Регулярное выражение для разделения текста на предложения
sentence_pattern = r'(?<=[.!?])\s+'

# Разделяем текст на предложения
sentences = re.split(sentence_pattern, sentence)

# Уберем лишние символы и экранирование в каждом предложении
for i in range(len(sentences)):
    sentences[i] = re.sub(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s(?![a-z])', '', sentences[i])

# Удаление лишних пробелов в каждом предложении
sentences = [' '.join(sentence.split()) for sentence in sentences]


# Вывод результата
for sentence in sentences:
    print(sentence)

import re

# Исходные предложения
sentences = [
    "What will Mk.Sim and his wife Ms.Sonya say to this?",
    "Send your inquiries to contact@example.com for more information."
    "Send your inquiries to rett@example.com for more information."
]

# Регулярное выражение для токенизации, учитывающее сокращения и адреса электронной почты
combined_pattern = r'\b(?:[A-Z][a-z]*\.)+[A-Z][a-z]*\b|\S+@\S+|\w+'

# Обработка каждого предложения и токенизация
for sentence in sentences:
    tokens = re.findall(combined_pattern, sentence)
    print(tokens)

import pandas as pd
import re

# Загрузите DataFrame из файла train_sentences.csv
file_path = '/content/drive/MyDrive/Lab1/promejutok/train_sentences.csv'
df = pd.read_csv(file_path)

# Регулярное выражение для токенизации, учитывающее сокращения и адреса электронной почты
combined_pattern = r'\b(?:[A-Z][a-z]*\.)+[A-Z][a-z]*\b|\S+@\S+|\w+'

# Регулярное выражение для разделения текста на предложения
sentence_pattern = r'(?<=[.!?])\s+'

# Функция для применения регулярных выражений к столбцу
def apply_regex(text):
    # Применяем sentence_pattern
    text = re.sub(sentence_pattern, '', text)
    # Применяем combined_pattern
    text = re.findall(combined_pattern, text)
    # Объединяем результаты в строку
    return ' '.join(text)

# Применяем функцию к столбцу 'sentences' с использованием метода .apply()
df['sentences'] = df['sentences'].apply(apply_regex)

# Выводим первые несколько строк для проверки результата
print(df.head())

# Сохраняем DataFrame в CSV-файл
output_file_path = '/content/drive/MyDrive/Lab1/promejutok/train_sentences_processed.csv'
df.to_csv(output_file_path, index=False)

import pandas as pd
import re

# Загрузите DataFrame из файла train_sentences.csv
file_path2 = '/content/drive/MyDrive/Lab1/promejutok/test_sentences.csv'
df2 = pd.read_csv(file_path2)

# Регулярное выражение для токенизации, учитывающее сокращения и адреса электронной почты
combined_pattern = r'\b(?:[A-Z][a-z]*\.)+[A-Z][a-z]*\b|\S+@\S+|\w+'

# Регулярное выражение для разделения текста на предложения
sentence_pattern = r'(?<=[.!?])\s+'

# Функция для применения регулярных выражений к столбцу
def apply_regex(text):
    # Применяем sentence_pattern
    text = re.sub(sentence_pattern, '', text)
    # Применяем combined_pattern
    text = re.findall(combined_pattern, text)
    # Объединяем результаты в строку
    return ' '.join(text)

# Применяем функцию к столбцу 'text' с использованием метода .apply()
df2['sentences'] = df2['sentences'].apply(apply_regex)

# Выводим первые несколько строк для проверки результата
print(df2.head())

# Сохраняем DataFrame в CSV-файл
output_file_path = '/content/drive/MyDrive/Lab1/promejutok/test_sentences_processed.csv'
df2.to_csv(output_file_path, index=False)

import nltk
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')

snowball_stemmer_obj = SnowballStemmer('english')
lemmatizer = WordNetLemmatizer()

full_df = pd.concat([df, df2])
output_file_path = '/content/drive/MyDrive/Lab1/promejutok/full_df.csv'
df.to_csv(output_file_path, index=False)

full_df

"""TECT"""

import os
from google.colab import drive
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer
from IPython.display import clear_output

nltk.download('wordnet')

snowball_stemmer_obj = SnowballStemmer('english')
lemmatizer = WordNetLemmatizer()

import pandas as pd
import re

# Загрузите DataFrame из CSV файла

file_path3 = '/content/drive/MyDrive/Lab1/promejutok/train_sentences_processed.csv'
df3 = pd.read_csv(file_path3)

# Регулярное выражение для токенизации, учитывающее сокращения и адреса электронной почты
combined_pattern = r'\b(?:[A-Z][a-z]*\.)+[A-Z][a-z]*\b|\S+@\S+|\w+'

# Еще одно регулярное выражение, которое вы хотите добавить
another_pattern = r'\b(?:[A-Z][a-z]*\.)+[A-Z][a-z]*\b|\S+@\S+|\w+'

# Функция для применения регулярных выражений к каждой ячейке
def apply_regex(cell):
    combined_matches = re.findall(combined_pattern, cell)
    another_matches = re.findall(another_pattern, cell)

    combined_tokens = ' '.join(combined_matches)
    another_tokens = ' '.join(another_matches)

    return f"{combined_tokens} {another_tokens}"

# Применяем функцию apply_regex к столбцу с текстовыми данными и создаем новый столбец 'tokens'
df3['tokens'] = df3['sentences'].apply(apply_regex)

# Оставляем только столбец 'tokens' в DataFrame
df3 = df3[['tokens']]

# Сохраняем DataFrame в CSV файле с одним столбцом 'tokens'
df3.to_csv('proba.csv', index=False)

df3

import pandas as pd
import re
import os
from IPython.display import clear_output

# Загрузите DataFrame из CSV файла
file_path3 = '/content/drive/MyDrive/Lab1/promejutok/train_sentences_processed.csv'
df3 = pd.read_csv(file_path3)

# Регулярное выражение для токенизации, учитывающее сокращения и адреса электронной почты
combined_pattern = r'\b(?:[A-Z][a-z]*\.)+[A-Z][a-z]*\b|\S+@\S+|\w+'

# Функция для применения регулярного выражения к каждой ячейке
def apply_regex(cell):
    return ' '.join(re.findall(combined_pattern, cell))

# Применяем функцию apply_regex к столбцу с текстовыми данными и создаем новый столбец 'tokens'
df3['tokens'] = df3['sentences'].apply(apply_regex)

# Оставляем только столбец 'tokens' в DataFrame
df3 = df3[['tokens']]

# Сохраняем DataFrame в CSV файле с одним столбцом 'tokens'
df3.to_csv('proba.csv', index=False)

# Путь к папке в Google Drive, где будут храниться результаты
results_folder = '/content/drive/MyDrive/Lab1/result'

# Создаем папки для каждого класса, если их еще нет
for class_number in df3['class'].unique():
    folder_path = os.path.join(results_folder, f'result{class_number}')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Обработка каждой строки в датафрейме
for index, row in df3.iterrows():
    clear_output()
    print(f"index of row on process {index}/119999")
    text = row['title'] + '. ' + row['text']

    # Применяем combined_pattern для токенизации
    tokens = re.findall(combined_pattern, text)

    # Создаем путь для сохранения результата
    folder_path = os.path.join(results_folder, f'result{row["class"]}')
    file_name = f"{index}.tsv"

    # Записываем каждое предложение в TSV-файл
    with open(os.path.join(folder_path, file_name), 'w') as writefile:
        # Вычисляем леммы и стеммы и записываем их в файл
        for token in tokens:
            lemma = lemmatizer.lemmatize(token)
            stemma = snowball_stemmer_obj.stem(token)
            writefile.write(f"{token}\t{stemma}\t{lemma}\n")
        writefile.write('\n')

# 2) вычленение токенов
      tokens = re.findall(regex_to_take_tokens, sentence)