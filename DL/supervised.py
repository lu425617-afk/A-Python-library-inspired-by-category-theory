import numpy as np
from dataclasses import dataclass
from typing import Any

import DL.mapping as mapping
from DL.mapping import Mapping, identity
from DL.parameteriedmapping import Para, ParaInit
from DL.update import Update, apply_update

# Loss : (B × B → L, B × B × L' → B' × B')
# LR : (L → I, L × I' → L')
# LR = (lambda loss: None, lambda loss, _: η)
def learning_rate(η: float):
    # note: rev creates constant array of η based on dimensions of loss
    def learning_rate_fwd(loss):
        return None

    def learning_rate_rev(args):
        loss, unit = args
        assert unit is None
        return np.array([η])

    return Mapping(learning_rate_fwd, learning_rate_rev)

def rda_learning_rate(η: float):
    # note: rev creates constant array of η based on dimensions of loss
    def learning_rate_fwd(loss):
        return None

    def learning_rate_rev(args):
        loss, unit = args
        assert unit is None
        # NOTE: Here, learning rate η is not constant:
        # instead, we *scale* it by the (forward) loss
        return loss * np.array([η])

    return mapping(learning_rate_fwd, learning_rate_rev)

def mse_fwd(args):
    y, yhat = args
    loss = np.sum(0.5 * (y - yhat)**2)
    return np.array([loss])

def mse_rev(args):
    # note: 'loss' represents a *change* in loss, and is normally a constant-
    # the learning rate η
    (y, yhat), loss = args
    assert type(loss) is np.ndarray
    return loss * (y - yhat), loss * (yhat - y)

mse_loss = Mapping(mse_fwd, mse_rev)

# Returns a function of type P × A × B → P
def supervised_step(model: ParaInit, update: Update, loss: Para, cap: Para):
    assert type(model) is ParaInit
    model_with_update = apply_update(model, update)
    learner = model_with_update.arrow >> (loss >> cap)

    def step(b, p, a):
        # rev : (((I × B) × P) × A) × I' → (((I' × B') × P') × A')
        (((_, _), p_new), _) = learner.arrow.rev( ((((None, b), p), a), None) )
        return p_new

    return step, model_with_update.param()

# step : (S(P) × P) × A × B → (S(P) × P)
# initial_parameters : S(P) × P
def train_supervised(step, initial_parameters, train_x, train_y, num_epochs=1, shuffle_data=True):
    # Check we have the same number of features and labels
    n = np.shape(train_x)[0]
    m = np.shape(train_y)[0]
    if n != m:
        err = "Mismatch in dimension 0: {} training examples but {} labels".format(n, m)
        raise ValueError(err)

    xs    = train_x
    ys    = train_y
    permutation = np.array(range(0, n))
    param = initial_parameters
    for epoch in range(0, num_epochs):
        if shuffle_data:
            np.random.shuffle(permutation)

        # A single loop of "generalised SGD" over each training example
        for j in range(0, n):
            i = permutation[j] # for shuffling
            x, y = xs[i], ys[i]
            param = step(y, param, x)
            yield (epoch, j, i, param)

