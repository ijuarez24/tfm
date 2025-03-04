# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 16:07:43 2025

@author: HP
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_curve, auc
)

# -------------------------------
# 1. Generar datos sintéticos
# -------------------------------
np.random.seed(42)
n_samples = 1000

# Características
edad = np.random.normal(60, 10, n_samples)  # Edad promedio: 60 años
cea = np.random.normal(5, 2, n_samples)       # Nivel de CEA promedio: 5 ng/mL
mutacion_kras = np.random.choice([0, 1], size=n_samples, p=[0.7, 0.3])
mutacion_braf = np.random.choice([0, 1], size=n_samples, p=[0.9, 0.1])

# Etiqueta objetivo (pronóstico)
prognosis = (0.2 * edad - 0.3 * cea + 0.4 * mutacion_kras + 0.6 * mutacion_braf +
             np.random.normal(0, 1, n_samples)) > 10
prognosis = prognosis.astype(int)

# Crear DataFrame
data = pd.DataFrame({
    'edad': edad,
    'cea': cea,
    'mutacion_kras': mutacion_kras,
    'mutacion_braf': mutacion_braf,
    'prognosis': prognosis
})

# -------------------------------
# 2. Dividir el conjunto de datos
# -------------------------------
X = data[['edad', 'cea', 'mutacion_kras', 'mutacion_braf']]
y = data['prognosis']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------------
# 3. MODELOS ML
# -------------------------------

# Regresión Logística
lr_model = LogisticRegression(random_state=42, max_iter=1000)
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)
accuracy_lr = accuracy_score(y_test, y_pred_lr)
precision_lr = precision_score(y_test, y_pred_lr)
recall_lr = recall_score(y_test, y_pred_lr)
f1_lr = f1_score(y_test, y_pred_lr)

print("Métricas modelo Regresión Logística:")
print(f"Accuracy: {accuracy_lr:.2f}")
print(f"Precision: {precision_lr:.2f}")
print(f"Recall: {recall_lr:.2f}")
print(f"F1 Score: {f1_lr:.2f}\n")

# SVM
svm_model = SVC(probability=True, random_state=42)
svm_model.fit(X_train, y_train)
y_pred_svm = svm_model.predict(X_test)
accuracy_svm = accuracy_score(y_test, y_pred_svm)
precision_svm = precision_score(y_test, y_pred_svm)
recall_svm = recall_score(y_test, y_pred_svm)
f1_svm = f1_score(y_test, y_pred_svm)

print("Métricas modelo SVM:")
print(f"Accuracy: {accuracy_svm:.2f}")
print(f"Precision: {precision_svm:.2f}")
print(f"Recall: {recall_svm:.2f}")
print(f"F1 Score: {f1_svm:.2f}\n")

# Random Forest
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
precision_rf = precision_score(y_test, y_pred_rf)
recall_rf = recall_score(y_test, y_pred_rf)
f1_rf = f1_score(y_test, y_pred_rf)

print("Métricas modelo Random Forest:")
print(f"Accuracy: {accuracy_rf:.2f}")
print(f"Precision: {precision_rf:.2f}")
print(f"Recall: {recall_rf:.2f}")
print(f"F1 Score: {f1_rf:.2f}\n")

# -------------------------------
# 4. Calcular y Graficar Curvas ROC
# -------------------------------

# Obtener probabilidades para la clase positiva (1)
y_proba_lr = lr_model.predict_proba(X_test)[:, 1]
y_proba_svm = svm_model.predict_proba(X_test)[:, 1]
y_proba_rf = rf_model.predict_proba(X_test)[:, 1]

# Calcular la curva ROC y el AUC para cada modelo
fpr_lr, tpr_lr, _ = roc_curve(y_test, y_proba_lr)
roc_auc_lr = auc(fpr_lr, tpr_lr)

fpr_svm, tpr_svm, _ = roc_curve(y_test, y_proba_svm)
roc_auc_svm = auc(fpr_svm, tpr_svm)

fpr_rf, tpr_rf, _ = roc_curve(y_test, y_proba_rf)
roc_auc_rf = auc(fpr_rf, tpr_rf)

# Graficar las curvas ROC
plt.figure(figsize=(8, 6))
plt.plot(fpr_lr, tpr_lr, label=f'Regresión logística (AUC = {roc_auc_lr:.2f})', color='blue')
plt.plot(fpr_svm, tpr_svm, label=f'SVM (AUC = {roc_auc_svm:.2f})', color='red')
plt.plot(fpr_rf, tpr_rf, label=f'Random Forest (AUC = {roc_auc_rf:.2f})', color='green')
plt.plot([0, 1], [0, 1], 'k--', label='Random Guess')
plt.xlabel('Tasa Falso Positivo Rate')
plt.ylabel('Tasa Verdadero Positivo')
plt.title('Curvas ROC de los Modelos')
plt.legend(loc='lower right')
plt.savefig(f'CurvasRoc.png', dpi=300, bbox_inches='tight')   
plt.show()
