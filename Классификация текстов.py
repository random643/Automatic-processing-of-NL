# -*- coding: utf-8 -*-
"""lab4_trabl.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rsIfyZ5tPeHWEJd4x3r1LDunM1zquHNe
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.svm import SVC
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score, accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import random
!pip install scikit-learn==1.0.2
import warnings
warnings.filterwarnings("ignore")

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

# Указываем путь к файлу на Google Диске
file_path = '/content/drive/MyDrive/lab4/test_3.csv'

# Чтение файла в DataFrame
df = pd.read_csv(file_path, header=None)

# Установка имен столбцов
df.columns = ['class', 'text_1', 'text_2']

# Добавление столбца 'index' с индексами
df['index'] = df.index

from tqdm import tqdm
import pandas as pd

# Указываем полный путь к файлу на Google Диске
file_path = '/content/drive/MyDrive/lab3/test-vector/test-embeddings.tsv'

df_embedding = pd.DataFrame(columns=['index'] + [f'col_{i+1}' for i in range(100)])
data_list = []

with open(file_path, 'r') as file:
    data = file.readlines()

# Продолжите выполнение операций с данными, как в вашем предыдущем коде

for line in tqdm(data, total=len(data), desc='Обработка файла в DataFrame'):
    line = line.split('\t')
    if len(line) == 101:# есть срочка где 111 символов (возможно некорректно записалась)
        index = line[0]
        embedding = [float(i) for i in line[1:]]

        # из списка embedding с 100 элементами в векторе получить 100 отдельных столбцов
        data_embedding = pd.DataFrame(embedding).T
        data_embedding.columns = [f'col_{i+1}' for i in range(100)]
        data_embedding['index'] = index

        df_embedding = pd.concat([df_embedding, data_embedding], ignore_index=True)

df_embedding = pd.concat([df_embedding, pd.DataFrame(data_list)], ignore_index=True)
df_embedding['index'] = df_embedding['index'].astype(int)

df_embedding.head()

final_data = pd.merge(df_embedding, df, on='index')
final_data = final_data.drop(columns=['text_1', 'text_2'], axis=1)

final_data.sample(5)

class_counts = final_data['class'].value_counts()


plt.figure(figsize=(6, 6))
plt.pie(class_counts, labels=class_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
plt.title('Распределение классов')

plt.axis('equal')
plt.show()

def custom_precision(y_true, y_pred):
    return precision_score(y_true, y_pred, average='macro')

def custom_recall(y_true, y_pred):
    return recall_score(y_true, y_pred, average='macro')

def custom_f1_score(y_true, y_pred):
    return f1_score(y_true, y_pred, average='macro')

def custom_accuracy(y_true, y_pred):
    return accuracy_score(y_true, y_pred)

# Создаем scorer для каждой метрики
scoring = {
    'precision': make_scorer(custom_precision),
    'recall': make_scorer(custom_recall),
    'f1_score': make_scorer(custom_f1_score),
    'accuracy': make_scorer(custom_accuracy)
}

X = final_data.drop(columns=['class', 'index'])
y = final_data['class']

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y ,test_size=0.2, random_state=42)

"""Напишем функцию для обучения и сбора метрик"""

def train_model(kernel='rbf'):
    data_list = []
    for epochs_count in tqdm(range(100, 2001, 100), total=len(range(100, 2001, 100)), desc='Обучение модели'):
        model = Pipeline([('scaler', StandardScaler()),
                         ('svc', SVC(kernel=kernel, max_iter=epochs_count))])

        cv_results = cross_validate(model, X_train, y_train, cv=5, scoring=scoring)
        fit_time = cv_results['fit_time'].mean()
        score_time = cv_results['score_time'].mean()
        test_precision = cv_results['test_precision'].mean()
        test_recall = cv_results['test_recall'].mean()
        test_f1_score = cv_results['test_f1_score'].mean()
        test_accuracy = cv_results['test_accuracy'].mean()

        new_row = {'epoch': epochs_count, 'fit_time': fit_time, 'score_time': score_time, 'test_precision': test_precision, 'test_recall': test_recall, 'test_f1_score': test_f1_score, 'test_accuracy': test_accuracy}
        data_list.append(new_row)
    return pd.DataFrame(data_list)

"""#### Linear SVC"""

data_linear = train_model(kernel='linear')

data_linear.sample(5)

"""#### Linear rbf"""

data_rbf = train_model(kernel='rbf')

data_rbf.sample(5)

"""#### Linear sigmoid"""

data_sigmoid = train_model(kernel='sigmoid')

data_sigmoid.sample(5)

"""Построим график для визуализации обучения"""

plt.figure(figsize=(12, 8))

# График для Precision
plt.subplot(221)
plt.plot(data_linear['epoch'], data_linear['test_precision'], marker='o', linestyle='-', color='b', label='linear')
plt.plot(data_rbf['epoch'], data_rbf['test_precision'], marker='x', linestyle='--', color='g', label='rbf')
plt.plot(data_sigmoid['epoch'], data_sigmoid['test_precision'], marker='s', linestyle='-.', color='r', label='sigmoid')
plt.xlabel('Эпоха')
plt.ylabel('Precision')
plt.title('Precision по эпохам')
plt.legend()
plt.grid(True)

# График для Recall
plt.subplot(222)
plt.plot(data_linear['epoch'], data_linear['test_recall'], marker='o', linestyle='-', color='b', label='linear')
plt.plot(data_rbf['epoch'], data_rbf['test_recall'], marker='x', linestyle='--', color='g', label='rbf')
plt.plot(data_sigmoid['epoch'], data_sigmoid['test_recall'], marker='s', linestyle='-.', color='r', label='sigmoid')
plt.xlabel('Эпоха')
plt.ylabel('Recall')
plt.title('Recall по эпохам')
plt.legend()
plt.grid(True)

# График для F1-Score
plt.subplot(223)
plt.plot(data_linear['epoch'], data_linear['test_f1_score'], marker='o', linestyle='-', color='b', label='linear')
plt.plot(data_rbf['epoch'], data_rbf['test_f1_score'], marker='x', linestyle='--', color='g', label='rbf')
plt.plot(data_sigmoid['epoch'], data_sigmoid['test_f1_score'], marker='s', linestyle='-.', color='r', label='sigmoid')
plt.xlabel('Эпоха')
plt.ylabel('F1-Score')
plt.title('F1-Score по эпохам')
plt.legend()
plt.grid(True)

# График для Accuracy
plt.subplot(224)
plt.plot(data_linear['epoch'], data_linear['test_accuracy'], marker='o', linestyle='-', color='b', label='linear')
plt.plot(data_rbf['epoch'], data_rbf['test_accuracy'], marker='x', linestyle='--', color='g', label='rbf')
plt.plot(data_sigmoid['epoch'], data_sigmoid['test_accuracy'], marker='s', linestyle='-.', color='r', label='sigmoid')
plt.xlabel('Эпоха')
plt.ylabel('Accuracy')
plt.title('Accuracy по эпохам')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

"""Искать лучшую модель будем опираясь на `f1_score`, так как комбинирует точность и полноту"""

index = data_rbf['test_f1_score'].idxmax()
f1_max = data_rbf['test_f1_score'][index]
precision_max = data_rbf['test_precision'][index]
recall_max = data_rbf['test_recall'][index]
accuracy_max = data_rbf['test_accuracy'][index]

print(f"Лучшая эпоха получилась {data_rbf['epoch'][index]}: \n"
      f"Время обучения: {data_rbf['fit_time'][index]:.4f} \n"
      f"Время предсказания: {data_rbf['score_time'][index]:.4f} \n"
      f"Best f1 score: {f1_max:.4f} \n"
      f"Best precision score: {precision_max:.4f} \n"
      f"Best recall score: {recall_max:.4f} \n"
      f"Best accuracy score: {accuracy_max:.4f} ")

"""### Задание: Отбросить несколько случайно выбранных элементов векторных представлений, зафиксировать характер зависимости значений метрик от количества отброшенных размерностей;

"""

results = []
max_drop_dimensions = 100

for drop_dimensions in tqdm(range(max_drop_dimensions + 1), total=len(range(max_drop_dimensions + 1)), desc='Обучение модели'):
    # Клонируем данные, чтобы избежать изменений в исходных данных
    X_train_modified = X_train.copy()

    columns_to_drop = np.random.choice(X_train_modified.columns, drop_dimensions, replace=False)
    X_train_modified = X_train_modified.drop(columns=columns_to_drop)

    model = Pipeline([('scaler', StandardScaler()),
                 ('svc', SVC(kernel='rbf', max_iter=1100))])

    cv_results = cross_validate(model, X_train_modified, y_train, cv=5, scoring=scoring)

    fit_time = cv_results['fit_time'].mean()
    score_time = cv_results['score_time'].mean()
    test_precision = cv_results['test_precision'].mean()
    test_recall = cv_results['test_recall'].mean()
    test_f1_score = cv_results['test_f1_score'].mean()
    test_accuracy = cv_results['test_accuracy'].mean()

    new_row = dict(drop_dimensions=drop_dimensions, fit_time=fit_time, score_time=score_time,
               test_precision=test_precision, test_recall=test_recall, test_f1_score=test_f1_score,
               test_accuracy=test_accuracy)

    results.append(new_row)  # Добавляем результаты в список

# Преобразуем список результатов в DataFrame
results_df = pd.DataFrame(results)

results = pd.DataFrame(results)
results.sample(7)

plt.figure(figsize=(12, 8))

# График для Precision
plt.subplot(221)
plt.plot(results['drop_dimensions'], results['test_precision'], marker='o', linestyle='-', color='b')
plt.xlabel('Кол-во столбцов')
plt.ylabel('Precision')
plt.title('Precision по эпохам')
plt.grid(True)

# График для Recall
plt.subplot(222)
plt.plot(results['drop_dimensions'], results['test_recall'], marker='o', linestyle='-', color='b')
plt.xlabel('Кол-во столбцов')
plt.ylabel('Recall')
plt.title('Recall по эпохам')
plt.grid(True)

# График для F1-Score
plt.subplot(223)
plt.plot(results['drop_dimensions'], results['test_f1_score'], marker='o', linestyle='-', color='b')
plt.xlabel('Кол-во столбцов')
plt.ylabel('F1-Score')
plt.title('F1-Score по эпохам')
plt.grid(True)

# График для Accuracy
plt.subplot(224)
plt.plot(results['drop_dimensions'], results['test_accuracy'], marker='o', linestyle='-', color='b')
plt.xlabel('Кол-во столбцов')
plt.ylabel('Accuracy')
plt.title('Accuracy по эпохам')
plt.grid(True)

plt.tight_layout()
plt.show()

index = results['test_f1_score'].idxmax()
f1_max = results['test_f1_score'][index]
precision_max = results['test_precision'][index]
recall_max = results['test_recall'][index]
accuracy_max = results['test_accuracy'][index]

print(f"Кол-во столбцов, которое сократили {results['drop_dimensions'][index]}: \n"
      f"Время обучения: {results['fit_time'][index]:.4f} \n"
      f"Время предсказания: {results['score_time'][index]:.4f} \n"
      f"Best f1 score: {f1_max:.4f} \n"
      f"Best precision score: {precision_max:.4f} \n"
      f"Best recall score: {recall_max:.4f} \n"
      f"Best accuracy score: {accuracy_max:.4f} ")

"""Видим, что при удалении 66 столбцов совсем немного выросла метрика f1

### Сократить размерность векторных представлений до некоторого значения, зафиксировать характер зависимости значений метрик от новой размерности;

Для сокращения размерности возьмем метод `PCA`
"""

results_pca = []

for drop_dimensions in tqdm(range(max_drop_dimensions + 1), total=len(range(max_drop_dimensions + 1)), desc='Обучение модели'):

    model = Pipeline([('scaler', StandardScaler()),
                      ('pca', PCA(n_components=drop_dimensions)),
                      ('svc', SVC(kernel='rbf', max_iter=1100))])

    cv_results = cross_validate(model, X_train, y_train, cv=5, scoring=scoring)

    fit_time = cv_results['fit_time'].mean()
    score_time = cv_results['score_time'].mean()
    test_precision = cv_results['test_precision'].mean()
    test_recall = cv_results['test_recall'].mean()
    test_f1_score = cv_results['test_f1_score'].mean()
    test_accuracy = cv_results['test_accuracy'].mean()

    new_row = dict(drop_dimensions=drop_dimensions, fit_time=fit_time, score_time=score_time,
                   test_precision=test_precision, test_recall=test_recall, test_f1_score=test_f1_score,
                   test_accuracy=test_accuracy)
    results_pca.append(new_row)

results_pca = pd.DataFrame(results_pca)
results_pca.sample(7)

plt.figure(figsize=(12, 8))

# График для Precision
plt.subplot(221)
plt.plot(results_pca['drop_dimensions'], results_pca['test_precision'], marker='o', linestyle='-', color='b')
plt.xlabel('Кол-во components')
plt.ylabel('Precision')
plt.title('Precision по эпохам')
plt.grid(True)

# График для Recall
plt.subplot(222)
plt.plot(results_pca['drop_dimensions'], results_pca['test_recall'], marker='o', linestyle='-', color='b')
plt.xlabel('Кол-во components')
plt.ylabel('Recall')
plt.title('Recall по эпохам')
plt.grid(True)

# График для F1-Score
plt.subplot(223)
plt.plot(results_pca['drop_dimensions'], results_pca['test_f1_score'], marker='o', linestyle='-', color='b')
plt.xlabel('Кол-во components')
plt.ylabel('F1-Score')
plt.title('F1-Score по эпохам')
plt.grid(True)

# График для Accuracy
plt.subplot(224)
plt.plot(results_pca['drop_dimensions'], results_pca['test_accuracy'], marker='o', linestyle='-', color='b')
plt.xlabel('Кол-во components')
plt.ylabel('Accuracy')
plt.title('Accuracy по эпохам')
plt.grid(True)

plt.tight_layout()
plt.show()

index = results_pca['test_f1_score'].idxmax()
f1_max = results_pca['test_f1_score'][index]
precision_max = results_pca['test_precision'][index]
recall_max = results_pca['test_recall'][index]
accuracy_max = results_pca['test_accuracy'][index]

print(f"Кол-во компонент в PCA {results_pca['drop_dimensions'][index]}: \n"
      f"Время обучения: {results_pca['fit_time'][index]:.4f} \n"
      f"Время предсказания: {results_pca['score_time'][index]:.4f} \n"
      f"Best f1 score: {f1_max:.4f} \n"
      f"Best precision score: {precision_max:.4f} \n"
      f"Best recall score: {recall_max:.4f} \n"
      f"Best accuracy score: {accuracy_max:.4f} ")

"""Лучший f1 score получился при размерности 53, метрика получилась такой же, что и при 100. Удалось успешно сократить размерность не потеряв в качестве

### Задание: Добавить дополнительные размерности векторных представлений с использованием стандартных математических функций (log, cos, sin и т.д.), зафиксировать характер влияния нескольких модификаций на значения метрик;

##### numpy.log1p

Воспользуемся numpy.log1p -  вычисления натурального логарифма (логарифма по основанию e) для каждого элемента массива, увеличенного на 1. Формально, она вычисляет `log(1 + x)` для каждого элемента x массива. Это необходимо так как, если применять np.log можем получить nan из за того, что значения близки к нулю
"""

model = Pipeline([('scaler', StandardScaler()),
                  ('svc', SVC(kernel='rbf', max_iter=1100))])

X_train_log = pd.concat([X_train, np.log1p(X_train)], axis=1)

def plus_new_feature(X_train, text):
    cv_results = cross_validate(model, X_train, y_train, cv=5, scoring=scoring)

    fit_time = cv_results['fit_time'].mean()
    score_time = cv_results['score_time'].mean()
    test_precision = cv_results['test_precision'].mean()
    test_recall = cv_results['test_recall'].mean()
    test_f1_score = cv_results['test_f1_score'].mean()
    test_accuracy = cv_results['test_accuracy'].mean()

    print(f"{text} :\n"
          f"Время обучения: {fit_time:.4f} \n"
          f"Время предсказания: {score_time:.4f} \n"
          f"f1 score: {test_f1_score:.4f} \n"
          f"precision score: {test_precision:.4f} \n"
          f"recall score: {test_recall:.4f} \n"
          f"accuracy score: {test_accuracy:.4f} ")

plus_new_feature(X_train=X_train_log,
                text='Original feature + log')

"""##### cos"""

X_train_cos = pd.concat([X_train, np.cos(X_train)], axis=1)

plus_new_feature(X_train=X_train_cos,
                text='Original feature + cos')

"""#### sin"""

X_train_sin = pd.concat([X_train, np.sin(X_train)], axis=1)

plus_new_feature(X_train=X_train_sin,
                text='Original feature + sin')

"""метрика немного ухудшилась

Теперь протестируем модель и посмотрим, что покажет она на тесте
"""

final_model = Pipeline([('scaler', StandardScaler()),
                 ('svc', SVC(kernel='linear', max_iter=1100))])

final_model.fit(X_train, y_train)

prediction = final_model.predict(X_test)

print(f"f1 score: {custom_f1_score(y_test, prediction):.4f} \n"
      f"precision score: {custom_precision(y_test, prediction):.4f} \n"
      f"recall score: {custom_recall(y_test, prediction):.4f} \n"
      f"accuracy score: {custom_accuracy(y_test, prediction):.4f} ")