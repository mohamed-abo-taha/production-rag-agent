# Circuit (neural network)

Source: Wikipedia (https://en.wikipedia.org/wiki/Circuit_%28neural_network%29)

A neural network circuit (also known as an artificial neural circuit or simply a circuit) is a conceptual and computational subgraph within an artificial neural network, that performs a specific, interpretable function. Inspired by and serving as a cognate to biological neural circuits, the study of artificial circuits is a primary focus of the field of mechanistic interpretability. Researchers aim to reverse-engineer "black box" deep learning models by identifying their fundamental variables – known as features – and the mathematical weights connecting them. By mapping these circuits, researchers can understand how models process information, exhibit emergent behaviors, and generate specific outputs.


== Background and biological inspiration ==
In neuroscience, a biological neural circuit is a population of interconnected neurons that carries out a specific physiological function when activated, such as a reflex arc or a visual edge detector. Analogously, in artificial neural networks, a circuit is a defined subgraph of the network's components (such as neurons, attention heads, or specific directions in activation space) that work together to compute a human-understandable algorithmic behavior.
AI researchers utilize mathematical tools, such as dictionary learning and sparse autoencoders, to probe the "anatomy" of artificial models. Researchers at Anthropic formalized this metaphor, arguing that while large language models (LLMs) are created by simple training algorithms, the internal mechanisms that emerge resemble the complexity of living organisms sculpted by evolution. By applying "circuit tracing" and generating "attribution graphs," researchers can dissect the step-by-step cognitive processes of these models, observing how distinct internal circuits interact to reach a final output.


== Foundational concepts ==
The conceptual framework of neural network circuits was heavily formalized by Chris Olah and collaborators. In the 2020 paper Zoom In: An Introduction to Circuits, the authors propose three central claims regarding artificial neural networks, initially focusing on convolutional neural networks (CNNs) used in vision models:

Features are the fundamental unit of networks: Rather than analyzing individual, highly "polysemantic" neurons (neurons that activate in response to multiple unrelated concepts due to a phenomenon known as superposition), researchers should identify "features." Features are interpretable, monosemantic properties of the input data.
Features are connected by weights: The neural network learns mathematical connections (weights) between these features.
Features form circuits: Early-layer features (such as edge, curve, or high-low frequency detectors) combine via learned weights into deeper, more complex features (such as a "dog head" or "car wheel" detector), forming a comprehensible circuit.


== Transformer circuits ==
With the rise of the transformer architecture, the focus of circuit research largely shifted from vision models to LLMs. The 2021 Anthropic paper A Mathematical Framework for Transformer Circuits introduced a linear algebra-based approach to reverse-engineering transformers.
Key components of transformer circuits include:

The Residual Stream: Viewed as the central communication channel of the network. Layers read from and write to this stream, accumulating information across the network's depth.
Attention Heads as Independent Circuits: Each attention head can be decomposed into a Query-Key (QK) circuit, which determines where the model looks in the context window, and an Output-Value (OV) circuit, which determines what information is extracted and written back to the residual stream.
Induction Heads: A well-documented type of transformer circuit consisting of two attention heads working in sequence. They are primarily responsible for in-context learning and the model's ability to recognize and continue text.
As language models have scaled, the circuits within them have become increasingly intricate. Modern circuit tracing techniques allow researchers to map the intermediate computational steps an LLM takes. For instance, researchers have identified multilingual circuits, addition circuits, and even "planning" circuits that allow a model to internally preselect rhyming words before generating a line of poetry.


== Applications ==
Understanding neural network circuits is considered a critical step in AI safety and AI alignment. By decomposing uninterpretable models into transparent circuits, researchers hope to:

Audit for bias and safety: Ensure that models are not relying on harmful stereotypes, faulty heuristics, or deceptive logic to reach their conclusions.
Predict emergent capabilities: Understand how and when models learn advanced skills. For example, the sudden formation of induction head circuits during training directly correlates with a model's sudden improvement in in-context learning.
Edit and control models: Directly intervene on a circuit to alter a model's behavior without the need for extensive retraining or fine-tuning.
As an example, the process of uncensoring a model via "abliteration" involves first detecting what feature corresponds to the undesirable behavior (referred to as the "refusal direction"), and then weakening the activation of that feature.


== Discoveries ==
In Anthropic's research with Claude 3.5 Haiku, by use of attribution graphs to activate and suppress circuits, they have concluded that the model:

"Employs remarkably general abstractions"
Forms "internally generated plans for its future outputs"
"Works backwards from its longer-term goals"
Functionally "can apparently only be faithfully described using an overwhelmingly large causal graph."
Includes "mechanisms that could underlie a simple form of metacognition"


== See also ==
Mechanistic interpretability
Artificial neural network
Neural circuit
Transformer (machine learning model)


== References ==