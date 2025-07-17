import numpy as np
from DL.learner import Learner
import DL.mapping as mapping

# Train a model using the given update, displacement, and inverse displacement maps
def train(learner: Learner, train_x, train_y, num_epochs=1, shuffle_data=True):
    n = np.shape(train_x)[0]
    m = np.shape(train_y)[0]
    if n != m:
        err = "Mismatch in dimension 0: {} training examples but {} labels".format(n, m)
        raise ValueError(err)

    # get initial value of S(P) × P
    p0 = learner.model.param()
    param = learner.update.initialize(p0), p0

    step  = learner.to_lens()
    xs    = train_x
    ys    = train_y
    permutation = np.array(range(0, n))
    for epoch in range(0, num_epochs):
        if shuffle_data:
            np.random.shuffle(permutation)

        # A single loop of "generalised SGD" over each training example
        for j in range(0, n):
            i = permutation[j] # for shuffling
            x, y = xs[i], ys[i]
            param, _ = step.rev(((param, x), y))
            yield (epoch, j, i, param)

# Measure the accuracy of a function (f : A → B) on a dataset of pairs [(A, B)]
def accuracy(f, xs, ys):
    n = len(xs)
    s = 0
    for i in range(0, n):
        yhat = f(xs[i])
        ytrue = ys[i]
        if np.all(yhat == ytrue):
            s += 1
    return s / n
