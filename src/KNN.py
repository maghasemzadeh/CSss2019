from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd


def KNN_classifier(df, k, target, train_attr):
    y_train, y_test, x_train, x_test = train_test_split(df[train_attr],
                                                        df[target], random_state=0, test_size=0.05)
    print("X_train shape: {}\ny_train shape: {}".format(x_train.shape, y_train.shape))
    print("X_test shape: {}\ny_test shape: {}".format(x_test.shape, y_test.shape))
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(x_train, y_train)
    y_pred = knn.predict(x_test)
    res = pd.concat([x_test, y_test, pd.Series(y_pred, name='Predicted', index=x_test.index)],ignore_index=False, axis=1)
    print(res)
    print("Test set score: {:.2f}".format(knn.score(x_test, y_test)))
    return res
