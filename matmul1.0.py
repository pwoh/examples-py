import tensorflow as tf
import sys
from tensorflow.python.client import timeline

dim = int(sys.argv[1])
repeat = int(sys.argv[2])
whichmatmul = sys.argv[3]
timeline_on = False

# Build a graph.

repeat = 1
if len(sys.argv) == 5:
    timeline_on = sys.argv[4] == 'timeline_on'

for _ in range(0, repeat):
    a = tf.random_uniform([dim, dim], tf.float32.min, tf.float32.max, tf.float32)
    b = tf.random_uniform([dim, dim], tf.float32.min, tf.float32.max, tf.float32)
    if whichmatmul == 'builtin':
        c = tf.matmul(a, b)
    elif whichmatmul == 'replicate':
        ar = dim
        ac_br = dim
        bc = dim
        b_rep = tf.reshape(tf.tile(tf.transpose(b), [ar,1]), [ar,bc,ac_br]) 
        a_rep = tf.reshape(tf.tile(a, [1,bc]), [ar,bc,ac_br])
        c = tf.reduce_sum(tf.multiply(a_rep, b_rep), 2)
    else:
        c = tf.no_op()

    # Evaluate the tensor `c`.
    with tf.Session() as sess:
        run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
        run_metadata = tf.RunMetadata()
        sess.run([a,b,c], options=run_options, run_metadata=run_metadata)

        if timeline_on:
            #Create the Timeline object, and write it to a json
            tl = timeline.Timeline(run_metadata.step_stats)
            ctf = tl.generate_chrome_trace_format()
            with open(str(dim) + 'timeline_matmul_'+whichmatmul+'.json', 'w') as f:
                f.write(ctf)

    sess.close()

try:
    sys.stdout.close()
except:
    pass
try:
    sys.stderr.close()
except:
    pass
    #http://stackoverflow.com/questions/34293714/tensorflow-can-i-measure-the-execution-time-of-individual-operations
    #You can then open Google Chrome, go to the page chrome://tracing and load the timeline.json file.

    #out of memory for 500:  failed to alloc 4294967296 bytes on host: CUDA_ERROR_OUT_OF_MEMORY
