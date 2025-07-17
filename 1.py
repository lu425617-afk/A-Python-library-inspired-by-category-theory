#!/usr/bin/env python3

import numpy as np
import tensorflow as tf
import DL.mapping as Mapping
from DL.parameteriedmapping import Para, ParaInit, dense, relu, sigmoid, to_para
from DL.statistics import accuracy
from DL.update import rda_momentum
from DL.supervised import supervised_step, train_supervised, mse_loss, learning_rate

# 使用 TensorFlow 加载 MNIST 数据集
def load_mnist():
    # 使用 tensorflow 加载 MNIST 数据集
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    # 归一化到 [0, 1] 范围
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0

    # 将数据从 (28, 28) 扩展到 (28, 28, 1)
    x_train = x_train.reshape(x_train.shape[0], 28 * 28)  # 展平图像
    x_test = x_test.reshape(x_test.shape[0], 28 * 28)  # 展平图像

    # one-hot 编码标签
    _MNIST_CLASSES = 10
    y_train = np.identity(_MNIST_CLASSES)[y_train]
    y_test = np.identity(_MNIST_CLASSES)[y_test]

    return (x_train, y_train), (x_test, y_test)

# 定义三层神经网络（激活函数使用 ReLU 或 Sigmoid）
model = (dense((28 * 28, 512), activation=Mapping.relu)  # 输入层到隐藏层1
         >> dense((512, 256), activation=Mapping.relu)  # 隐藏层1到隐藏层2
         >> dense((256, 10), activation=Mapping.sigmoid))  # 隐藏层2到输出层

if __name__ == "__main__":
    print("NOTE: TensorFlow will load the MNIST dataset.")

    # 加载 MNIST 数据集
    try:
        (x_train, y_train), (x_test, y_test) = load_mnist()
        print("MNIST load successfully！")
    except Exception as e:
        print("MNIST fail to load:", e)
        exit(1)

    # 定义训练步骤和参数
    step, param = supervised_step(model, rda_momentum(γ=-0.1), Para(mse_loss), to_para(learning_rate(η=-0.01)))

    # 打印训练过程中的诊断信息
    e_prev = None
    fwd = model.arrow.arrow.fwd
    for e, j, i, param in train_supervised(step, param, x_train, y_train, num_epochs=4, shuffle_data=True):
        # 仅每隔 10000 个样本打印一次诊断信息
        if j % 10000:
            continue

        e_prev = e
        predict = lambda x: fwd((param[1], x)).argmax()
        # 打印测试集上的准确率
        acc = accuracy(predict, x_test, y_test.argmax(axis=1))
        print('epoch', e, 'sample', j, '\taccuracy {0:.4f}'.format(acc), sep='\t')

    # 打印最终的测试集准确率
    acc = accuracy(predict, x_test, y_test.argmax(axis=1))
    print('final accuracy: {0:.4f}'.format(acc))
