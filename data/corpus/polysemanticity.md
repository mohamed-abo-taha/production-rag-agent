# Polysemanticity

Source: Wikipedia (https://en.wikipedia.org/wiki/Polysemanticity)

Polysemanticity is a phenomenon in neural networks in which individual neurons respond to multiple unrelated concepts rather than to a single well-defined one. A polysemantic neuron might activate for legal text, DNA sequences, and Hebrew script simultaneously. Because such neurons cannot be straightforwardly interpreted, polysemanticity is a central obstacle in mechanistic interpretability.


== Background ==
Mechanistic interpretability often begins from the hope that internal model components correspond to human-readable concepts. In practice, many neurons in trained models activate across semantically unrelated inputs, making them difficult to analyze in isolation. A major theoretical treatment of the phenomenon came in a 2022 paper by Nelson Elhage and colleagues at Anthropic, which argued that polysemanticity can arise from superposition and studied it in controlled toy models.


== Superposition hypothesis ==
The dominant explanation for polysemanticity is the superposition hypothesis. Real-world data contains more distinct features than a network has neurons. A network can therefore represent more features than it has dimensions by encoding them as overlapping linear combinations across many neurons. The trade-off is that individual neurons end up responsive to multiple unrelated features that share representational directions. Elhage et al. argued that this trade-off can be loss-minimizing, increasing representational capacity at the expense of interpretability.


== Sparse autoencoders ==
One approach to recovering interpretable structure from polysemantic representations is to train a sparse autoencoder on the activations of the model being studied. The autoencoder learns a larger set of directions, each of which ideally corresponds to a single concept. A 2023 Anthropic paper reported that dictionary learning could decompose a 512-neuron transformer layer into more than 4,000 such features. A 2024 follow-up applied the technique to Claude 3 Sonnet and reported many interpretable features, including some that appeared safety-relevant.
MIT Technology Review named mechanistic interpretability one of its ten breakthrough technologies of 2026.


== References ==