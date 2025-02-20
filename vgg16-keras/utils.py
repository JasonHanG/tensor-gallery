from __future__ import division, print_function
import math

from matplotlib import pyplot as plt

import itertools

import bcolz

from keras.utils.np_utils import to_categorical

from vgg16 import *

np.set_printoptions(precision=4, linewidth=100)

to_bw = np.array([0.299, 0.587, 0.114])


def gray(img):
    if K.image_dim_ordering() == 'tf':
        return np.rollaxis(img, 0, 1).dot(to_bw)
    else:
        return np.rollaxis(img, 0, 3).dot(to_bw)


def to_plot(img):
    if K.image_dim_ordering() == 'tf':
        return np.rollaxis(img, 0, 1).astype(np.uint8)
    else:
        return np.rollaxis(img, 0, 3).astype(np.uint8)


def plot(img):
    plt.imshow(to_plot(img))


def floor(x):
    return int(math.floor(x))


def ceil(x):
    return int(math.ceil(x))


def plots(ims, figsize=(12, 6), rows=1, interp=False, titles=None):
    if type(ims[0]) is np.ndarray:
        ims = np.array(ims).astype(np.uint8)
        if (ims.shape[-1] != 3):
            ims = ims.transpose((0, 2, 3, 1))
    f = plt.figure(figsize=figsize)
    cols = len(ims) // rows if len(ims) % 2 == 0 else len(ims) // rows + 1
    for i in range(len(ims)):
        sp = f.add_subplot(rows, cols, i + 1)
        sp.axis('Off')
        if titles is not None:
            sp.set_title(titles[i], fontsize=16)
        plt.imshow(ims[i], interpolation=None if interp else 'none')


def do_clip(arr, mx):
    clipped = np.clip(arr, (1 - mx) / 1, mx)
    return clipped / clipped.sum(axis=1)[:, np.newaxis]


def get_batches(dirname, gen=image.ImageDataGenerator(), shuffle=True, batch_size=4, class_mode='categorical',
                target_size=(224, 224)):
    return gen.flow_from_directory(dirname, target_size=target_size,
                                   class_mode=class_mode, shuffle=shuffle, batch_size=batch_size)


def onehot(x):
    return to_categorical(x)


def wrap_config(layer):
    return {'class_name': layer.__class__.__name__, 'config': layer.get_config()}


def copy_weights(from_layers, to_layers):
    for from_layer, to_layer in zip(from_layers, to_layers):
        to_layer.set_weights(from_layer.get_weights())


def adjust_dropout(weights, prev_p, new_p):
    scal = (1 - prev_p) / (1 - new_p)
    return [o * scal for o in weights]


def get_data(path, target_size=(224, 224)):
    batches = get_batches(path, shuffle=False, batch_size=1, class_mode=None, target_size=target_size)
    return np.concatenate([batches.next() for i in range(batches.nb_sample)])


def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    (This function is copied from the scikit docs.)
    """
    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print(cm)
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j], horizontalalignment="center", color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def save_array(fname, arr):
    c = bcolz.carray(arr, rootdir=fname, mode='w')
    c.flush()


def load_array(fname):
    return bcolz.open(fname)[:]


def mk_size(img, r2c):
    r, c, _ = img.shape
    curr_r2c = r / c
    new_r, new_c = r, c
    if r2c > curr_r2c:
        new_r = floor(c * r2c)
    else:
        new_c = floor(r / r2c)
    arr = np.zeros((new_r, new_c, 3), dtype=np.float32)
    r2 = (new_r - r) // 2
    c2 = (new_c - c) // 2
    arr[floor(r2):floor(r2) + r, floor(c2):floor(c2) + c] = img
    return arr


def mk_square(img):
    x, y, _ = img.shape
    maxs = max(img.shape[:2])
    y2 = (maxs - y) // 2
    x2 = (maxs - x) // 2
    arr = np.zeros((maxs, maxs, 3), dtype=np.float32)
    arr[floor(x2):floor(x2) + x, floor(y2):floor(y2) + y] = img
    return arr


def vgg_ft(out_dim):
    vgg = Vgg16()
    vgg.ft(out_dim)
    model = vgg.model
    return model


def get_classes(path):
    batches = get_batches(path + 'train', shuffle=False, batch_size=1)
    val_batches = get_batches(path + 'valid', shuffle=False, batch_size=1)
    test_batches = get_batches(path + 'test', shuffle=False, batch_size=1)
    return (val_batches.classes, batches.classes, onehot(val_batches.classes), onehot(batches.classes),
            val_batches.filenames, batches.filenames, test_batches.filenames)


def split_at(model, layer_type):
    layers = model.layers
    layer_idx = [index for index, layer in enumerate(layers)
                 if type(layer) is layer_type][-1]
    return layers[:layer_idx + 1], layers[layer_idx + 1:]


class MixIterator(object):
    def __init__(self, iters):
        self.iters = iters
        self.multi = type(iters) is list
        if self.multi:
            self.N = sum([it[0].N for it in self.iters])
        else:
            self.N = sum([it.N for it in self.iters])

    def reset(self):
        for it in self.iters: it.reset()

    def __iter__(self):
        return self

    def next(self, *args, **kwargs):
        if self.multi:
            nexts = [[next(it) for it in o] for o in self.iters]
            n0 = np.concatenate([n[0] for n in nexts])
            n1 = np.concatenate([n[1] for n in nexts])
            return (n0, n1)
        else:
            nexts = [next(it) for it in self.iters]
            n0 = np.concatenate([n[0] for n in nexts])
            n1 = np.concatenate([n[1] for n in nexts])
            return (n0, n1)
