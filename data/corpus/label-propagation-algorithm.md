# Label propagation algorithm

Source: Wikipedia (https://en.wikipedia.org/wiki/Label_propagation_algorithm)

Label propagation is a semi-supervised algorithm in machine learning that assigns labels to previously unlabeled data points. At the start of the algorithm, a (generally small) subset of the data points have labels (or classifications). These labels are propagated to the unlabeled points throughout the course of the algorithm.
Within complex networks, real networks tend to have community structure. Label propagation is an algorithm  for finding communities. In comparison with other algorithms label propagation has advantages in its running time and amount of a priori information needed about the network structure (no parameter is required to be known beforehand). The disadvantage is that it produces no unique solution, but an aggregate of many solutions.


== Functioning of the algorithm ==
At initial condition, the nodes carry a label that denotes the community they belong to. Membership in a community changes based on the labels that the neighboring nodes possess. This change is subject to the maximum number of labels within one degree of the nodes. Every node is initialized with a unique label, then the labels diffuse through the network. Consequently, densely connected groups reach a common label quickly. When many such dense (consensus) groups are created throughout the network, they continue to expand outwards until it is impossible to do so.
The process has 5 steps:
1. Initialize the labels at all nodes in the network. For a given node x, Cx (0) = x.
2. Set t = 1.
3. Arrange the nodes in the network in a random order and set it to X.
4. For each x ∈ X chosen in that specific order, let Cx(t) = f(Cxi1(t), ...,Cxim(t),Cxi(m+1) (t − 1), ...,Cxik (t − 1)). Here returns the label occurring with the highest frequency among neighbours. Select a label at random if there are multiple highest frequency labels.
5. If every node has a label that the maximum number of their neighbours have, then stop the algorithm. Else, set t = t + 1 and go to (3).


== Application in text classification and machine learning ==
Label propagation offers an efficient solution to the challenge of labeling datasets in machine learning by reducing the need for manual labels. Text classification utilizes a graph-based technique, where the nearest neighbor graph is built from network embeddings, and labels are extended based on cosine similarity by merging these pseudo-labeled data points into supervised learning. 


== Multiple community structure ==
In contrast with other algorithms label propagation can result in various community structures from the same initial condition. The range of solutions can be narrowed if some nodes are given preliminary labels while others are held unlabelled. Consequently, unlabelled nodes will be more likely to adapt to the labelled ones. For a more accurate finding of communities, Jaccard’s index is used to aggregate multiple community structures, containing all important information.


== References ==


== External links ==
Python implementation of label propagation algorithm.