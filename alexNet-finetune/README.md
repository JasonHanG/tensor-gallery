## AlexNet Fine-tuning
Simple fine-tuning code for alexNet to classify cats vs dogs.  
Original author: Frederik Kratzert (contact: f.kratzert@gmail.com)  
[Post](https://kratzert.github.io/2017/02/24/finetuning-alexnet-with-tensorflow.html)


#### 1.Content

- `alexnet.py`: Class with the graph definition of the AlexNet.
- `finetune.py`: Script to run the finetuning process.
- `datagenerator.py`: Contains a wrapper class for the new input pipeline.
- `caffe_classes.py`: List of the 1000 class names of ImageNet (copied from [here](http://www.cs.toronto.edu/~guerzhoy/tf_alexnet/)).

#### 2.Usage
- Download data from [here](https://www.kaggle.com/c/dogs-vs-cats-redux-kernels-edition/data)
- You have to provide two `.txt` files to the script (`train.txt` and `val.txt`). Each of them list the complete path to your train/val images together with the class number in the following structure.
see "train_test_list_file_gen.py" for example.
```
Example train.txt:
/path/to/train/image1.png 0
/path/to/train/image2.png 1
/path/to/train/image3.png 2
/path/to/train/image4.png 0
.
```
were the first column is the path and the second the class label.

- Run script finetune.py

#### 3.Depedencies

- TensorFlow >= 1.12
