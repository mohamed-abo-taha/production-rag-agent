# TabPFN

Source: Wikipedia (https://en.wikipedia.org/wiki/TabPFN)

TabPFN (Tabular Prior-data Fitted Network) is a machine learning model for tabular datasets proposed in 2022. It uses a transformer architecture. It is intended for supervised classification and regression analysis on tabular datasets, particularly focusing on small- to medium-sized datasets. The latest version, TabPFN-3, was released in May 2026 and supports datasets with up to one million  rows and 200 features. 


== History ==
TabPFN was first introduced in a 2022 pre-print and presented at ICLR 2023. TabPFN v2 was published in 2025 in Nature by Hollmann and co-authors. The source code is published on GitHub under a modified Apache License and on PyPi. Writing for ICLR blogs, McCarter states that the model has attracted attention due to its performance on small dataset benchmarks. TabPFN v2.5 was released on November 6, 2025. TabPFN-3 was released on May 12, 2026.
Prior Labs, founded in 2024, aims to commercialize TabPFN.
As of April 2026, the open-source TabPFN repository had more than 6,000 stars on GitHub.


== Overview and pre-training ==
TabPFN supports classification, regression and generative tasks. It leverages "Prior-Data Fitted Networks" models to model tabular data. By using a transformer pre-trained on synthetic tabular datasets, TabPFN avoids benchmark contamination and costs of curating real-world data.
TabPFN v2 was pre-trained on approximately 130 million such datasets. Synthetic datasets are generated using causal models or Bayesian neural networks; this can include simulating missing values, imbalanced data, and noise. Random inputs are passed through these models to generate outputs, with a bias towards simpler causal structures. During pre-training, TabPFN predicts the masked target values of new data points given training data points and their known targets, effectively learning a generic learning algorithm that is executed by running a neural network forward pass. The new dataset is then processed in a single forward pass without retraining. The model's transformer encoder processes features and labels by alternating attention across rows and columns. TabPFN v2 handles numerical and categorical features, missing values, and supports tasks like regression and synthetic data generation, while TabPFN-2.5 scales this approach to datasets with up to 50,000 rows and 2,000 features. TabPFN-3 introduced a redesigned architecture with row-compression, an attention-based many-class decoder, native missing-value handling, and inference optimizations such as row chunking and a reduced key-value cache, with benchmark-validated regimes of up to 1 million rows with 200 features, 100,000 rows with 2,000 features, or 1,000 rows with 20,000 features.
Since TabPFN is pre-trained, in contrast to other deep learning methods, it does not require costly hyperparameter optimization.


== Research ==
TabPFN is the subject of on-going research. Applications for TabPFN have been investigated for domains such as chemoproteomics, insurance risk classification, and metagenomics.
In clinical research, TabPFN was used in a study on the early detection of pancreatic cancer from blood samples, where it was combined with metabolomic data and reported high diagnostic performance.


== Applications ==
TabPFN has been used in industrial and biomedical contexts. Hitachi Ltd. has been reported to use the model for predictive maintenance in rail networks, with its use described as helping to identify track issues earlier and reduce manual inspections.
In the biomedical domain, Oxford Cancer Analytics has used TabPFN in the analysis of proteomic data in lung disease research.
A 2025 ML Contests report noted that the winners of DrivenData's PREPARE challenge used TabPFN to generate features for gradient-boosted decision tree models.


== Limitations ==
TabPFN has been criticized for its "one large neural network is all you need" approach to modeling problems. Further, its performance is limited in high-dimensional and large-scale datasets.


== Scaling Mode ==
In late November 2025, Prior Labs introduced ‘‘Scaling Mode’’, an operating mode for TabPFN designed to remove the fixed upper bound on training set size. Earlier versions of TabPFN had been optimized and validated primarily for datasets of up to 100,000 rows, whereas Scaling Mode was reported to extend support to substantially larger datasets, with benchmarked experiments on datasets containing up to 10 million rows.
According to Prior Labs, Scaling Mode preserves the existing TabPFN architecture, including its alternating row-attention and column-attention design, as well as the same feature-count limits as prior releases. Inference remains based on a single forward pass rather than dataset-specific gradient-descent training, while scalability is described as being constrained primarily by available compute and memory resources.
Prior Labs reported benchmark results on an internal collection of datasets ranging from 1 million to 10 million rows across industry and scientific applications. In these benchmarks, Scaling Mode was compared with CatBoost, XGBoost, LightGBM, and TabPFN 2.5 using 50,000-row subsampling. The company stated that predictive performance improved monotonically with increasing training set size and that no diminishing returns from scaling were observed within the tested range.
Prior Labs also announced the release through company and executive social media channels.
TabPFN-3 later incorporated related scaling improvements, including row chunking and a reduced key-value cache, into the model architecture and inference pipeline.


== See also ==
XGBoost
LightGBM
CatBoost


== References ==


== External links ==
TabPFN on GitHub