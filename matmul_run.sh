#!/bin/sh
#python timer.py [vector/matrix size] [size increment] [json] [times to run] [output filename]
python timer.py 5000 50 '{
   "columns":[
      "Matrix size",
      "Tensorflow (built-in)",
      "Tensorflow (replicate)",
      "Tensorflow (no-op)",
      "Accelerate (replicate)",
      "Accelerate (divide-and-conquer)",
      "Accelerate (no-op)"
   ],
   "python":[
      {
         "filename":"matmul.py",
         "maxDim":5000,
         "args":["builtin"]
      },
      {
         "filename":"matmul.py",
         "maxDim":300,
         "args":["replicate"]
      },
      {
         "filename":"matmul.py",
         "maxDim":5000,
         "args":["noop"]
      }
   ],
   "stack":[
      {
         "filename":"examples-hs-exe",
         "maxDim":850,
         "args":["mmult_repl"]
      },
      {
         "filename":"examples-hs-exe",
         "maxDim":1500,
         "args":["mmult_divconq"]
      },
      {
         "filename":"examples-hs-exe",
         "maxDim":5000,
         "args":["noop"]
      }
   ]
}' 10 "matmul_results-"
