from sklearn.base import BaseEstimator, TransformerMixin, ClusterMixin


class DistilledCluster(
    ClusterMixin,
    BaseEstimator
):
    """
    A meta-transformer that can use any clustering algorithms.
    """

    def __init__(self, cluster, distiller):
        """
        Parameters
        ----------
        cluster : sklearn.base.ClusterMixin
            A clustering algorithm.
        distiller : sklearn.base.ClassifierMixin
            A classifier that can predict cluster labels.
        """
        self.cluster = cluster
        self.distiller = distiller

    def fit(self, X, y=None):
        """
        Fit the model using X as training data and y as target values.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training instances to cluster.
        y : Ignored
            Not used, present here for API consistency by convention.
        """

        self.cluster.fit(X)
        self.distiller.fit(X, self.cluster.labels_)
        return self

    def fit_predict(self, X, y=None):
        """
        Fit the model using X as training data and y as target values.
        Then predict the closest cluster each sample in X belongs to.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            New data to predict.
        y : Ignored
            Not used, present here for API consistency by convention.
        """
        self.fit(X)
        return self.predict(X)

    def fit_transform(self, X, y=None):
        """
        Fit the model using X as training data and y as target values.
        Then predict the closest cluster each sample in X belongs to.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            New data to predict.
        y : Ignored
            Not used, present here for API consistency by convention.
        """
        return self.fit_predict(X)

    def predict(self, X):
        """
        Predict the closest cluster each sample in X belongs to.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            New data to predict.
        """

        return self.distiller.predict(X)

    def transform(self, X):
        """
        Predict the closest cluster each sample in X belongs to.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            New data to predict.
        """
        return self.distiller.predict(X)


class DistilledTransformer(
    TransformerMixin,
    BaseEstimator
):
    """
    A meta-transformer that can use any dimensionality reduction algorithms.
    """
    def __init__(self, dimensionality_reducer, distiller):
        """
        Parameters
        ----------
        dimensionality_reducer : sklearn.base.TransformerMixin
            A dimensionality reduction algorithm.
        distiller : sklearn.base.RegressorMixin
            A regressor that can predict feature values.
        """
        self.dimensionality_reducer = dimensionality_reducer
        self.distiller = distiller

    def fit(self, X, y=None):
        """
        Fit the model using X as training data and y as target values.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training instances to cluster.  
        y : Ignored
            Not used, present here for API consistency by convention.
        """
        # TransformerMixin
        if hasattr(self.dimensionality_reducer, 'fit_transform'):
            feature = self.dimensionality_reducer.fit_transform(X)
        elif hasattr(self.dimensionality_reducer, 'fit_predict'):
            feature = self.dimensionality_reducer.fit_predict(X)
        else:
            raise ValueError(
                'dimensionality_reducer must have either fit_transform or fit_predict method')
        self.distiller.fit(X, feature)

    def fit_transform(self, X, y=None, **fit_params):
        """
        Fit the model using X as training data and y as target values.
        Then predict the target values.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training instances to cluster.
        y : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        X_new : array-like, shape (n_samples, n_features_new)
            Transformed array.
        """
        self.fit(X, y)
        return self.transform(X)

    def transform(self, X, y=None):
        """
        Predict the target values.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training instances to cluster.
        """
        return self.distiller.predict(X)
