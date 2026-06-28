# Kernel principal component analysis

Source: Wikipedia (https://en.wikipedia.org/wiki/Kernel_principal_component_analysis)

In the field of multivariate statistics, kernel principal component analysis (kernel PCA)
is an extension of principal component analysis (PCA) using techniques of kernel methods. Using a kernel, the originally linear operations of PCA are performed in a reproducing kernel Hilbert space.


== Background: Linear PCA ==
Recall that conventional PCA operates on zero-centered data; that is, 

  
    
      
        
          
            1
            N
          
        
        
          ∑
          
            i
            =
            1
          
          
            N
          
        
        
          
            x
          
          
            i
          
        
        =
        
          0
        
      
    
    {\displaystyle {\frac {1}{N}}\sum _{i=1}^{N}\mathbf {x} _{i}=\mathbf {0} }
  
,
where 
  
    
      
        
          
            x
          
          
            i
          
        
      
    
    {\displaystyle \mathbf {x} _{i}}
  
 is one of the 
  
    
      
        N
      
    
    {\displaystyle N}
  
 multivariate observations.
It operates by diagonalizing the covariance matrix,

  
    
      
        C
        =
        
          
            1
            N
          
        
        
          ∑
          
            i
            =
            1
          
          
            N
          
        
        
          
            x
          
          
            i
          
        
        
          
            x
          
          
            i
          
          
            ⊤
          
        
      
    
    {\displaystyle C={\frac {1}{N}}\sum _{i=1}^{N}\mathbf {x} _{i}\mathbf {x} _{i}^{\top }}
  

in other words, it gives an eigendecomposition of the covariance matrix:

  
    
      
        λ
        
          v
        
        =
        C
        
          v
        
      
    
    {\displaystyle \lambda \mathbf {v} =C\mathbf {v} }
  

which can be rewritten as

  
    
      
        λ
        
          
            x
          
          
            i
          
          
            ⊤
          
        
        
          v
        
        =
        
          
            x
          
          
            i
          
          
            ⊤
          
        
        C
        
          v
        
        
        
          
            for
          
        
         
        i
        =
        1
        ,
        …
        ,
        N
      
    
    {\displaystyle \lambda \mathbf {x} _{i}^{\top }\mathbf {v} =\mathbf {x} _{i}^{\top }C\mathbf {v} \quad {\textrm {for}}~i=1,\ldots ,N}
  
.
(See also: Covariance matrix as a linear operator)


== Introduction of the Kernel to PCA ==
To understand the utility of kernel PCA, particularly for clustering, observe that, while N points cannot, in general, be linearly separated in 
  
    
      
        d
        <
        N
      
    
    {\displaystyle d<N}
  
 dimensions, they can almost always be linearly separated in 
  
    
      
        d
        ≥
        N
      
    
    {\displaystyle d\geq N}
  
 dimensions. That is, given N points, 
  
    
      
        
          
            x
          
          
            i
          
        
      
    
    {\displaystyle \mathbf {x} _{i}}
  
, if we map them to an N-dimensional space with

  
    
      
        Φ
        (
        
          
            x
          
          
            i
          
        
        )
      
    
    {\displaystyle \Phi (\mathbf {x} _{i})}
  
 where 
  
    
      
        Φ
        :
        
          
            R
          
          
            d
          
        
        →
        
          
            R
          
          
            N
          
        
      
    
    {\displaystyle \Phi :\mathbb {R} ^{d}\to \mathbb {R} ^{N}}
  
,
it is easy to construct a hyperplane that divides the points into arbitrary clusters. Of course, this 
  
    
      
        Φ
      
    
    {\displaystyle \Phi }
  
 creates linearly independent vectors, so there is no covariance on which to perform eigendecomposition explicitly as we would in linear PCA.
Instead, in kernel PCA, a non-trivial, arbitrary 
  
    
      
        Φ
      
    
    {\displaystyle \Phi }
  
 function is 'chosen' that is never calculated explicitly, allowing the possibility to use very-high-dimensional 
  
    
      
        Φ
      
    
    {\displaystyle \Phi }
  
's if we never have to actually evaluate the data in that space. Since we generally try to avoid working in the 
  
    
      
        Φ
      
    
    {\displaystyle \Phi }
  
-space, which we will call the 'feature space', we can create the N-by-N kernel

  
    
      
        K
        =
        k
        (
        
          x
        
        ,
        
          y
        
        )
        =
        (
        Φ
        (
        
          x
        
        )
        ,
        Φ
        (
        
          y
        
        )
        )
        =
        Φ
        (
        
          x
        
        
          )
          
            T
          
        
        Φ
        (
        
          y
        
        )
      
    
    {\displaystyle K=k(\mathbf {x} ,\mathbf {y} )=(\Phi (\mathbf {x} ),\Phi (\mathbf {y} ))=\Phi (\mathbf {x} )^{T}\Phi (\mathbf {y} )}
  

which represents the inner product space (see Gramian matrix) of the otherwise intractable feature space. The dual form that arises in the creation of a kernel allows us to mathematically formulate a version of PCA in which we never actually solve the eigenvectors and eigenvalues of the covariance matrix in the 
  
    
      
        Φ
        (
        
          x
        
        )
      
    
    {\displaystyle \Phi (\mathbf {x} )}
  
-space (see Kernel trick).  The N-elements in each column of K represent the dot product of one point of the transformed data with respect to all the transformed points (N points). Some well-known kernels are shown in the example below.
Because we are never working directly in the feature space, the kernel-formulation of PCA is restricted in that it computes not the principal components themselves, but the projections of our data onto those components. To evaluate the projection from a point in the feature space 
  
    
      
        Φ
        (
        
          x
        
        )
      
    
    {\displaystyle \Phi (\mathbf {x} )}
  
 onto the kth principal component 
  
    
      
        
          V
          
            k
          
        
      
    
    {\displaystyle V^{k}}
  
 (where superscript k means the component k, not powers of k)

  
    
      
        
          
            
              V
              
                k
              
            
          
          
            T
          
        
        Φ
        (
        
          x
        
        )
        =
        
          
            (
            
              
                ∑
                
                  i
                  =
                  1
                
                
                  N
                
              
              
                
                  a
                
                
                  i
                
                
                  k
                
              
              Φ
              (
              
                
                  x
                
                
                  i
                
              
              )
            
            )
          
          
            T
          
        
        Φ
        (
        
          x
        
        )
      
    
    {\displaystyle {V^{k}}^{T}\Phi (\mathbf {x} )=\left(\sum _{i=1}^{N}\mathbf {a} _{i}^{k}\Phi (\mathbf {x} _{i})\right)^{T}\Phi (\mathbf {x} )}
  

We note that 
  
    
      
        Φ
        (
        
          
            x
          
          
            i
          
        
        
          )
          
            T
          
        
        Φ
        (
        
          x
        
        )
      
    
    {\displaystyle \Phi (\mathbf {x} _{i})^{T}\Phi (\mathbf {x} )}
  
 denotes dot product, which is simply the elements of the kernel 
  
    
      
        K
      
    
    {\displaystyle K}
  
. It seems all that's left is to calculate and normalize the  
  
    
      
        
          
            a
          
          
            i
          
          
            k
          
        
      
    
    {\displaystyle \mathbf {a} _{i}^{k}}
  
, which can be done by solving the eigenvector equation

  
    
      
        N
        λ
        
          a
        
        =
        K
        
          a
        
      
    
    {\displaystyle N\lambda \mathbf {a} =K\mathbf {a} }
  

where 
  
    
      
        N
      
    
    {\displaystyle N}
  
 is the number of data points in the set, and 
  
    
      
        λ
      
    
    {\displaystyle \lambda }
  
 and 
  
    
      
        
          a
        
      
    
    {\displaystyle \mathbf {a} }
  
 are the eigenvalues and eigenvectors of 
  
    
      
        K
      
    
    {\displaystyle K}
  
. Then to normalize the eigenvectors 
  
    
      
        
          
            a
          
          
            k
          
        
      
    
    {\displaystyle \mathbf {a} ^{k}}
  
, we require that

  
    
      
        1
        =
        (
        
          V
          
            k
          
        
        
          )
          
            T
          
        
        
          V
          
            k
          
        
      
    
    {\displaystyle 1=(V^{k})^{T}V^{k}}
  

Care must be taken regarding the fact that, whether or not 
  
    
      
        x
      
    
    {\displaystyle x}
  
 has zero-mean in its original space, it is not guaranteed to be centered in the feature space (which we never compute explicitly). Since centered data is required to perform an effective principal component analysis, we 'centralize' 
  
    
      
        K
      
    
    {\displaystyle K}
  
 to become 
  
    
      
        
          K
          ′
        
      
    
    {\displaystyle K'}
  

  
    
      
        
          K
          ′
        
        =
        K
        −
        
          
            1
            
              N
            
          
        
        K
        −
        K
        
          
            1
            
              N
            
          
        
        +
        
          
            1
            
              N
            
          
        
        K
        
          
            1
            
              N
            
          
        
      
    
    {\displaystyle K'=K-\mathbf {1_{N}} K-K\mathbf {1_{N}} +\mathbf {1_{N}} K\mathbf {1_{N}} }
  

where  
  
    
      
        
          
            1
            
              N
            
          
        
      
    
    {\displaystyle \mathbf {1_{N}} }
  
 denotes a N-by-N matrix for which each element takes value 
  
    
      
        1
        
          /
        
        N
      
    
    {\displaystyle 1/N}
  
. We use 
  
    
      
        
          K
          ′
        
      
    
    {\displaystyle K'}
  
 to perform the kernel PCA algorithm described above.
One caveat of kernel PCA should be illustrated here. In linear PCA, we can use the eigenvalues to rank the eigenvectors based on how much of the variation of the data is captured by each principal component. This is useful for data dimensionality reduction and it could also be applied to KPCA. However, in practice there are cases that all variations of the data are same. This is typically caused by a wrong choice of kernel scale.


== Large datasets ==
In practice, a large data set leads to a large K, and storing K may become a problem. One way to deal with this is to perform clustering on the dataset, and populate the kernel with the means of those clusters. Since even this method may yield a relatively large K, it is common to compute only the top P eigenvalues and eigenvectors of the eigenvalues are calculated in this way.


== Example ==

Consider three concentric clouds of points (shown); we wish to use kernel PCA to identify these groups. The color of the points does not represent information involved in the algorithm, but only shows how the transformation relocates the data points.
First, consider the kernel

  
    
      
        k
        (
        
          x
        
        ,
        
          y
        
        )
        =
        (
        
          
            x
          
          
            
              T
            
          
        
        
          y
        
        +
        1
        
          )
          
            2
          
        
      
    
    {\displaystyle k({\boldsymbol {x}},{\boldsymbol {y}})=({\boldsymbol {x}}^{\mathrm {T} }{\boldsymbol {y}}+1)^{2}}
  

Applying this to kernel PCA yields the next image.

Now consider a Gaussian kernel:

  
    
      
        k
        (
        
          x
        
        ,
        
          y
        
        )
        =
        
          e
          
            
              
                −
                
                  |
                
                
                  |
                
                
                  x
                
                −
                
                  y
                
                
                  |
                
                
                  
                    |
                  
                  
                    2
                  
                
              
              
                2
                
                  σ
                  
                    2
                  
                
              
            
          
        
        ,
      
    
    {\displaystyle k({\boldsymbol {x}},{\boldsymbol {y}})=e^{\frac {-||{\boldsymbol {x}}-{\boldsymbol {y}}||^{2}}{2\sigma ^{2}}},}
  

That is, this kernel is a measure of closeness, equal to 1 when the points coincide and equal to 0 at infinity.

Note in particular that the first principal component is enough to distinguish the three different groups, which is impossible using only linear PCA, because linear PCA operates only in the given (in this case two-dimensional) space, in which these concentric point clouds are not linearly separable.


== Applications ==
Kernel PCA has been demonstrated to be useful for novelty detection and image de-noising.


== See also ==
Cluster analysis
Nonlinear dimensionality reduction
Spectral clustering


== References ==