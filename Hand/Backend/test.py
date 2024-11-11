import numpy as np
import feature_extractor as fe

open = np.array([1,1,1,1,1,1,1,1])
fist = np.array([1,2000,1,1,1,1,1,1])
peace = np.array([1,1,2000,1,1,1,1,1])
point = np.array([1,1,1,2000,1,1,1,1])
thumb = np.array([1,1,1,1,2000,1,1,1])

signals = np.tile(thumb, (10, 1))

featureExtractor = fe.FeatureExtractor()

features = featureExtractor.extract_features(signals)
print(features)