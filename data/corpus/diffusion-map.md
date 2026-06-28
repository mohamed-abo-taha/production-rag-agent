# Diffusion map

Source: Wikipedia (https://en.wikipedia.org/wiki/Diffusion_map)

Diffusion maps is a dimensionality reduction or feature extraction algorithm introduced by Coifman and Lafon  which computes a family of embeddings of a data set into Euclidean space (often low-dimensional) whose coordinates can be computed from the eigenvectors and eigenvalues of a diffusion operator on the data. The Euclidean distance between points in the embedded space is equal to the "diffusion distance" between probability distributions centered at those points. Different from linear dimensionality reduction methods such as principal component analysis (PCA), diffusion maps are part of the family of nonlinear dimensionality reduction methods which focus on discovering the underlying manifold that the data has been sampled from. By integrating local similarities at different scales, diffusion maps give a global description of the data-set. Compared with other methods, the diffusion map algorithm is robust to noise perturbation and computationally inexpensive.


== Definition of diffusion maps ==
Following  and , diffusion maps can be defined in four steps.


=== Connectivity ===
Diffusion maps exploit the relationship between heat diffusion and random walk Markov chain. The basic observation is that if we take a random walk on the data, walking to a nearby data-point is more likely than walking to another that is far away.  Let 
  
    
      
        (
        X
        ,
        
          
            A
          
        
        ,
        μ
        )
      
    
    {\displaystyle (X,{\mathcal {A}},\mu )}
  
 be a measure space, where 
  
    
      
        X
      
    
    {\displaystyle X}
  
 is the data set and 
  
    
      
        μ
      
    
    {\displaystyle \mu }
  
 represents the distribution of the points on 
  
    
      
        X
      
    
    {\displaystyle X}
  
.
Based on this, the connectivity 
  
    
      
        k
      
    
    {\displaystyle k}
  
 between two data points, 
  
    
      
        x
      
    
    {\displaystyle x}
  
 and 
  
    
      
        y
      
    
    {\displaystyle y}
  
, can be defined as the probability of walking from 
  
    
      
        x
      
    
    {\displaystyle x}
  
 to 
  
    
      
        y
      
    
    {\displaystyle y}
  
 in one step of the random walk. Usually, this probability is specified in terms of a kernel function of the two points: 
  
    
      
        k
        :
        X
        ×
        X
        →
        
          R
        
      
    
    {\displaystyle k:X\times X\rightarrow \mathbb {R} }
  
. For example, the popular Gaussian kernel:

  
    
      
        k
        (
        x
        ,
        y
        )
        =
        exp
        ⁡
        
          (
          
            −
            
              
                
                  
                    |
                  
                  
                    |
                  
                  x
                  −
                  y
                  
                    |
                  
                  
                    
                      |
                    
                    
                      2
                    
                  
                
                ϵ
              
            
          
          )
        
      
    
    {\displaystyle k(x,y)=\exp \left(-{\frac {||x-y||^{2}}{\epsilon }}\right)}
  

More generally, the kernel function has the following properties

  
    
      
        k
        (
        x
        ,
        y
        )
        =
        k
        (
        y
        ,
        x
        )
      
    
    {\displaystyle k(x,y)=k(y,x)}
  

(
  
    
      
        k
      
    
    {\displaystyle k}
  
 is symmetric)

  
    
      
        k
        (
        x
        ,
        y
        )
        ≥
        0
        
        
        ∀
        x
        ,
        y
      
    
    {\displaystyle k(x,y)\geq 0\,\,\forall x,y}
  

(
  
    
      
        k
      
    
    {\displaystyle k}
  
 is positivity preserving).
The kernel constitutes the prior definition of the local geometry of the data-set. Since a given kernel will capture a specific feature of the data set, its choice should be guided by the application that one has in mind. This is a major difference with methods such as principal component analysis, where correlations between all data points are taken into account at once.
Given 
  
    
      
        (
        X
        ,
        k
        )
      
    
    {\displaystyle (X,k)}
  
, we can then construct a reversible discrete-time Markov chain on 
  
    
      
        X
      
    
    {\displaystyle X}
  
 (a process known as the normalized graph Laplacian construction):

  
    
      
        d
        (
        x
        )
        =
        
          ∫
          
            X
          
        
        k
        (
        x
        ,
        y
        )
        d
        μ
        (
        y
        )
      
    
    {\displaystyle d(x)=\int _{X}k(x,y)d\mu (y)}
  

and define:

  
    
      
        p
        (
        x
        ,
        y
        )
        =
        
          
            
              k
              (
              x
              ,
              y
              )
            
            
              d
              (
              x
              )
            
          
        
      
    
    {\displaystyle p(x,y)={\frac {k(x,y)}{d(x)}}}
  

Although the new normalized kernel does not inherit the symmetric property, it does inherit the positivity-preserving property and gains a conservation property:

  
    
      
        
          ∫
          
            X
          
        
        p
        (
        x
        ,
        y
        )
        d
        μ
        (
        y
        )
        =
        1
      
    
    {\displaystyle \int _{X}p(x,y)d\mu (y)=1}
  


=== Diffusion process ===
From 
  
    
      
        p
        (
        x
        ,
        y
        )
      
    
    {\displaystyle p(x,y)}
  
 we can construct a transition matrix of a Markov chain (
  
    
      
        M
      
    
    {\displaystyle M}
  
) on 
  
    
      
        X
      
    
    {\displaystyle X}
  
. In other words, 
  
    
      
        p
        (
        x
        ,
        y
        )
      
    
    {\displaystyle p(x,y)}
  
 represents the one-step transition probability from 
  
    
      
        x
      
    
    {\displaystyle x}
  
 to 
  
    
      
        y
      
    
    {\displaystyle y}
  
, and 
  
    
      
        
          M
          
            t
          
        
      
    
    {\displaystyle M^{t}}
  
 gives the t-step transition matrix.
We define the diffusion matrix 
  
    
      
        L
      
    
    {\displaystyle L}
  
 (it is also a version of graph Laplacian matrix)

  
    
      
        
          L
          
            i
            ,
            j
          
        
        =
        k
        (
        
          x
          
            i
          
        
        ,
        
          x
          
            j
          
        
        )
        
      
    
    {\displaystyle L_{i,j}=k(x_{i},x_{j})\,}
  

We then define the new kernel

  
    
      
        
          L
          
            i
            ,
            j
          
          
            (
            α
            )
          
        
        =
        
          k
          
            (
            α
            )
          
        
        (
        
          x
          
            i
          
        
        ,
        
          x
          
            j
          
        
        )
        =
        
          
            
              L
              
                i
                ,
                j
              
            
            
              (
              d
              (
              
                x
                
                  i
                
              
              )
              d
              (
              
                x
                
                  j
                
              
              )
              
                )
                
                  α
                
              
            
          
        
        
      
    
    {\displaystyle L_{i,j}^{(\alpha )}=k^{(\alpha )}(x_{i},x_{j})={\frac {L_{i,j}}{(d(x_{i})d(x_{j}))^{\alpha }}}\,}
  

or equivalently,

  
    
      
        
          L
          
            (
            α
            )
          
        
        =
        
          D
          
            −
            α
          
        
        L
        
          D
          
            −
            α
          
        
        
      
    
    {\displaystyle L^{(\alpha )}=D^{-\alpha }LD^{-\alpha }\,}
  

where D is a diagonal matrix and 
  
    
      
        
          D
          
            i
            ,
            i
          
        
        =
        
          ∑
          
            j
          
        
        
          L
          
            i
            ,
            j
          
        
        .
      
    
    {\displaystyle D_{i,i}=\sum _{j}L_{i,j}.}
  

We apply the graph Laplacian normalization to this new kernel:

  
    
      
        M
        =
        (
        
          
            D
          
          
            (
            α
            )
          
        
        
          )
          
            −
            1
          
        
        
          L
          
            (
            α
            )
          
        
        ,
        
      
    
    {\displaystyle M=({D}^{(\alpha )})^{-1}L^{(\alpha )},\,}
  

where 
  
    
      
        
          D
          
            (
            α
            )
          
        
      
    
    {\displaystyle D^{(\alpha )}}
  
 is a diagonal matrix and 
  
    
      
        
          
            D
          
          
            i
            ,
            i
          
          
            (
            α
            )
          
        
        =
        
          ∑
          
            j
          
        
        
          L
          
            i
            ,
            j
          
          
            (
            α
            )
          
        
        .
      
    
    {\displaystyle {D}_{i,i}^{(\alpha )}=\sum _{j}L_{i,j}^{(\alpha )}.}
  

  
    
      
        p
        (
        
          x
          
            j
          
        
        ,
        t
        
          |
        
        
          x
          
            i
          
        
        )
        =
        
          M
          
            i
            ,
            j
          
          
            t
          
        
        
      
    
    {\displaystyle p(x_{j},t|x_{i})=M_{i,j}^{t}\,}
  

One of the main ideas of the diffusion framework is that running the chain forward in time (taking larger and larger powers of 
  
    
      
        M
      
    
    {\displaystyle M}
  
) reveals the geometric structure of 
  
    
      
        X
      
    
    {\displaystyle X}
  
 at larger and larger scales (the diffusion process). Specifically, the notion of a cluster in the data set is quantified as a region in which the probability of escaping this region is low (within a certain time t). Therefore, t not only serves as a time parameter, but it also has the dual role of scale parameter.
The eigendecomposition of the matrix 
  
    
      
        
          M
          
            t
          
        
      
    
    {\displaystyle M^{t}}
  
 yields

  
    
      
        
          M
          
            i
            ,
            j
          
          
            t
          
        
        =
        
          ∑
          
            l
          
        
        
          λ
          
            l
          
          
            t
          
        
        
          ψ
          
            l
          
        
        (
        
          x
          
            i
          
        
        )
        
          ϕ
          
            l
          
        
        (
        
          x
          
            j
          
        
        )
        
      
    
    {\displaystyle M_{i,j}^{t}=\sum _{l}\lambda _{l}^{t}\psi _{l}(x_{i})\phi _{l}(x_{j})\,}
  

where 
  
    
      
        {
        
          λ
          
            l
          
        
        }
      
    
    {\displaystyle \{\lambda _{l}\}}
  
 is the sequence of eigenvalues of 
  
    
      
        M
      
    
    {\displaystyle M}
  
 and 
  
    
      
        {
        
          ψ
          
            l
          
        
        }
      
    
    {\displaystyle \{\psi _{l}\}}
  
 and 
  
    
      
        {
        
          ϕ
          
            l
          
        
        }
      
    
    {\displaystyle \{\phi _{l}\}}
  
 are the biorthogonal left and right eigenvectors respectively.
Due to the spectrum decay of the eigenvalues, only a few terms are necessary to achieve a given relative accuracy in this sum.


==== Parameter α and the diffusion operator ====
The reason to introduce the normalization step involving 
  
    
      
        α
      
    
    {\displaystyle \alpha }
  
 is to tune the influence of the data point density on the infinitesimal transition of the diffusion. In some applications, the sampling of the data is generally not related to the geometry of the manifold we are interested in describing. In this case, we can set 
  
    
      
        α
        =
        1
      
    
    {\displaystyle \alpha =1}
  
 and the diffusion operator approximates the Laplace–Beltrami operator. We then recover the Riemannian geometry of the data set regardless of the distribution of the points. To describe the long-term behavior of the point distribution of a system of stochastic differential equations, we can use 
  
    
      
        α
        =
        0.5
      
    
    {\displaystyle \alpha =0.5}
  
 and the resulting Markov chain approximates the Fokker–Planck diffusion. With 
  
    
      
        α
        =
        0
      
    
    {\displaystyle \alpha =0}
  
, it reduces to the classical graph Laplacian normalization.


=== Diffusion distance ===
The diffusion distance at time 
  
    
      
        t
      
    
    {\displaystyle t}
  
 between two points can be measured as the similarity of two points in the observation space with the connectivity between them. It is given by

  
    
      
        
          D
          
            t
          
        
        (
        
          x
          
            i
          
        
        ,
        
          x
          
            j
          
        
        
          )
          
            2
          
        
        =
        
          ∑
          
            y
          
        
        
          
            
              (
              p
              (
              y
              ,
              t
              
                |
              
              
                x
                
                  i
                
              
              )
              −
              p
              (
              y
              ,
              t
              
                |
              
              
                x
                
                  j
                
              
              )
              
                )
                
                  2
                
              
            
            
              
                ϕ
                
                  0
                
              
              (
              y
              )
            
          
        
      
    
    {\displaystyle D_{t}(x_{i},x_{j})^{2}=\sum _{y}{\frac {(p(y,t|x_{i})-p(y,t|x_{j}))^{2}}{\phi _{0}(y)}}}
  

where 
  
    
      
        
          ϕ
          
            0
          
        
        (
        y
        )
      
    
    {\displaystyle \phi _{0}(y)}
  
 is the stationary distribution of the Markov chain, given by the first left eigenvector of 
  
    
      
        M
      
    
    {\displaystyle M}
  
. Explicitly:

  
    
      
        
          ϕ
          
            0
          
        
        (
        y
        )
        =
        
          
            
              d
              (
              y
              )
            
            
              
                ∑
                
                  z
                  ∈
                  X
                
              
              d
              (
              z
              )
            
          
        
      
    
    {\displaystyle \phi _{0}(y)={\frac {d(y)}{\sum _{z\in X}d(z)}}}
  

Intuitively, 
  
    
      
        
          D
          
            t
          
        
        (
        
          x
          
            i
          
        
        ,
        
          x
          
            j
          
        
        )
      
    
    {\displaystyle D_{t}(x_{i},x_{j})}
  
 is small if there is a large number of short paths connecting 
  
    
      
        
          x
          
            i
          
        
      
    
    {\displaystyle x_{i}}
  
 and 
  
    
      
        
          x
          
            j
          
        
      
    
    {\displaystyle x_{j}}
  
. There are several interesting features associated with the diffusion distance, based on our previous discussion that 
  
    
      
        t
      
    
    {\displaystyle t}
  
 also serves as a scale parameter:

Points are closer at a given scale (as specified by 
  
    
      
        
          D
          
            t
          
        
        (
        
          x
          
            i
          
        
        ,
        
          x
          
            j
          
        
        )
      
    
    {\displaystyle D_{t}(x_{i},x_{j})}
  
) if they are highly connected in the graph, therefore emphasizing the concept of a cluster.
This distance is robust to noise, since the distance between two points depends on all possible paths of length 
  
    
      
        t
      
    
    {\displaystyle t}
  
 between the points.
From a machine learning point of view, the distance takes into account all evidences linking 
  
    
      
        
          x
          
            i
          
        
      
    
    {\displaystyle x_{i}}
  
 to 
  
    
      
        
          x
          
            j
          
        
      
    
    {\displaystyle x_{j}}
  
, allowing us to conclude that this distance is appropriate for the design of inference algorithms based on the majority of preponderance.


=== Diffusion process and low-dimensional embedding ===
The diffusion distance can be calculated using the eigenvectors by

  
    
      
        
          D
          
            t
          
        
        (
        
          x
          
            i
          
        
        ,
        
          x
          
            j
          
        
        
          )
          
            2
          
        
        =
        
          ∑
          
            l
          
        
        
          λ
          
            l
          
          
            2
            t
          
        
        (
        
          ψ
          
            l
          
        
        (
        
          x
          
            i
          
        
        )
        −
        
          ψ
          
            l
          
        
        (
        
          x
          
            j
          
        
        )
        
          )
          
            2
          
        
        
      
    
    {\displaystyle D_{t}(x_{i},x_{j})^{2}=\sum _{l}\lambda _{l}^{2t}(\psi _{l}(x_{i})-\psi _{l}(x_{j}))^{2}\,}
  

So the eigenvectors can be used as a new set of coordinates for the data. The diffusion map is defined as:

  
    
      
        
          Ψ
          
            t
          
        
        (
        x
        )
        =
        (
        
          λ
          
            1
          
          
            t
          
        
        
          ψ
          
            1
          
        
        (
        x
        )
        ,
        
          λ
          
            2
          
          
            t
          
        
        
          ψ
          
            2
          
        
        (
        x
        )
        ,
        …
        ,
        
          λ
          
            k
          
          
            t
          
        
        
          ψ
          
            k
          
        
        (
        x
        )
        )
      
    
    {\displaystyle \Psi _{t}(x)=(\lambda _{1}^{t}\psi _{1}(x),\lambda _{2}^{t}\psi _{2}(x),\ldots ,\lambda _{k}^{t}\psi _{k}(x))}
  

Because of the spectrum decay, it is sufficient to use only the first k eigenvectors and eigenvalues.
Thus we get the diffusion map from the original data to a k-dimensional space which is embedded in the original space.
In  it is proved that

  
    
      
        
          D
          
            t
          
        
        (
        
          x
          
            i
          
        
        ,
        
          x
          
            j
          
        
        
          )
          
            2
          
        
        ≈
        
          |
        
        
          |
        
        
          Ψ
          
            t
          
        
        (
        
          x
          
            i
          
        
        )
        −
        
          Ψ
          
            t
          
        
        (
        
          x
          
            j
          
        
        )
        
          |
        
        
          
            |
          
          
            2
          
        
        
      
    
    {\displaystyle D_{t}(x_{i},x_{j})^{2}\approx ||\Psi _{t}(x_{i})-\Psi _{t}(x_{j})||^{2}\,}
  

so the Euclidean distance in the diffusion coordinates approximates the diffusion distance.


== Algorithm ==
The basic algorithm framework of diffusion map is as:
Step 1. Given the similarity matrix L.
Step 2. Normalize the matrix according to parameter 
  
    
      
        α
      
    
    {\displaystyle \alpha }
  
: 
  
    
      
        
          L
          
            (
            α
            )
          
        
        =
        
          D
          
            −
            α
          
        
        L
        
          D
          
            −
            α
          
        
      
    
    {\displaystyle L^{(\alpha )}=D^{-\alpha }LD^{-\alpha }}
  
.
Step 3. Form the normalized matrix 
  
    
      
        M
        =
        (
        
          
            D
          
          
            (
            α
            )
          
        
        
          )
          
            −
            1
          
        
        
          L
          
            (
            α
            )
          
        
      
    
    {\displaystyle M=({D}^{(\alpha )})^{-1}L^{(\alpha )}}
  
.
Step 4. Compute the k largest eigenvalues of 
  
    
      
        
          M
          
            t
          
        
      
    
    {\displaystyle M^{t}}
  
 and the corresponding eigenvectors.
Step 5. Use diffusion map to get the embedding 
  
    
      
        
          Ψ
          
            t
          
        
      
    
    {\displaystyle \Psi _{t}}
  
.


== Application ==
In the paper  Nadler et al. showed how to design a kernel that reproduces the diffusion induced by a Fokker–Planck equation. They also explained that, when the data approximate a manifold, one can recover the geometry of this manifold by computing an approximation of the Laplace–Beltrami operator. This computation is completely insensitive
to the distribution of the points and therefore provides a separation of the statistics and the geometry of the
data. Since diffusion maps give a global description of the data-set, they can measure the distances between pairs of sample points in the manifold in which the data is embedded. Applications based on diffusion maps include face recognition, spectral clustering, low dimensional representation of images, image segmentation, 3D model segmentation, speaker verification and identification, sampling on manifolds, anomaly detection, image inpainting, revealing brain resting state networks organization   and so on.
Furthermore, the diffusion maps framework has been productively extended to complex networks, revealing a functional organisation of networks which differs from the purely topological or structural one.


== Vector and Tensor Diffusion Maps ==
The basic idea of diffusion maps can be extended to vectors and higher order tensors by augmenting the data manifold with an affine connection. This describes the way that vectors and other tensors transform when moving locally from one point on the manifold to a point nearby. In the case of a discrete data graph approximating a continuous manifold, this amounts to assigning a local subspace to every data point and an orthonormal matrix mapping between subspaces to every edge on the graph. This object is known as a cellular sheaf. The subspaces can be found by applying principal component analysis locally around each point, while the edge mappings can be found by applying canonical correlation analysis between the local subspaces. Then, an extension of the graph Laplacian that describes the time evolution of vectors undergoing a random walk can be defined: the graph connection Laplacian:

  
    
      
        
          L
          
            i
            j
          
        
        =
        
          
            
              O
            
          
          
            i
            j
          
        
      
    
    {\displaystyle L_{ij}={\mathcal {O}}_{ij}}
  

  
    
      
        
          L
          
            i
            i
          
        
        =
        d
        
          I
        
      
    
    {\displaystyle L_{ii}=d\mathbf {I} }
  

where 
  
    
      
        d
      
    
    {\displaystyle d}
  
 is the degree of the node 
  
    
      
        i
      
    
    {\displaystyle i}
  
 in the graph and 
  
    
      
        
          
            
              O
            
          
          
            i
            j
          
        
      
    
    {\displaystyle {\mathcal {O}}_{ij}}
  
 is the orthonormal connection between neighboring nodes. This is a block-sparse matrix, with one block 
  
    
      
        
          L
          
            i
            j
          
        
      
    
    {\displaystyle L_{ij}}
  
 for each edge of the graph.
The equivalent embedding found by applying diffusion maps to this connection Laplacian is known as the vector diffusion map.
The connection Laplacian can also be defined for higher-order tensors, in which case each block of the matrix will be a Kronecker product of the connection matrices. The second order graph connection Laplacian encodes information about how matrices and subspaces evolve under random walk diffusion. This has a close connection to holonomy theory and the de Rham decomposition. The eigenvectors of the second-order connection Laplacian can be used to decompose the data manifold into submanifolds, rather than finding an embedding. This is the central idea behind the Geometric Manifold Component Estimator (GeoManCEr).


== See also ==
Nonlinear dimensionality reduction
Spectral clustering


== References ==