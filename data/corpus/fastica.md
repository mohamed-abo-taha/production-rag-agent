# FastICA

Source: Wikipedia (https://en.wikipedia.org/wiki/FastICA)

FastICA is an efficient and popular algorithm for independent component analysis invented by Aapo Hyvärinen at Helsinki University of Technology. Like most ICA algorithms, FastICA seeks an orthogonal rotation of prewhitened data, through a fixed-point iteration scheme, that maximizes a measure of non-Gaussianity of the rotated components. Non-gaussianity serves as a proxy for statistical independence, which is a very strong condition and requires infinite data to verify. FastICA can also be alternatively derived as an approximative Newton iteration.


== Algorithm ==


=== Prewhitening the data ===
Let the 
  
    
      
        
          X
        
        :=
        (
        
          x
          
            i
            j
          
        
        )
        ∈
        
          
            R
          
          
            N
            ×
            M
          
        
      
    
    {\displaystyle \mathbf {X} :=(x_{ij})\in \mathbb {R} ^{N\times M}}
  
 denote the input data matrix, 
  
    
      
        M
      
    
    {\displaystyle M}
  
 the number of columns corresponding with the number of samples of mixed signals and 
  
    
      
        N
      
    
    {\displaystyle N}
  
 the number of rows corresponding with the number of independent source signals. The input data matrix 
  
    
      
        
          X
        
      
    
    {\displaystyle \mathbf {X} }
  
 must be prewhitened, or centered and whitened, before applying the FastICA algorithm to it.

Centering the data entails demeaning each component of the input data 
  
    
      
        
          X
        
      
    
    {\displaystyle \mathbf {X} }
  
, that is,

for each 
  
    
      
        i
        =
        1
        ,
        …
        ,
        N
      
    
    {\displaystyle i=1,\ldots ,N}
  
 and 
  
    
      
        j
        =
        1
        ,
        …
        ,
        M
      
    
    {\displaystyle j=1,\ldots ,M}
  
. After centering, each row of 
  
    
      
        
          X
        
      
    
    {\displaystyle \mathbf {X} }
  
 has an expected value of 
  
    
      
        0
      
    
    {\displaystyle 0}
  
.
Whitening the data requires a linear transformation  
  
    
      
        
          L
        
        :
        
          
            R
          
          
            N
            ×
            M
          
        
        →
        
          
            R
          
          
            N
            ×
            M
          
        
      
    
    {\displaystyle \mathbf {L} :\mathbb {R} ^{N\times M}\to \mathbb {R} ^{N\times M}}
  
 of the centered data so that the components of 
  
    
      
        
          L
        
        (
        
          X
        
        )
      
    
    {\displaystyle \mathbf {L} (\mathbf {X} )}
  
 are uncorrelated and have variance one. More precisely, if 
  
    
      
        
          X
        
      
    
    {\displaystyle \mathbf {X} }
  
 is a centered data matrix, the covariance of 
  
    
      
        
          
            L
          
          
            
              x
            
          
        
        :=
        
          L
        
        (
        
          X
        
        )
      
    
    {\displaystyle \mathbf {L} _{\mathbf {x} }:=\mathbf {L} (\mathbf {X} )}
  
 is the 
  
    
      
        (
        N
        ×
        N
        )
      
    
    {\displaystyle (N\times N)}
  
-dimensional identity matrix, that is,

A common method for whitening is by performing an eigenvalue decomposition on the covariance matrix of the centered data 
  
    
      
        
          X
        
      
    
    {\displaystyle \mathbf {X} }
  
, 
  
    
      
        E
        
          {
          
            
              X
            
            
              
                X
              
              
                T
              
            
          
          }
        
        =
        
          E
        
        
          D
        
        
          
            E
          
          
            T
          
        
      
    
    {\displaystyle E\left\{\mathbf {X} \mathbf {X} ^{T}\right\}=\mathbf {E} \mathbf {D} \mathbf {E} ^{T}}
  
, where 
  
    
      
        
          E
        
      
    
    {\displaystyle \mathbf {E} }
  
 is the matrix of eigenvectors and 
  
    
      
        
          D
        
      
    
    {\displaystyle \mathbf {D} }
  
 is the diagonal matrix of eigenvalues. The whitened data matrix is defined thus by


=== Single component extraction ===
The iterative algorithm finds the direction for the weight vector 
  
    
      
        
          w
        
        ∈
        
          
            R
          
          
            N
          
        
      
    
    {\displaystyle \mathbf {w} \in \mathbb {R} ^{N}}
  

that maximizes a measure of non-Gaussianity of the projection 
  
    
      
        
          
            w
          
          
            T
          
        
        
          X
        
      
    
    {\displaystyle \mathbf {w} ^{T}\mathbf {X} }
  
, 
with 
  
    
      
        
          X
        
        ∈
        
          
            R
          
          
            N
            ×
            M
          
        
      
    
    {\displaystyle \mathbf {X} \in \mathbb {R} ^{N\times M}}
  
 denoting a prewhitened data matrix as described above.
Note that 
  
    
      
        
          w
        
      
    
    {\displaystyle \mathbf {w} }
  
 is a column vector. To measure non-Gaussianity, FastICA relies on a nonquadratic nonlinear function 
  
    
      
        f
        (
        u
        )
      
    
    {\displaystyle f(u)}
  
, its first derivative 
  
    
      
        g
        (
        u
        )
      
    
    {\displaystyle g(u)}
  
, and its second derivative 
  
    
      
        
          g
          
            ′
          
        
        (
        u
        )
      
    
    {\displaystyle g^{\prime }(u)}
  
. Hyvärinen states that the functions 

are useful for general purposes, while 

 
may be highly robust. The steps for extracting the weight vector 
  
    
      
        
          w
        
      
    
    {\displaystyle \mathbf {w} }
  
 for single component in FastICA are the following: 

Randomize the initial weight vector 
  
    
      
        
          w
        
      
    
    {\displaystyle \mathbf {w} }
  

Let 
  
    
      
        
          
            w
          
          
            +
          
        
        ←
        E
        
          {
          
            
              X
            
            g
            (
            
              
                w
              
              
                T
              
            
            
              X
            
            
              )
              
                T
              
            
          
          }
        
        −
        E
        
          {
          
            
              g
              ′
            
            (
            
              
                w
              
              
                T
              
            
            
              X
            
            )
          
          }
        
        
          w
        
      
    
    {\displaystyle \mathbf {w} ^{+}\leftarrow E\left\{\mathbf {X} g(\mathbf {w} ^{T}\mathbf {X} )^{T}\right\}-E\left\{g'(\mathbf {w} ^{T}\mathbf {X} )\right\}\mathbf {w} }
  
, where 
  
    
      
        E
        
          {
          
            .
            .
            .
          
          }
        
      
    
    {\displaystyle E\left\{...\right\}}
  
 means averaging over all column-vectors of matrix 
  
    
      
        
          X
        
      
    
    {\displaystyle \mathbf {X} }
  

Let 
  
    
      
        
          w
        
        ←
        
          
            w
          
          
            +
          
        
        
          /
        
        ‖
        
          
            w
          
          
            +
          
        
        ‖
      
    
    {\displaystyle \mathbf {w} \leftarrow \mathbf {w} ^{+}/\|\mathbf {w} ^{+}\|}
  

If not converged, go back to 2


=== Multiple component extraction ===
The single unit iterative algorithm estimates only one weight vector which extracts a single component. Estimating additional components that are mutually "independent" requires repeating the algorithm to obtain linearly independent projection vectors - note that the notion of  independence here refers to maximizing non-Gaussianity in the estimated components. Hyvärinen provides several ways of extracting multiple components with the simplest being the following. Here, 
  
    
      
        
          
            1
            
              M
            
          
        
      
    
    {\displaystyle \mathbf {1_{M}} }
  
 is a column vector of 1's of dimension 
  
    
      
        M
      
    
    {\displaystyle M}
  
.
Algorithm FastICA

Input: 
  
    
      
        C
      
    
    {\displaystyle C}
  
 Number of desired components
Input: 
  
    
      
        
          X
        
        ∈
        
          
            R
          
          
            N
            ×
            M
          
        
      
    
    {\displaystyle \mathbf {X} \in \mathbb {R} ^{N\times M}}
  
 Prewhitened matrix, where each column represents an 
  
    
      
        N
      
    
    {\displaystyle N}
  
-dimensional sample, where 
  
    
      
        C
        <=
        N
      
    
    {\displaystyle C<=N}
  

Output: 
  
    
      
        
          W
        
        ∈
        
          
            R
          
          
            N
            ×
            C
          
        
      
    
    {\displaystyle \mathbf {W} \in \mathbb {R} ^{N\times C}}
  
 Un-mixing matrix where each column projects 
  
    
      
        
          X
        
      
    
    {\displaystyle \mathbf {X} }
  
 onto independent component.
Output: 
  
    
      
        
          S
        
        ∈
        
          
            R
          
          
            C
            ×
            M
          
        
      
    
    {\displaystyle \mathbf {S} \in \mathbb {R} ^{C\times M}}
  
 Independent components matrix, with 
  
    
      
        M
      
    
    {\displaystyle M}
  
 columns representing a sample with 
  
    
      
        C
      
    
    {\displaystyle C}
  
  dimensions.
 for p in 1 to C:
    
  
    
      
        
          
            w
            
              p
            
          
        
        ←
      
    
    {\displaystyle \mathbf {w_{p}} \leftarrow }
  
 Random vector of length N
    while 
  
    
      
        
          
            w
            
              p
            
          
        
      
    
    {\displaystyle \mathbf {w_{p}} }
  
 changes
        
  
    
      
        
          
            w
            
              p
            
          
        
        ←
        
          
            1
            M
          
        
        
          X
        
        g
        (
        
          
            
              w
              
                p
              
            
          
          
            T
          
        
        
          X
        
        
          )
          
            T
          
        
        −
        
          
            1
            M
          
        
        
          g
          ′
        
        (
        
          
            
              w
              
                p
              
            
          
          
            T
          
        
        
          X
        
        )
        
          
            1
            
              M
            
          
        
        
          
            w
            
              p
            
          
        
      
    
    {\displaystyle \mathbf {w_{p}} \leftarrow {\frac {1}{M}}\mathbf {X} g(\mathbf {w_{p}} ^{T}\mathbf {X} )^{T}-{\frac {1}{M}}g'(\mathbf {w_{p}} ^{T}\mathbf {X} )\mathbf {1_{M}} \mathbf {w_{p}} }
  

        
  
    
      
        
          
            w
            
              p
            
          
        
        ←
        
          
            w
            
              p
            
          
        
        −
        
          ∑
          
            j
            =
            1
          
          
            p
            −
            1
          
        
        (
        
          
            
              w
              
                p
              
            
          
          
            T
          
        
        
          
            w
            
              j
            
          
        
        )
        
          
            w
            
              j
            
          
        
      
    
    {\displaystyle \mathbf {w_{p}} \leftarrow \mathbf {w_{p}} -\sum _{j=1}^{p-1}(\mathbf {w_{p}} ^{T}\mathbf {w_{j}} )\mathbf {w_{j}} }
  

        
  
    
      
        
          
            w
            
              p
            
          
        
        ←
        
          
            
              
                w
                
                  p
                
              
            
            
              ‖
              
                
                  w
                  
                    p
                  
                
              
              ‖
            
          
        
      
    
    {\displaystyle \mathbf {w_{p}} \leftarrow {\frac {\mathbf {w_{p}} }{\|\mathbf {w_{p}} \|}}}
  

 output 
  
    
      
        
          W
        
        ←
        
          
            [
            
              
                
                  
                    
                      w
                      
                        1
                      
                    
                  
                  ,
                  …
                  ,
                  
                    
                      w
                      
                        C
                      
                    
                  
                
              
            
            ]
          
        
      
    
    {\displaystyle \mathbf {W} \leftarrow {\begin{bmatrix}\mathbf {w_{1}} ,\dots ,\mathbf {w_{C}} \end{bmatrix}}}
  

 output 
  
    
      
        
          S
        
        ←
        
          
            W
            
              T
            
          
        
        
          X
        
      
    
    {\displaystyle \mathbf {S} \leftarrow \mathbf {W^{T}} \mathbf {X} }
  


== See also ==
Unsupervised learning
Machine learning
The IT++ library features a FastICA implementation in C++
Infomax


== References ==


== External links ==
FastICA in Python
FastICA package for Matlab or Octave
fastICA package in R programming language
FastICA in Java on SourceForge
FastICA in Java in RapidMiner.
FastICA in Matlab
FastICA in MDP
FastICA in Julia