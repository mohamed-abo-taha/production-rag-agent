# JAX (software)

Source: Wikipedia (https://en.wikipedia.org/wiki/JAX_%28software%29)

JAX is a Python library for accelerator-oriented array computation and program transformation, designed for high-performance numerical computing and large-scale machine learning. It is developed by Google with contributions from Nvidia and other community contributors.
It is described as bringing together a modified version of the automatic differentiation system autograd and OpenXLA's XLA (Accelerated Linear Algebra). It is designed to follow the structure and workflow of NumPy as closely as possible and works with various existing frameworks such as TensorFlow and PyTorch. The primary features of JAX are:

Providing a unified NumPy-like interface to computations that run on CPU, GPU, or TPU, in local or distributed settings.
Built-in Just-In-Time (JIT) compilation via OpenXLA, an open-source machine learning compiler ecosystem.
Efficient evaluation of gradients via its automatic differentiation transformations.
Automatic vectorization to efficiently map functions over arrays representing batches of inputs.


== Libraries using Jax ==
Flax 
Equinox 
Optax 
Diffrax


== See also ==
NumPy
TensorFlow
PyTorch
CUDA
Accelerated Linear Algebra
Comparison of machine learning software
List of numerical libraries


== External links ==
Documentationː docs.jax.dev
Colab (Jupyter/iPython) Quickstart Guideː colab.research.google.com/github/google/jax/blob/main/docs/notebooks/thinking_in_jax.ipynb
TensorFlow's XLAː www.tensorflow.org/xla (Accelerated Linear Algebra)
YouTube TensorFlow Channel "Intro to JAX: Accelerating Machine Learning research": www.youtube.com/watch?v=WdTeDXsOSj4
Original paperː mlsys.org/Conferences/doc/2018/146.pdf


== References ==