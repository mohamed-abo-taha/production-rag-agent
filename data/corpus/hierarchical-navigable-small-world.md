# Hierarchical navigable small world

Source: Wikipedia (https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world)

Hierarchical navigable small world (HNSW) is an algorithm for approximate nearest neighbor search. It is used to find items that are similar to a query item in a large collection, without comparing the query with every item one by one.
The algorithm is commonly used for searching vector data. In these systems, an item such as a document, image, song, or user profile is represented by a list of numbers called a vector. Items with similar vectors are treated as similar according to the model that produced the vectors. HNSW provides a way to search these vectors quickly, especially in large datasets.
HNSW stores vectors in a graph. Each vector is a node, and links connect it to some nearby vectors. The graph has several layers: upper layers contain fewer nodes and act like a rough map, while the bottom layer contains all nodes and gives a more detailed view. A search starts in an upper layer, follows links toward nodes that are closer to the query, and then repeats the process in lower layers until it finds a set of likely nearest neighbors.


== Background ==
The nearest neighbor search problem asks which items in a dataset are closest to a query item. A direct search can compare the query with every item in the dataset, but this becomes slow when the dataset is large. Exact search methods based on spatial trees, such as the k-d tree and R-tree, can also become less effective for high-dimensional data, a problem often associated with the curse of dimensionality.
Approximate nearest neighbor methods trade some exactness for speed or lower resource use. Instead of always guaranteeing the exact closest item, they try to return close items quickly. Other approximate methods include locality-sensitive hashing and product quantization.
HNSW builds on research into small-world networks and navigable graphs. In a small-world graph, most nodes can be reached from other nodes through a short chain of links. In a navigable graph, a search procedure can use local information to move toward a target. Jon Kleinberg's work on navigation in small-world networks is an important example of this research area. Later work studied ways to add links that make graphs easier to navigate greedily.
The HNSW algorithm extends earlier navigable small world methods for similarity search by adding a hierarchy of graph layers. This hierarchy helps the algorithm find a good region of the graph before doing a more detailed search in the bottom layer.


== Algorithm ==
HNSW is based on a proximity graph. In this graph, nearby vectors are connected by edges. The algorithm uses these edges to move through the dataset, rather than scanning every vector.
The graph is hierarchical. Every vector appears in the bottom layer. Some vectors are also placed in higher layers, with fewer vectors appearing as the layers go upward. The upper layers allow long-range movement across the dataset, while the lower layers allow a more detailed search near promising candidates.
A typical search proceeds as follows:

The search begins from an entry point in the highest layer.
At each step, the algorithm looks at neighboring nodes and moves to a neighbor that is closer to the query.
When it cannot find a closer neighbor in that layer, it moves down to the next layer.
In the bottom layer, it explores a wider set of candidate nodes and returns the nearest candidates found.
This search strategy is often described as greedy navigation. The algorithm repeatedly chooses locally better nodes, using the graph structure to approach the query point.


== Construction and parameters ==
The HNSW graph is built incrementally. When a new vector is inserted, the algorithm assigns it a maximum layer, searches for nearby existing nodes, and connects the new node to selected neighbors in each layer where it appears.
Implementations usually expose parameters that control the trade-off between speed, accuracy, memory use, and construction time. A higher number of graph connections can improve recall but requires more memory. A larger search candidate list can improve accuracy but makes queries slower. A larger construction candidate list can improve the quality of the graph but makes index building slower.
Because HNSW is approximate, its results are not always identical to a full exact search. Its practical performance depends on the dataset, distance measure, implementation, and parameter settings. Benchmarking studies have found HNSW-based libraries to be strong performers among approximate nearest neighbor methods, although worst-case performance can differ from performance on common benchmark datasets.


== Use in vector search systems ==
HNSW is used as an index in systems that store and search high-dimensional vectors. These systems include vector databases, search engines, and database extensions. Typical uses include semantic search, recommender systems, image similarity search, and retrieval-augmented generation.
Several software projects implement or support HNSW. Libraries include hnswlib, which is associated with the original HNSW authors, and FAISS. Database and search systems that document HNSW support include Apache Lucene, Chroma, ClickHouse, DuckDB, MariaDB, Milvus, pgvector, Qdrant, and Redis.


== See also ==
Approximate nearest neighbor search
Vector database
Locality-sensitive hashing
Product quantization


== References ==