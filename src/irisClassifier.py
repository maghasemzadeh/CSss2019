import math
import operator
from sklearn.model_selection import train_test_split


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet.iloc[x], length)
        distances.append((trainingSet.iloc[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet.iloc[x][-1] == predictions[x]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0


def iris_knn(df, k, target, train_attr):
    y_train, y_test, x_train, x_test = train_test_split(df[train_attr],
                                                        df[target], random_state=0, test_size=0.05)
    print("X_train shape: {}\ny_train shape: {}".format(x_train.shape, y_train.shape))
    print("X_test shape: {}\ny_test shape: {}".format(x_test.shape, y_test.shape))

    train_set = x_train
    test_set = x_test
    train_set['out'] = y_train
    test_set['out'] = y_test
    output = {}
    predictions = []
    for ind in range(len(test_set)):
        item = test_set.iloc[ind]
        neighbors = getNeighbors(train_set, item, k)
        result = getResponse(neighbors)
        predictions.append(result)
        output[ind] = {
            'neighbors': neighbors,
            'test': item,
            'predicted': result,
            'actual': test_set.iloc[ind][-1]
        }
        print('> predicted=' + repr(result) + ', actual=' + repr(test_set.iloc[ind][-1]))
    accuracy = getAccuracy(test_set, predictions)
    print('Accuracy: ' + repr(accuracy) + '%')
    # print(output)
    return output




