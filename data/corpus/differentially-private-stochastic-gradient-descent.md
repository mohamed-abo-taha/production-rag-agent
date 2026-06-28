# Differentially private stochastic gradient descent

Source: Wikipedia (https://en.wikipedia.org/wiki/Differentially_private_stochastic_gradient_descent)

Differentially private stochastic gradient descent (DP-SGD) is an algorithmic technique for learning and a refined analysis of privacy costs within the framework of differential privacy. DP-SGD was introduced by Abadi et al. at the 2016 ACM Conference on Computer and Communications Security. A fundamental challenge is the privacy-utility trade-off, where stronger privacy requires more noise or larger privacy budgets, potentially reducing model accuracy. DP-SGD is used in domains with sensitive data, including healthcare, social media and cybersecurity. DP-SGD can demonstrate that deep neural networks with non-convex objectives may be trained under a modest privacy budget. This is achieved at a manageable cost in software complexity, training efficiency, and model quality. DP-SGD has become a standard for privacy-preserving learning from large datasets. Existing approaches require large privacy budgets to train and incur high overheads in computational resources. DP-SGD follows the same steps as standard stochastic gradient descent (SGD) but clips the gradients' norm to a threshold, before adding Gaussian noise. Differential privacy is formally defined using the parameters (ε, δ), which bound the privacy loss of any algorithm. It can also track detailed information about the privacy loss by a method called the moments accountant. Current implementations often use a method called Rényi differential privacy, which provides even tighter privacy accounting than the original moments accountant. Another alternative privacy-preserving training method is Private Aggregation of Teacher Ensembles (PATE), which uses an ensemble of teacher models to label public data.


== Description ==
DP-SGD was introduced by Abadi et al. at the 2016 ACM Conference on Computer and Communications Security. Standard SGD computes gradients over mini batches. Differential privacy is defined by parameters (ε, δ), which bound the privacy loss of any algorithm. These gradients can then reveal information about individual training examples. DP-SGD can modify this process to provide privacy guarantees. There are three steps in DP-SGD, including per-sample gradient computation, gradient clipping, and Gaussian noise addition. It first computes gradients for each training example in the batch. Then, it clips the L2 norm, the straight-line distance from the origin to the point represented by the vector, of each gradient to a threshold C. Finally, it adds Gaussian noise to the clipped gradients, before averaging them out. DP-SGD typically uses Poisson subsampling, where each mini-batch is formed by sampling each example independently with probability q. This provides privacy amplification by subsampling. The privacy parameters include the clipping norm (C) and the noise scale (σ). These parameters can determine the privacy-utility trade-off. The noise scale σ is calibrated such that the noise variance is proportional to C²σ². Unlike standard SGD, DP-SGD's privacy loss accumulates over multiple training steps, and the moments accountant can track this cumulative loss to determine the overall privacy guarantee, usually denoted as ε, δ. Hence, it provides much tighter estimates on the overall privacy loss.


== Privacy accounting ==
Unlike standard SGD, DP-SGD's privacy loss accumulates over every gradient step over multiple epochs. To provide a formal guarantee, it must account for these steps combined.


=== Moments accountant ===
The moments accountant tracks the privacy loss as a random variable at each step. Rather than just tracking the average privacy loss, it also tracks higher-order moments, which are statistical measures like variance, kurtosis and skewness that describe the shape of the privacy loss distribution. This can allow it to bound the tail probability, the probability that a variable takes a value in the extreme end of its distribution, of the privacy loss distribution more tightly. Therefore, it yields a much tighter estimate for the overall privacy guarantee (ε, δ) than methods that only track the average privacy loss. An alternative to the moments accountant is Rényi differential privacy (RDP), which provides tighter privacy bounds by tracking Rényi divergences of order α. RDP accounting has become the standard method in modern implementations.


=== Implications ===
The moments accountant allows practitioners to train deep neural networks under a single-digit privacy budget. It can also allow the noise scale σ to be calibrated to achieve a desired (ε, δ) guarantee. Without the moments accountant, the privacy budget would be consumed much faster, forcing practitioners to use more noise or train for fewer steps, which would harm accuracy and performance.


== Applications and challenges ==
DP-SGD has become the de facto standard for privacy-preserving learning from large datasets. It is used in domains where training data contains sensitive personal information. Examples of these kinds of datasets include healthcare, social media and cybersecurity.
Challenges include large privacy budgets, computational and memory overhead and privacy-utility trade-offs. Training accurate models often consumes large amounts of privacy budget, which degrades utility. There are also significant computational and memory overheads, since per-sample gradient computation is computation-heavy and there is always a trade-off between protection and model accuracy.
An alternative privacy-preserving training method includes Private Aggregation of Teacher Ensembles (PATE). PATE trains an ensemble of teacher models on subsets of private data, then uses that ensemble to label a public dataset for training a student model.


== Research directions ==
The research directions of DP-SGD include adaptive techniques like clipping threshold, learning rate, or budget allocation to improve the trade-off. A second direction is individualized privacy, which allows different users to have different privacy requirements. It also includes benchmarking, which compares different approaches head-to-head on common datasets. Empirical privacy auditing has also emerged as a method to assess actual privacy protection.


== References ==