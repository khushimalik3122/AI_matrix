# -*- coding: utf-8 -*-
"""data cleaning ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iYRTFTg7fEaCY0AOtdm379vrEQ0RCuBS
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
train_df= pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Sentinel2_CropSamples_Reorganized.csv')
test_df= pd.read_csv('/content/drive/MyDrive/test (6).csv')

train_df.head()

train_df.info()

test_df.head()

test_df.info()

import numpy as np
train_df['time'] = pd.to_datetime(train_df['time'], errors='coerce')
test_df['time'] = pd.to_datetime(test_df['time'], errors='coerce')

train_df.dropna(subset=['time'], inplace=True)
test_df.dropna(subset=['time'], inplace=True)

train_df['red'] = pd.to_numeric(train_df['red'], errors='coerce')
test_df['red'] = pd.to_numeric(test_df['red'], errors='coerce')
train_df.dropna(subset=['red'], inplace=True)
test_df.dropna(subset=['red'], inplace=True)

x_mean, x_std = train_df['x'].mean(), train_df['x'].std()
y_mean, y_std = train_df['y'].mean(), train_df['y'].std()
train_df['x_norm'] = (train_df['x'] - x_mean) / x_std
train_df['y_norm'] = (train_df['y'] - y_mean) / y_std
test_df['x_norm'] = (test_df['x'] - x_mean) / x_std
test_df['y_norm'] = (test_df['y'] - y_mean) / y_std

plt.figure(figsize=(8, 5))
sns.countplot(data=train_df, x='crop_type', order=train_df['crop_type'].value_counts().index)
plt.title("Crop Type Distribution")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

bands = ['blue', 'green', 'red', 'nir', 'nir08', 'rededge1', 'rededge2', 'rededge3', 'swir16', 'swir22']
fig, axes = plt.subplots(2, 5, figsize=(20, 8))
for i, band in enumerate(bands):
    sns.boxplot(data=train_df, x='crop_type', y=band, ax=axes[i // 5, i % 5])
    axes[i // 5, i % 5].set_title(f"{band} by Crop")
    axes[i // 5, i % 5].tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
for uid in train_df['unique_id'].unique()[:3]:
    group = train_df[train_df['unique_id'] == uid].sort_values("time")
    plt.plot(group['time'], group['nir'] - group['red'], label=uid)
plt.title("NIR - RED (NDVI-like) Over Time")
plt.ylabel("NIR - RED")
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.kdeplot(x=train_df['red'], label='Train - Red', fill=True)
sns.kdeplot(x=test_df['red'], label='Test - Red', fill=True)
plt.title("Red Band Distribution: Train vs Test")
plt.xlabel("Red Reflectance")
plt.legend()
plt.tight_layout()
plt.show()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Compute NDVI and NDRE safely
train_df['ndvi'] = (train_df['nir'] - train_df['red']) / (train_df['nir'] + train_df['red'] + 1e-6)
train_df['ndre'] = (train_df['rededge3'] - train_df['red']) / (train_df['rededge3'] + train_df['red'] + 1e-6)

test_df['ndvi'] = (test_df['nir'] - test_df['red']) / (test_df['nir'] + test_df['red'] + 1e-6)
test_df['ndre'] = (test_df['rededge3'] - test_df['red']) / (test_df['rededge3'] + test_df['red'] + 1e-6)

# Plot NDVI and NDRE distributions per crop type
plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
sns.boxplot(data=train_df, x='crop_type', y='ndvi')
plt.title("NDVI by Crop Type")
plt.xticks(rotation=45)

plt.subplot(1, 2, 2)
sns.boxplot(data=train_df, x='crop_type', y='ndre')
plt.title("NDRE by Crop Type")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

import pandas as pd


# Convert key bands to numeric
bands = ['red', 'nir', 'rededge3', 'blue', 'swir16']
for band in bands:
    train_df[band] = pd.to_numeric(train_df[band], errors='coerce')
    test_df[band] = pd.to_numeric(test_df[band], errors='coerce')

# Drop rows with missing key bands
train_df.dropna(subset=bands, inplace=True)
test_df.dropna(subset=bands, inplace=True)

# Define constants
epsilon = 1e-6
L = 0.5

# --- Compute Indices ---

# NDVI = (NIR - Red) / (NIR + Red)
train_df['ndvi'] = (train_df['nir'] - train_df['red']) / (train_df['nir'] + train_df['red'] + epsilon)
test_df['ndvi'] = (test_df['nir'] - test_df['red']) / (test_df['nir'] + test_df['red'] + epsilon)

# NDRE = (RedEdge3 - Red) / (RedEdge3 + Red)
train_df['ndre'] = (train_df['rededge3'] - train_df['red']) / (train_df['rededge3'] + train_df['red'] + epsilon)
test_df['ndre'] = (test_df['rededge3'] - test_df['red']) / (test_df['rededge3'] + test_df['red'] + epsilon)

# EVI = 2.5 * (NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1)
train_df['evi'] = 2.5 * (train_df['nir'] - train_df['red']) / (
    train_df['nir'] + 6 * train_df['red'] - 7.5 * train_df['blue'] + 1 + epsilon)
test_df['evi'] = 2.5 * (test_df['nir'] - test_df['red']) / (
    test_df['nir'] + 6 * test_df['red'] - 7.5 * test_df['blue'] + 1 + epsilon)

# NDWI = (NIR - SWIR16) / (NIR + SWIR16)
train_df['ndwi'] = (train_df['nir'] - train_df['swir16']) / (train_df['nir'] + train_df['swir16'] + epsilon)
test_df['ndwi'] = (test_df['nir'] - test_df['swir16']) / (test_df['nir'] + test_df['swir16'] + epsilon)

# SAVI = (1 + L) * (NIR - Red) / (NIR + Red + L)
train_df['savi'] = (1 + L) * (train_df['nir'] - train_df['red']) / (train_df['nir'] + train_df['red'] + L + epsilon)
test_df['savi'] = (1 + L) * (test_df['nir'] - test_df['red']) / (test_df['nir'] + test_df['red'] + L + epsilon)

# Preview
print(train_df.head())

train_df

from sklearn.preprocessing import StandardScaler
train_df=train_df
# List of raw bands and indices
features_to_scale = ['blue', 'green', 'red', 'nir', 'nir08',
                     'rededge1', 'rededge2', 'rededge3',
                     'swir16', 'swir22',
                     'ndvi', 'ndre', 'evi', 'ndwi', 'savi']

scaler = StandardScaler()
train_scaled = scaler.fit_transform(train_df[features_to_scale])
test_scaled = scaler.transform(test_df[features_to_scale])

train_scaled_df = pd.DataFrame(train_scaled, columns=features_to_scale)
test_scaled_df = pd.DataFrame(test_scaled, columns=features_to_scale)
# 🧠 Re-attach these columns from the original train/test
train_scaled_df['unique_id'] = train_df['unique_id'].values
train_scaled_df['time'] = train_df['time'].values
train_scaled_df['crop_type'] = train_df['crop_type'].values

test_scaled_df['unique_id'] = test_df['unique_id'].values
test_scaled_df['time'] = test_df['time'].values

test_scaled_df.info()
train_scaled_df.info()

train_scaled_df.to_csv("train_scaled_clean.csv", index=False)
test_scaled_df.to_csv("/content/drive/MyDrive/test_scaled_clean.csv", index=False)



from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import log_loss
from sklearn.preprocessing import StandardScaler
import numpy as np

# Define features and label
features = ['blue', 'green', 'red', 'nir', 'nir08', 'rededge1', 'rededge2',
            'rededge3', 'swir16', 'swir22', 'ndvi', 'ndre', 'evi', 'ndwi', 'savi']

X = train_df[features]
y = train_df['crop_type']

# ---------------------------
# 1. Model on raw features
# ---------------------------
clf_raw = LogisticRegression(max_iter=1000, multi_class='multinomial')
scores_raw = cross_val_score(clf_raw, X, y, cv=5, scoring='neg_log_loss')
print("Log Loss (Raw):", -np.mean(scores_raw))

# ---------------------------
# 2. Model on normalized features
# ---------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

clf_scaled = LogisticRegression(max_iter=1000, multi_class='multinomial')
scores_scaled = cross_val_score(clf_scaled, X_scaled, y, cv=5, scoring='neg_log_loss')
print("Log Loss (Scaled):", -np.mean(scores_scaled))











