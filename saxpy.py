import tensorflow as tf
import sys
from tensorflow.python.client import timeline

saxpy_unvectorised = lambda xs, ys: tf.map_fn(lambda x: 11.0*x[0] + x[1], (xs,ys), dtype=tf.float32)
saxpy_vectorised = lambda xs, ys: tf.add(tf.multiply(11.0,xs),ys)

dim = int(sys.argv[1])
repeat = int(sys.argv[2])
whichsaxpy = sys.argv[3]
timeline_on = False

# Build a graph.

repeat = 1
if len(sys.argv) == 5:
    timeline_on = sys.argv[4] == 'timeline_on'

for _ in range(0, repeat):
    a = tf.random_uniform([dim], tf.float32.min, tf.float32.max, tf.float32)
    b = tf.random_uniform([dim], tf.float32.min, tf.float32.max, tf.float32)
    if whichsaxpy == 'unvectorised':
        c = saxpy_unvectorised(a,b)
    elif whichsaxpy == 'vectorised':
        c = saxpy_vectorised(a,b)
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
            with open(str(dim) + 'timeline_dotp_'+whichsaxpy+'.json', 'w') as f:
                f.write(ctf)

    sess.close()

    #http://stackoverflow.com/questions/34293714/tensorflow-can-i-measure-the-execution-time-of-individual-operations
    #You can then open Google Chrome, go to the page chrome://tracing and load the timeline.json file.

    #out of memory for 500:  failed to alloc 4294967296 bytes on host: CUDA_ERROR_OUT_OF_MEMORY
try:
    sys.stdout.close()
except:
    pass
try:
    sys.stderr.close()
except:
    pass