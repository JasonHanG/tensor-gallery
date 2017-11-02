import tensorflow as tf

W = tf.Variable(10)
assign_op = W.assign(100)

with tf.Session() as sess:
    sess.run(W.initializer)
    print(W.eval())  # >> 10
    print(sess.run(assign_op))  # >> 100

my_var = tf.Variable(2, name="my_var")

my_var_times_two = my_var.assign(2 * my_var)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print(sess.run(my_var_times_two))  # >> 4
    print(sess.run(my_var_times_two))  # >> 8
    print(sess.run(my_var_times_two))  # >> 16

W = tf.Variable(10)
sess1 = tf.Session()
sess2 = tf.Session()

sess1.run(W.initializer)
sess2.run(W.initializer)

print(sess1.run(W.assign_add(10)))  # >> 20
print(sess2.run(W.assign_sub(2)))  # >> 8

print(sess1.run(W.assign_add(100)))  # >> 120
print(sess2.run(W.assign_sub(50)))  # >> -42

sess1.close()
sess2.close()
