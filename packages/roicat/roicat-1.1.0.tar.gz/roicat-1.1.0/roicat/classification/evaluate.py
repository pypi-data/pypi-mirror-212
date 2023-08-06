import numpy as np
from .. import helpers
    
class Evaluation():
    def __init__(self, classifier):
        self.classifier = classifier
        return
    
    def confusion_matrix(self, x, y, counts=False):
        """
        Generate a confusion matrix for the dataset based on the classifier

        JZ 2022

        logreg: sklearn model with score method
        X_eval: Head from which to classify examples
        y_eval: True labels for examples for evaluation
        counts: Whether to return confusion matrix as counts (False) or percentages (True)
        """
        try:
            preds = self.classifier.predict(x).astype(np.int32)
        except:
            preds = self.classifier.run(x)[:,0].astype(np.int32)
        cm = helpers.confusion_matrix(preds, y.astype(np.int32), counts=counts)
        return cm
        
    def score_classifier_logreg(self, x, y, class_weights=None):
        """
        Generate a classification score for dataset based on the classifier
        
        JZ 2022
        
        logreg: sklearn model with score method
        X_eval: Head from which to classify examples
        y_eval: True labels for examples for evaluation
        """
        acc = self.classifier.score(x, y.astype(np.int32), sample_weight=helpers.get_balanced_sample_weights(y.astype(np.int32), class_weights=class_weights))
        return acc
    
    # =========================
