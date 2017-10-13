import tensorflow as tf
import sys
from tensorflow.python.client import timeline

riskfree   = 0.02
volatility = 0.30

horner = lambda coeff, x: x * tf.foldr(lambda a, b: a + x*b, coeff)

rsqrt2pi = 0.39894228040143267793994605993438
coeff    = [0.31938153,-0.356563782,1.781477937,-1.821255978,1.330274429]
cnd1 = lambda d: rsqrt2pi * tf.exp (-0.5*d*d) * horner(coeff, 1.0 / (1.0 + 0.2316419 * abs(d)))

def cnd(d):
    return cnd1(d)
    # c = tf.Variable(cnd1(d),validate_shape=False)
    # return tf.cond(tf.reshape(d,[]) > 0, lambda: 1.0 - c, lambda: c)

def blackscholes((price, strike, years)):
    r = tf.constant(riskfree)
    v = tf.constant(volatility)
    v_sqrtT = (v * tf.sqrt(years))
    d1      = (tf.log (price / strike) + (r + 0.5 * v * v) * years) / v_sqrtT
    d2      = (d1 - v_sqrtT)
    cndD1   = cnd(d1)
    cndD2   = cnd(d2)
    x_expRT = (strike * tf.exp (-r * years))
    V_call = price * cndD1 - x_expRT * cndD2
    V_put = x_expRT * (1.0 - cndD2) - price * (1.0 - cndD1)
    return (V_call, V_put)

dim = int(sys.argv[1])
repeat = int(sys.argv[2])
whichbs = sys.argv[3]
timeline_on = False

# Build a graph.

repeat = 1
if len(sys.argv) == 5:
    timeline_on = sys.argv[4] == 'timeline_on'

for _ in range(0, repeat):
    # Randomly generate [dim] number of options, and map blackscholes over all of them
    prices = tf.random_uniform([dim], 5.0, 30.0, tf.float32)
    strikes = tf.random_uniform([dim], 1.0, 100.0, tf.float32)
    years = tf.random_uniform([dim], 0.25, 10, tf.float32) 

    if whichbs == 'map':
        elems = tf.tuple([prices,strikes,years])
        blackscholesmap = tf.map_fn(lambda (x,y,z): blackscholes((x,y,z)), elems, dtype=(tf.float32,tf.float32))
    else:
        blackscholesmap = tf.no_op()

    # Evaluate the tensor `c`.
    with tf.Session() as sess:
        run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
        run_metadata = tf.RunMetadata()

        # Add print operation
        # blackscholesmap = tf.Print(blackscholesmap, [blackscholesmap], message="Result: ")

        # init_op = tf.global_variables_initializer()
        # sess.run(init_op)

        sess.run(blackscholesmap, options=run_options, run_metadata=run_metadata)

        if timeline_on:
            #Create the Timeline object, and write it to a json
            tl = timeline.Timeline(run_metadata.step_stats)
            ctf = tl.generate_chrome_trace_format()
            with open(str(dim) + 'timeline_blackscholes_'+whichbs+'.json', 'w') as f:
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