data_path = '/data'
train_file = open("train.txt", 'w')

for i in range(0,10000):
    train_file.write("%s/cat.%s.jpg 0" % (data_path,i))
    train_file.write('\n')

    train_file.write("%s/dog.%s.jpg 1" % (data_path,i))
    train_file.write('\n')

train_file.flush()
train_file.close()

test_file = open("test.txt", 'w')

for i in range(10000,12500):
    test_file.write("%s/cat.%s.jpg 0" % (data_path,i))
    test_file.write('\n')

    test_file.write("%s/dog.%s.jpg 1" % (data_path,i))
    test_file.write('\n')


test_file.flush()
test_file.close()