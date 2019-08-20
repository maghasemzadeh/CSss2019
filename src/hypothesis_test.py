import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random


def random_grouping(df, group, info):
    data = pd.DataFrame({"info":df[info],"groups":df[group]})
    numbers = random.sample(range(0, data["groups"].size), sum(data["groups"]))
    others= [i for i in range(0, data["groups"].size) if i not in numbers]
    first = data["info"][numbers]
    second = data["info"][others]
    plt.boxplot([first, second], labels=["sick","not sick"])
    plt.show()


def box_diagram(df, group, info):
    first_group = df[df[group] == 1][info]
    second_group = df[df[group] == 0][info]
    plt.boxplot([first_group, second_group], labels=["sick", "not sick"])
    plt.show()


def mean(datas):
    return sum(datas) / len(datas)


def mean_difference(first_group, second_group):
    return mean(first_group) - mean(second_group)


def permutation_test(df, group, info):
    data = df[info]
    size_first_group = len(data) // 2
    n = 1000
    zero_target = df[df[group] == 0][info]
    one_target = df[df[group] == 1][info]
    main_difference = mean_difference(one_target, zero_target)
    res = list()
    counter = 0
    for i in range(n):
        random.shuffle(data)
        group_b = data[size_first_group:]
        group_a = data[:size_first_group]
        differ = mean_difference(group_a, group_b)
        if differ > main_difference:
            counter += 1
        res.append(differ)
    print("There are "+str(counter)+" times in 1000 times that we have mean difference greater or equal to our data's mean difference")
    plt.hist(res)
    plt.show()



