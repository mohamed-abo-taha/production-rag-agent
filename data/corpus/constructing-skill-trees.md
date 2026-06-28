# Constructing skill trees

Source: Wikipedia (https://en.wikipedia.org/wiki/Constructing_skill_trees)

Constructing skill trees (CST) is a hierarchical reinforcement learning algorithm which can build  skill trees from a set of sample solution trajectories obtained from demonstration.  CST uses an incremental MAP (maximum a posteriori) change point detection algorithm to segment each demonstration trajectory into skills and integrate the results into a skill tree.  CST was introduced by George Konidaris, Scott Kuindersma, Andrew Barto and Roderic Grupen in 2010.


== Algorithm ==
CST consists of mainly three parts;change point detection, alignment and merging. The main focus of CST is online change-point detection. The change-point detection algorithm is used to segment data into skills and uses the sum of discounted reward 
  
    
      
        
          R
          
            t
          
        
      
    
    {\displaystyle R_{t}}
  
 as the target regression variable. Each skill is assigned an appropriate abstraction. A particle filter is used to control the computational complexity of CST.
The change point detection algorithm is implemented as follows. The data for times 
  
    
      
        t
        ∈
        T
      
    
    {\displaystyle t\in T}
  
 and models Q with prior 
  
    
      
        p
        (
        q
        ∈
        Q
        )
      
    
    {\displaystyle p(q\in Q)}
  
 are given.  The algorithm is assumed to be able to fit a segment from time 
  
    
      
        j
        +
        1
      
    
    {\displaystyle j+1}
  
 to t using model q with the fit probability 
  
    
      
        P
        (
        j
        ,
        t
        ,
        q
        
          )
          

          
          

          
        
      
    
    {\displaystyle P(j,t,q)_{}^{}}
  
.  A linear regression model with Gaussian noise is used to compute 
  
    
      
        P
        (
        j
        ,
        t
        ,
        q
        )
      
    
    {\displaystyle P(j,t,q)}
  
. The Gaussian noise prior has mean zero, and variance which follows 
  
    
      
        
          I
          n
          v
          e
          r
          s
          e
          G
          a
          m
          m
          a
        
        
          (
          
            
              
                v
                2
              
            
            ,
            
              
                u
                2
              
            
          
          )
        
      
    
    {\displaystyle \mathrm {InverseGamma} \left({\frac {v}{2}},{\frac {u}{2}}\right)}
  
. The prior for each weight follows 
  
    
      
        
          N
          o
          r
          m
          a
          l
        
        (
        0
        ,
        
          σ
          
            2
          
        
        δ
        )
      
    
    {\displaystyle \mathrm {Normal} (0,\sigma ^{2}\delta )}
  
.
The fit probability 
  
    
      
        P
        (
        j
        ,
        t
        ,
        q
        )
      
    
    {\displaystyle P(j,t,q)}
  
 is computed by the following equation.

  
    
      
        P
        (
        j
        ,
        t
        ,
        q
        )
        =
        
          
            
              π
              
                −
                
                  
                    n
                    2
                  
                
              
            
            
              δ
              
                m
              
            
          
        
        
          
            |
            
              (
              A
              +
              D
              
                )
                
                  −
                  1
                
              
            
            |
          
          
            
              1
              2
            
          
        
        
          
            
              u
              
                
                  v
                  2
                
              
            
            
              (
              y
              +
              u
              
                )
                
                  
                    
                      u
                      +
                      v
                    
                    2
                  
                
              
            
          
        
        
          
            
              Γ
              (
              
                
                  
                    n
                    +
                    v
                  
                  2
                
              
              )
            
            
              Γ
              (
              
                
                  v
                  2
                
              
              )
            
          
        
      
    
    {\displaystyle P(j,t,q)={\frac {\pi ^{-{\frac {n}{2}}}}{\delta ^{m}}}\left|(A+D)^{-1}\right|^{\frac {1}{2}}{\frac {u^{\frac {v}{2}}}{(y+u)^{\frac {u+v}{2}}}}{\frac {\Gamma ({\frac {n+v}{2}})}{\Gamma ({\frac {v}{2}})}}}
  

Then, CST compute the probability of the changepoint at time j with model q, 
  
    
      
        
          P
          
            t
          
        
        (
        j
        ,
        q
        )
      
    
    {\displaystyle P_{t}(j,q)}
  
 and 
  
    
      
        
          P
          
            j
          
          
            MAP
          
        
      
    
    {\displaystyle P_{j}^{\text{MAP}}}
  
 using a Viterbi algorithm.

  
    
      
        
          P
          
            t
          
        
        (
        j
        ,
        q
        )
        =
        (
        1
        −
        G
        (
        t
        −
        j
        −
        1
        )
        )
        P
        (
        j
        ,
        t
        ,
        q
        )
        p
        (
        q
        )
        
          P
          
            j
          
          
            MAP
          
        
      
    
    {\displaystyle P_{t}(j,q)=(1-G(t-j-1))P(j,t,q)p(q)P_{j}^{\text{MAP}}}
  

  
    
      
        
          P
          
            j
          
          
            MAP
          
        
        =
        
          max
          
            i
            ,
            q
          
        
        
          
            
              
                P
                
                  j
                
              
              (
              i
              ,
              q
              )
              g
              (
              j
              −
              i
              )
            
            
              1
              −
              G
              (
              j
              −
              i
              −
              1
              )
            
          
        
        ,
        ∀
        j
        <
        t
      
    
    {\displaystyle P_{j}^{\text{MAP}}=\max _{i,q}{\frac {P_{j}(i,q)g(j-i)}{1-G(j-i-1)}},\forall j<t}
  

The descriptions of the parameters and variables are as follows;

  
    
      
        A
        =
        
          ∑
          
            i
            =
            j
          
          
            t
          
        
        Φ
        (
        
          x
          
            i
          
        
        )
        Φ
        (
        
          x
          
            i
          
        
        
          )
          
            T
          
        
      
    
    {\displaystyle A=\sum _{i=j}^{t}\Phi (x_{i})\Phi (x_{i})^{T}}
  

  
    
      
        Φ
        (
        
          x
          
            i
          
        
        )
      
    
    {\displaystyle \Phi (x_{i})}
  
: a vector of m basis functions evaluated at state 
  
    
      
        
          x
          
            i
          
        
      
    
    {\displaystyle x_{i}}
  

  
    
      
        y
        =
        (
        
          ∑
          
            i
            =
            j
          
          
            t
          
        
        
          R
          
            i
          
          
            2
          
        
        )
        −
        
          b
          
            T
          
        
        (
        A
        +
        D
        
          )
          
            −
            1
          
        
        b
      
    
    {\displaystyle y=(\sum _{i=j}^{t}R_{i}^{2})-b^{T}(A+D)^{-1}b}
  

  
    
      
        b
        =
        
          ∑
          
            i
            =
            j
          
          
            t
          
        
        
          R
          
            i
          
        
        Φ
        (
        
          x
          
            i
          
        
        )
      
    
    {\displaystyle b=\sum _{i=j}^{t}R_{i}\Phi (x_{i})}
  

  
    
      
        
          R
          
            i
          
        
        =
        
          ∑
          
            j
            =
            i
          
          
            T
          
        
        
          γ
          
            j
            −
            i
          
        
        
          r
          
            j
          
        
      
    
    {\displaystyle R_{i}=\sum _{j=i}^{T}\gamma ^{j-i}r_{j}}
  

𝛾: Gamma function

  
    
      
        n
        =
        t
        −
        j
      
    
    {\displaystyle n=t-j}
  

m: The number of basis functions q has.
D: an m by m matrix with 
  
    
      
        
          δ
          
            −
            1
          
        
      
    
    {\displaystyle \delta ^{-1}}
  
 on the diagonal and zeros elsewhere
The skill length l is assumed to follow a Geometric distribution with parameter p

  
    
      
        
          g
          

          
          

          
        
        (
        l
        )
        =
        (
        1
        −
        p
        
          )
          
            l
            −
            1
          
        
        p
      
    
    {\displaystyle g_{}^{}(l)=(1-p)^{l-1}p}
  

  
    
      
        
          G
          

          
          

          
        
        (
        l
        )
        =
        (
        1
        −
        (
        1
        −
        p
        
          )
          
            l
          
        
        )
      
    
    {\displaystyle G_{}^{}(l)=(1-(1-p)^{l})}
  

  
    
      
        
          p
          

          
          

          
        
        =
        
          
            1
            k
          
        
      
    
    {\displaystyle p_{}^{}={\frac {1}{k}}}
  

k: Expected skill length
Using the method above, CST can segment data into a skill chain. The time complexity of the change point detection is 
  
    
      
        O
        (
        N
        L
        )
      
    
    {\displaystyle O(NL)}
  
 and storage size is 
  
    
      
        O
        (
        N
        c
        )
      
    
    {\displaystyle O(Nc)}
  
, where N is the number of particles, L is the time of computing 
  
    
      
        P
        (
        j
        ,
        t
        ,
        q
        )
      
    
    {\displaystyle P(j,t,q)}
  
, and there are 
  
    
      
        O
        (
        c
        )
      
    
    {\displaystyle O(c)}
  
 change points.
Next step is alignment. CST needs to align the component skills because the change-point does not occur in the exactly same places. Thus, when segmenting second trajectory after segmenting the first trajectory, it has a bias on the location of change point in the second trajectory. This bias follows a mixture of gaussians.
The last step is merging. CST merges skill chains into a skill tree.  CST merges a pair of trajectory segments by allocating the same skill. All trajectories have the same goal and it merges two chains by starting at their final segments. If two segments are statistically similar, it merges them. This procedure is repeated until it fails to merge a pair of skill segments. 
  
    
      
        P
        (
        j
        ,
        t
        ,
        q
        )
      
    
    {\displaystyle P(j,t,q)}
  
 are used to determine whether a pair of trajectories are modeled better as one skill or as two different skills.


== Pseudocode ==
The following pseudocode describes the change point detection algorithm:

particles := [];
Process each incoming data point
for t = 1:T do
    //Compute fit probabilities for all particles      
    for p ∈ particles do
        p_tjq := (1 − G(t − p.pos − 1)) × p.fit_prob × model_prior(p.model) × p.prev_MAP 
        p.MAP := p_tjq × g(t−p.pos) / (1 − G(t − p.pos − 1))
    end
    // Filter if necessary
    if the number of particles ≥ N then
        particles := particle_filter(p.MAP, M)
    end
    // Determine the Viterbi path
    for t = 1 do
        max_path := []
        max_MAP := 1/|Q|
    else
        max_particle := maxp p.MAP
        max_path := max_particle.path ∪ max_particle
        max_MAP := max_particle.MAP
    end
    // Create new particles for a changepoint at time t
    for q ∈ Q do
        new_p := create_particle(model=q, pos=t, prev_MAP=max_MAP, path=max_path)
        p := p ∪ new_p
    end
    // Update all particles
    for p ∈ P do
        particles := update_particle(current_state, current_reward, p)      
    end
end
// Return the most likely path to the final point
return max_path

function update_particle(current_state, current_reward, particle) is
    p := particle
    r_t := current_reward
    // Initialization
    if t = 0 then
        p.A := zero matrix(p.m, p.m)
        p.b := zero vector(p.m)
        p.z := zero vector(p.m)
        p.sum r := 0
        p.tr1 := 0
        p.tr2 := 0
    end if
    // Compute the basis function vector for the current state
    Φt := p.Φ (current state)
    // Update sufficient statistics
    p.A := p.A + ΦtΦTt
    p.z := 𝛾p.z + Φt
    p.b := p.b + rt p.z
    p.tr1 := 1 + 𝛾2 p.tr1
    p.sum r := sum p.r + r2t p.tr1 + 2𝛾rt p.tr2
    p.tr2 := 𝛾p.tr2 + rt p.tr1
    p.fit_prob := compute_fit_prob(p, v, u, delta, 𝛾)


== Assumptions ==
CTS assume that the demonstrated skills form a tree, the domain reward function is known and the best model for merging a pair of skills is the model selected for representing both individually.


== Advantages ==
CST is much faster learning algorithm than skill chaining. CST can be applied to learning higher dimensional policies.
Even unsuccessful episode can improve skills. Skills acquired using agent-centric features can be used for other problems.


== Uses ==
CST has been used to acquire skills from human demonstration in the PinBall domain. It has been also used to acquire skills from human demonstration on a mobile manipulator.


== See also ==
Prefrontal cortex basal ganglia working memory
State–action–reward–state–action
Sammon Mapping


== References ==

Konidaris, George; Scott Kuindersma; Andrew Barto; Roderic Grupen (2010). "Constructing Skill Trees for Reinforcement Learning Agents from Demonstration Trajectories". Advances in Neural Information Processing Systems 23.
Konidaris, George; Andrew Barto (2009). "Skill discovery in continuous reinforcement learning domains using skill chaining". Advances in Neural Information Processing Systems 22.
Fearnhead, Paul; Zhen Liu (2007). "On-line Inference for Multiple Change Points". Journal of the Royal Statistical Society.