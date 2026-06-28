# Knowledge cutoff

Source: Wikipedia (https://en.wikipedia.org/wiki/Knowledge_cutoff)

In machine learning, a knowledge cutoff (or data cutoff) is the point in time beyond which a model has not been trained on new data. The term is used in reference to large language models. Large language models are pretrained ahead of time. After that, the model's knowledge is fixed. Any information about events after this date is absent from the model's training data. The model cannot access information about later events without a system for real-time data access like retrieval-augmented generation, which is a technique that fetches new information from an external database. While simple for training and tuning large language models, knowledge cutoffs introduce new limitations like erroneous AI-generated content, information gaps, and reduced accuracy on evolving knowledge. A later knowledge cutoff may achieve higher accuracy in time-sensitive tasks.


== Description ==
A large language model is pretrained ahead of time on static snapshots of data collected from the internet, books, and other sources up to a specific knowledge cutoff date. During pretraining, an AI model can learn linguistic patterns, semantics, and contextual meanings. The model can then learn probabilities and predict what word is likely to come next. After pretraining, the model's knowledge is fixed. Therefore, a model with a fixed knowledge cutoff is unable to provide information on facts or developments that have emerged since that time because the model is not connected to the internet. As a result, it may occasionally produce incorrect answers. Training on newer data would create a major price concern, since training the most powerful large language models may soon cost over a billion dollars according to Time.
AI model cutoff dates include:

The GPT-4 model has a knowledge cutoff of September 2021.
The GPT-4 Turbo model has a knowledge cutoff of December 2023.
The GPT-5 model has a knowledge cutoff of September 2024.
The Llama 4 models have a knowledge cutoff of August 2024.
The GPT-OSS models have a knowledge cutoff of May 2024.


== Effects ==


=== Knowledge gaps ===
Knowledge cutoffs create information gaps, where the model lacks any knowledge of events or discoveries that are not included in its training data. This can lead to erroneous AI-generated content. Such inaccuracies occur because large language models are designed to predict and generate the most probable sequence of words based on their training patterns, which may result in confident but incorrect outputs when queried beyond the information present in its training data.


=== Effective vs. reported dates ===
A study by Pęzik et al. at the University of Łódź indicates that a model's actual knowledge does not always match its official cutoff date. This effective cutoff, the date up to which it can reliably know information, often differs for various subjects and is influenced by the distribution of information within the training data itself, meaning some topics may reflect later knowledge than others while knowledge that predates the cutoff may be absent. This is because the training data contains uneven information across topics. Due to the high cost of retraining large language models, these models are rarely completely retrained to increase their knowledge cutoff. Some models can also use integrated search tools to access more recent information, which makes it unclear whether an answer comes from the model's original training or from a live search. For example, GPT-4 can access its search tool and give real-time information.


=== Real-world impact ===
A study by Cacioli et al. at Oregon State University demonstrated the real-world impact of a knowledge cutoff. Researchers created a 363-question benchmark based on two versions of the IDSA's COVID-19 treatment guidelines. Models whose knowledge cutoffs predated the newer guideline, like GPT-3.5-Turbo and Llama-2, performed worse on these questions, at 76.03% and 25.26% respectively. In contrast, the models with knowledge cutoffs after the guideline, like GPT-4o and Llama 3.3, achieved over 90% accuracy. These findings show that clinical reliability improves as models incorporate newer knowledge cutoffs.


== Mitigation strategies ==


=== Retrieval-augmented generation ===

Retrieval-augmented generation is a framework that augments a large language model with updated data from external sources, allowing it to generate more informed responses. In a retrieval-augmented generation system, the language model is connected to an external knowledge base or search engine to retrieve live data. This architecture allows the model to find current information relevant to a query and incorporate it into its response, with citations. Grounding a model in external data, which ties a model's answers to its retrieved sources, helps reduce the frequency of erroneous AI-generated content and improves output accuracy. However, the external knowledge base might be outdated or contain biases, which may also lead to incorrect information or hallucinations. For example, Google AI Overviews have created false claims, and the results are sometimes unreliable, since the model may either misinterpret the prompt or fail to retrieve high-quality sources. However, a method to mitigate this is to apply techniques like reinforcement learning from human feedback. Reinforcement learning from human feedback is a technique to align an AI model with human preferences. This technique can enhance the quality and reliability of a large language model's responses.


=== Continual learning ===

Another approach is continual learning. Continual learning is a method of machine learning where new data is continuously used to extend the existing model's knowledge, and it aims to prevent catastrophic forgetting, which is a tendency for AI to abruptly forget about what it has already learned. In practice however, it often fails to do so completely. This technique allows efficient, incremental updates to a model without the high cost of a full retraining cycle. One method of continual learning is a technique called fine-tuning, which allows AI labs to precisely adjust an AI model's behavior. A more efficient way of fine-tuning involves methods like Low-Rank Adaptation.  However, this does not give real-time awareness, since adding modules to the system may result in catastrophic forgetting, as the weights in the model become biased towards the new set of data.


== References ==