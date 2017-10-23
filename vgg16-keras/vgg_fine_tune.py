from __future__ import division, print_function

from vgg16 import Vgg16

batch_size = 64
data_path = "data/"
model_path = "models/"

vgg = Vgg16(model_path)

batches = vgg.get_batches(data_path + 'train', batch_size=batch_size)
val_batches = vgg.get_batches(data_path + 'valid', batch_size=batch_size)

vgg.fine_tune(batches)

vgg.fit(batches, val_batches, nb_epoch=1)
