# Forward–backward algorithm

Source: Wikipedia (https://en.wikipedia.org/wiki/Forward%E2%80%93backward_algorithm)

The forward–backward algorithm is an  inference algorithm for hidden Markov models which computes the posterior marginals of all hidden state variables given a sequence of observations/emissions 
  
    
      
        
          o
          
            1
            :
            T
          
        
        :=
        
          o
          
            1
          
        
        ,
        …
        ,
        
          o
          
            T
          
        
      
    
    {\displaystyle o_{1:T}:=o_{1},\dots ,o_{T}}
  
, i.e. it computes, for all hidden state variables 
  
    
      
        
          X
          
            t
          
        
        ∈
        {
        
          X
          
            1
          
        
        ,
        …
        ,
        
          X
          
            T
          
        
        }
      
    
    {\displaystyle X_{t}\in \{X_{1},\dots ,X_{T}\}}
  
, the distribution 
  
    
      
        P
        (
        
          X
          
            t
          
        
         
        
          |
        
         
        
          o
          
            1
            :
            T
          
        
        )
      
    
    {\displaystyle P(X_{t}\ |\ o_{1:T})}
  
. This inference task is usually called smoothing. The algorithm makes use of the principle of dynamic programming to efficiently compute the values that are required to obtain the posterior marginal distributions in two passes. The first pass goes forward in time while the second goes backward in time; hence the name forward–backward algorithm.
The term forward–backward algorithm is also used to refer to any algorithm belonging to the general class of algorithms that operate on sequence models in a forward–backward manner. In this sense, the descriptions in the remainder of this article refer only to one specific instance of this class.


== Overview ==
In the first pass, the forward–backward algorithm computes a set of forward probabilities which provide, for all 
  
    
      
        t
        ∈
        {
        1
        ,
        …
        ,
        T
        }
      
    
    {\displaystyle t\in \{1,\dots ,T\}}
  
, the probability of ending up in any particular state given the first 
  
    
      
        t
      
    
    {\displaystyle t}
  
 observations in the sequence, i.e. 
  
    
      
        P
        (
        
          X
          
            t
          
        
         
        
          |
        
         
        
          o
          
            1
            :
            t
          
        
        )
      
    
    {\displaystyle P(X_{t}\ |\ o_{1:t})}
  
. In the second pass, the algorithm computes a set of backward probabilities which provide the probability of observing the remaining observations given any starting point 
  
    
      
        t
      
    
    {\displaystyle t}
  
, i.e. 
  
    
      
        P
        (
        
          o
          
            t
            +
            1
            :
            T
          
        
         
        
          |
        
         
        
          X
          
            t
          
        
        )
      
    
    {\displaystyle P(o_{t+1:T}\ |\ X_{t})}
  
.  These two sets of probability distributions can then be combined to obtain the distribution over states at any specific point in time given the entire observation sequence:

  
    
      
        P
        (
        
          X
          
            t
          
        
         
        
          |
        
         
        
          o
          
            1
            :
            T
          
        
        )
        =
        P
        (
        
          X
          
            t
          
        
         
        
          |
        
         
        
          o
          
            1
            :
            t
          
        
        ,
        
          o
          
            t
            +
            1
            :
            T
          
        
        )
        ∝
        P
        (
        
          o
          
            t
            +
            1
            :
            T
          
        
         
        
          |
        
         
        
          X
          
            t
          
        
        )
        P
        (
        
          X
          
            t
          
        
        
          |
        
        
          o
          
            1
            :
            t
          
        
        )
      
    
    {\displaystyle P(X_{t}\ |\ o_{1:T})=P(X_{t}\ |\ o_{1:t},o_{t+1:T})\propto P(o_{t+1:T}\ |\ X_{t})P(X_{t}|o_{1:t})}
  

The last step follows from an application of the Bayes' rule and the conditional independence of 
  
    
      
        
          o
          
            t
            +
            1
            :
            T
          
        
      
    
    {\displaystyle o_{t+1:T}}
  
 and 
  
    
      
        
          o
          
            1
            :
            t
          
        
      
    
    {\displaystyle o_{1:t}}
  
 given 
  
    
      
        
          X
          
            t
          
        
      
    
    {\displaystyle X_{t}}
  
.
As outlined above, the algorithm involves three steps:

computing forward probabilities
computing backward probabilities
computing smoothed values.
The forward and backward steps may also be called "forward message pass" and "backward message pass" - these terms are due to the message-passing used in general belief propagation approaches. At each single observation in the sequence, probabilities to be used for calculations at the next observation are computed. The smoothing step can be calculated simultaneously during the backward pass. This step allows the algorithm to take into account any past observations of output for computing more accurate results.
The forward–backward algorithm can be used to find the most likely state for any point in time. It cannot, however, be used to find the most likely sequence of states (see Viterbi algorithm).


== Forward probabilities ==
The following description will use matrices of probability values instead of probability distributions. However, the forward-backward algorithm can generally be applied to both continuous and discrete probability models.
We transform the probability distributions related to a given hidden Markov model into matrix notation as follows.
The transition probabilities 
  
    
      
        
          P
        
        (
        
          X
          
            t
          
        
        ∣
        
          X
          
            t
            −
            1
          
        
        )
      
    
    {\displaystyle \mathbf {P} (X_{t}\mid X_{t-1})}
  
 of a given random variable 
  
    
      
        
          X
          
            t
          
        
      
    
    {\displaystyle X_{t}}
  
 representing all possible states in the hidden Markov model will be represented by the matrix 
  
    
      
        
          T
        
      
    
    {\displaystyle \mathbf {T} }
  
 where the column index 
  
    
      
        j
      
    
    {\displaystyle j}
  
 will represent the target state and the row index 
  
    
      
        i
      
    
    {\displaystyle i}
  
 represents the start state. A transition from row-vector state 
  
    
      
        
          
            π
            
              t
            
          
        
      
    
    {\displaystyle \mathbf {\pi _{t}} }
  
 to the incremental row-vector state 
  
    
      
        
          
            π
            
              t
              +
              1
            
          
        
      
    
    {\displaystyle \mathbf {\pi _{t+1}} }
  
 is written as 
  
    
      
        
          
            π
            
              t
              +
              1
            
          
        
        =
        
          
            π
            
              t
            
          
        
        
          T
        
      
    
    {\displaystyle \mathbf {\pi _{t+1}} =\mathbf {\pi _{t}} \mathbf {T} }
  
. The example below represents a system where the probability of staying in the same state after each step is 70% and the probability of transitioning to the other state is 30%.  The transition matrix is then:

  
    
      
        
          T
        
        =
        
          
            (
            
              
                
                  0.7
                
                
                  0.3
                
              
              
                
                  0.3
                
                
                  0.7
                
              
            
            )
          
        
      
    
    {\displaystyle \mathbf {T} ={\begin{pmatrix}0.7&0.3\\0.3&0.7\end{pmatrix}}}
  

In a typical Markov model, we would multiply a state vector by this matrix to obtain the probabilities for the subsequent state.  In a hidden Markov model the state is unknown, and we instead observe events associated with the possible states.  An event matrix of the form:

  
    
      
        
          B
        
        =
        
          
            (
            
              
                
                  0.9
                
                
                  0.1
                
              
              
                
                  0.2
                
                
                  0.8
                
              
            
            )
          
        
      
    
    {\displaystyle \mathbf {B} ={\begin{pmatrix}0.9&0.1\\0.2&0.8\end{pmatrix}}}
  

provides the probabilities for observing events given a particular state.  In the above example, event 1 will be observed 90% of the time if we are in state 1 while event 2 has a 10% probability of occurring in this state.  In contrast, event 1 will only be observed 20% of the time if we are in state 2 and event 2 has an 80% chance of occurring.  Given an arbitrary row-vector describing the state of the system (
  
    
      
        
          π
        
      
    
    {\displaystyle \mathbf {\pi } }
  
), the probability of observing event j is then:

  
    
      
        
          P
        
        (
        O
        =
        j
        )
        =
        
          ∑
          
            i
          
        
        
          π
          
            i
          
        
        
          B
          
            i
            ,
            j
          
        
      
    
    {\displaystyle \mathbf {P} (O=j)=\sum _{i}\pi _{i}B_{i,j}}
  

The probability of a given state leading to the observed event j can be represented in matrix form by multiplying the state row-vector (
  
    
      
        
          π
        
      
    
    {\displaystyle \mathbf {\pi } }
  
) with an observation matrix (
  
    
      
        
          
            O
            
              j
            
          
        
        =
        
          d
          i
          a
          g
        
        (
        
          B
          
            ∗
            ,
            
              o
              
                j
              
            
          
        
        )
      
    
    {\displaystyle \mathbf {O_{j}} =\mathrm {diag} (B_{*,o_{j}})}
  
) containing only diagonal entries. Continuing the above example, the observation matrix for event 1 would be:

  
    
      
        
          
            O
            
              1
            
          
        
        =
        
          
            (
            
              
                
                  0.9
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.2
                
              
            
            )
          
        
      
    
    {\displaystyle \mathbf {O_{1}} ={\begin{pmatrix}0.9&0.0\\0.0&0.2\end{pmatrix}}}
  

This allows us to calculate the new unnormalized probabilities state vector 
  
    
      
        
          
            π
            ′
          
        
      
    
    {\displaystyle \mathbf {\pi '} }
  
 through Bayes rule, weighting by the likelihood that each element of 
  
    
      
        
          π
        
      
    
    {\displaystyle \mathbf {\pi } }
  
 generated event 1 as:

  
    
      
        
          
            π
            ′
          
        
        =
        
          π
        
        
          
            O
            
              1
            
          
        
      
    
    {\displaystyle \mathbf {\pi '} =\mathbf {\pi } \mathbf {O_{1}} }
  

We can now make this general procedure specific to our series of observations. Assuming an initial state vector 
  
    
      
        
          
            π
          
          
            0
          
        
      
    
    {\displaystyle \mathbf {\pi } _{0}}
  
, (which can be optimized as a parameter through repetitions of the forward-backward procedure), we begin with 
  
    
      
        
          
            f
            
              0
              :
              0
            
          
        
        =
        
          
            π
          
          
            0
          
        
      
    
    {\displaystyle \mathbf {f_{0:0}} =\mathbf {\pi } _{0}}
  
,  then updating the state distribution and weighting by the likelihood of the first observation:

  
    
      
        
          
            f
            
              0
              :
              1
            
          
        
        =
        
          
            π
          
          
            0
          
        
        
          T
        
        
          
            O
            
              
                o
                
                  1
                
              
            
          
        
      
    
    {\displaystyle \mathbf {f_{0:1}} =\mathbf {\pi } _{0}\mathbf {T} \mathbf {O_{o_{1}}} }
  

This process can be carried forward with additional observations using:

  
    
      
        
          
            f
            
              0
              :
              t
            
          
        
        =
        
          
            f
            
              0
              :
              t
              −
              1
            
          
        
        
          T
        
        
          
            O
            
              
                o
                
                  t
                
              
            
          
        
      
    
    {\displaystyle \mathbf {f_{0:t}} =\mathbf {f_{0:t-1}} \mathbf {T} \mathbf {O_{o_{t}}} }
  

This value is the forward unnormalized probability vector.  The i'th entry of this vector provides:

  
    
      
        
          
            f
            
              0
              :
              t
            
          
        
        (
        i
        )
        =
        
          P
        
        (
        
          o
          
            1
          
        
        ,
        
          o
          
            2
          
        
        ,
        …
        ,
        
          o
          
            t
          
        
        ,
        
          X
          
            t
          
        
        =
        
          x
          
            i
          
        
        
          |
        
        
          
            π
          
          
            0
          
        
        )
      
    
    {\displaystyle \mathbf {f_{0:t}} (i)=\mathbf {P} (o_{1},o_{2},\dots ,o_{t},X_{t}=x_{i}|\mathbf {\pi } _{0})}
  

Typically, we will normalize the probability vector at each step so that its entries sum to 1.  A scaling factor is thus introduced at each step such that:

  
    
      
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              t
            
          
        
        =
        
          c
          
            t
          
          
            −
            1
          
        
         
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              t
              −
              1
            
          
        
        
          T
        
        
          
            O
            
              
                o
                
                  t
                
              
            
          
        
      
    
    {\displaystyle \mathbf {{\hat {f}}_{0:t}} =c_{t}^{-1}\ \mathbf {{\hat {f}}_{0:t-1}} \mathbf {T} \mathbf {O_{o_{t}}} }
  

where 
  
    
      
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              t
              −
              1
            
          
        
      
    
    {\displaystyle \mathbf {{\hat {f}}_{0:t-1}} }
  
 represents the scaled vector from the previous step and 
  
    
      
        
          c
          
            t
          
        
      
    
    {\displaystyle c_{t}}
  
 represents the scaling factor that causes the resulting vector's entries to sum to 1.  The product of the scaling factors is the total probability for observing the given events irrespective of the final states:

  
    
      
        
          P
        
        (
        
          o
          
            1
          
        
        ,
        
          o
          
            2
          
        
        ,
        …
        ,
        
          o
          
            t
          
        
        
          |
        
        
          
            π
          
          
            0
          
        
        )
        =
        
          ∏
          
            s
            =
            1
          
          
            t
          
        
        
          c
          
            s
          
        
      
    
    {\displaystyle \mathbf {P} (o_{1},o_{2},\dots ,o_{t}|\mathbf {\pi } _{0})=\prod _{s=1}^{t}c_{s}}
  

This allows us to interpret the scaled probability vector as:

  
    
      
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              t
            
          
        
        (
        i
        )
        =
        
          
            
              
                
                  f
                  
                    0
                    :
                    t
                  
                
              
              (
              i
              )
            
            
              
                ∏
                
                  s
                  =
                  1
                
                
                  t
                
              
              
                c
                
                  s
                
              
            
          
        
        =
        
          
            
              
                P
              
              (
              
                o
                
                  1
                
              
              ,
              
                o
                
                  2
                
              
              ,
              …
              ,
              
                o
                
                  t
                
              
              ,
              
                X
                
                  t
                
              
              =
              
                x
                
                  i
                
              
              
                |
              
              
                
                  π
                
                
                  0
                
              
              )
            
            
              
                P
              
              (
              
                o
                
                  1
                
              
              ,
              
                o
                
                  2
                
              
              ,
              …
              ,
              
                o
                
                  t
                
              
              
                |
              
              
                
                  π
                
                
                  0
                
              
              )
            
          
        
        =
        
          P
        
        (
        
          X
          
            t
          
        
        =
        
          x
          
            i
          
        
        
          |
        
        
          o
          
            1
          
        
        ,
        
          o
          
            2
          
        
        ,
        …
        ,
        
          o
          
            t
          
        
        ,
        
          
            π
          
          
            0
          
        
        )
      
    
    {\displaystyle \mathbf {{\hat {f}}_{0:t}} (i)={\frac {\mathbf {f_{0:t}} (i)}{\prod _{s=1}^{t}c_{s}}}={\frac {\mathbf {P} (o_{1},o_{2},\dots ,o_{t},X_{t}=x_{i}|\mathbf {\pi } _{0})}{\mathbf {P} (o_{1},o_{2},\dots ,o_{t}|\mathbf {\pi } _{0})}}=\mathbf {P} (X_{t}=x_{i}|o_{1},o_{2},\dots ,o_{t},\mathbf {\pi } _{0})}
  

We thus find that the product of the scaling factors provides us with the total probability for observing the given sequence up to time t and that the scaled probability vector provides us with the probability of being in each state at this time.


== Backward probabilities ==
A similar procedure can be constructed to find backward probabilities.  These intend to provide the probabilities:

  
    
      
        
          
            b
            
              t
              :
              T
            
          
        
        (
        i
        )
        =
        
          P
        
        (
        
          o
          
            t
            +
            1
          
        
        ,
        
          o
          
            t
            +
            2
          
        
        ,
        …
        ,
        
          o
          
            T
          
        
        
          |
        
        
          X
          
            t
          
        
        =
        
          x
          
            i
          
        
        )
      
    
    {\displaystyle \mathbf {b_{t:T}} (i)=\mathbf {P} (o_{t+1},o_{t+2},\dots ,o_{T}|X_{t}=x_{i})}
  

That is, we now want to assume that we start in a particular state (
  
    
      
        
          X
          
            t
          
        
        =
        
          x
          
            i
          
        
      
    
    {\displaystyle X_{t}=x_{i}}
  
), and we are now interested in the probability of observing all future events from this state.  Since the initial state is assumed as given (i.e. the prior probability of this state = 100%), we begin with:

  
    
      
        
          
            b
            
              T
              :
              T
            
          
        
        =
        [
        1
         
        1
         
        1
         
        …
        
          ]
          
            T
          
        
      
    
    {\displaystyle \mathbf {b_{T:T}} =[1\ 1\ 1\ \dots ]^{T}}
  

Notice that we are now using a column vector while the forward probabilities used row vectors.  We can then work backwards using:

  
    
      
        
          
            b
            
              t
              −
              1
              :
              T
            
          
        
        =
        
          T
        
        
          
            O
            
              t
            
          
        
        
          
            b
            
              t
              :
              T
            
          
        
      
    
    {\displaystyle \mathbf {b_{t-1:T}} =\mathbf {T} \mathbf {O_{t}} \mathbf {b_{t:T}} }
  

While we could normalize this vector as well so that its entries sum to one, this is not usually done.  Noting that each entry contains the probability of the future event sequence given a particular initial state, normalizing this vector would be equivalent to applying Bayes' theorem to find the likelihood of each initial state given the future events (assuming uniform priors for the final state vector).  However, it is more common to scale this vector using the same 
  
    
      
        
          c
          
            t
          
        
      
    
    {\displaystyle c_{t}}
  
 constants used in the forward probability calculations.  
  
    
      
        
          
            b
            
              T
              :
              T
            
          
        
      
    
    {\displaystyle \mathbf {b_{T:T}} }
  
 is not scaled, but subsequent operations use:

  
    
      
        
          
            
              
                
                  b
                  ^
                
              
            
            
              t
              −
              1
              :
              T
            
          
        
        =
        
          c
          
            t
          
          
            −
            1
          
        
        
          T
        
        
          
            O
            
              t
            
          
        
        
          
            
              
                
                  b
                  ^
                
              
            
            
              t
              :
              T
            
          
        
      
    
    {\displaystyle \mathbf {{\hat {b}}_{t-1:T}} =c_{t}^{-1}\mathbf {T} \mathbf {O_{t}} \mathbf {{\hat {b}}_{t:T}} }
  

where 
  
    
      
        
          
            
              
                
                  b
                  ^
                
              
            
            
              t
              :
              T
            
          
        
      
    
    {\displaystyle \mathbf {{\hat {b}}_{t:T}} }
  
 represents the previous, scaled vector.  This result is that the scaled probability vector is related to the backward probabilities by:

  
    
      
        
          
            
              
                
                  b
                  ^
                
              
            
            
              t
              :
              T
            
          
        
        (
        i
        )
        =
        
          
            
              
                
                  b
                  
                    t
                    :
                    T
                  
                
              
              (
              i
              )
            
            
              
                ∏
                
                  s
                  =
                  t
                  +
                  1
                
                
                  T
                
              
              
                c
                
                  s
                
              
            
          
        
      
    
    {\displaystyle \mathbf {{\hat {b}}_{t:T}} (i)={\frac {\mathbf {b_{t:T}} (i)}{\prod _{s=t+1}^{T}c_{s}}}}
  

This is useful because it allows us to find the total probability of being in each state at a given time, t, by multiplying these values:

  
    
      
        
          
            γ
            
              t
            
          
        
        (
        i
        )
        =
        
          P
        
        (
        
          X
          
            t
          
        
        =
        
          x
          
            i
          
        
        
          |
        
        
          o
          
            1
          
        
        ,
        
          o
          
            2
          
        
        ,
        …
        ,
        
          o
          
            T
          
        
        ,
        
          
            π
          
          
            0
          
        
        )
        =
        
          
            
              
                P
              
              (
              
                o
                
                  1
                
              
              ,
              
                o
                
                  2
                
              
              ,
              …
              ,
              
                o
                
                  T
                
              
              ,
              
                X
                
                  t
                
              
              =
              
                x
                
                  i
                
              
              
                |
              
              
                
                  π
                
                
                  0
                
              
              )
            
            
              
                P
              
              (
              
                o
                
                  1
                
              
              ,
              
                o
                
                  2
                
              
              ,
              …
              ,
              
                o
                
                  T
                
              
              
                |
              
              
                
                  π
                
                
                  0
                
              
              )
            
          
        
        =
        
          
            
              
                
                  f
                  
                    0
                    :
                    t
                  
                
              
              (
              i
              )
              ⋅
              
                
                  b
                  
                    t
                    :
                    T
                  
                
              
              (
              i
              )
            
            
              
                ∏
                
                  s
                  =
                  1
                
                
                  T
                
              
              
                c
                
                  s
                
              
            
          
        
        =
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              t
            
          
        
        (
        i
        )
        ⋅
        
          
            
              
                
                  b
                  ^
                
              
            
            
              t
              :
              T
            
          
        
        (
        i
        )
      
    
    {\displaystyle \mathbf {\gamma _{t}} (i)=\mathbf {P} (X_{t}=x_{i}|o_{1},o_{2},\dots ,o_{T},\mathbf {\pi } _{0})={\frac {\mathbf {P} (o_{1},o_{2},\dots ,o_{T},X_{t}=x_{i}|\mathbf {\pi } _{0})}{\mathbf {P} (o_{1},o_{2},\dots ,o_{T}|\mathbf {\pi } _{0})}}={\frac {\mathbf {f_{0:t}} (i)\cdot \mathbf {b_{t:T}} (i)}{\prod _{s=1}^{T}c_{s}}}=\mathbf {{\hat {f}}_{0:t}} (i)\cdot \mathbf {{\hat {b}}_{t:T}} (i)}
  

To understand this, we note that 
  
    
      
        
          
            f
            
              0
              :
              t
            
          
        
        (
        i
        )
        ⋅
        
          
            b
            
              t
              :
              T
            
          
        
        (
        i
        )
      
    
    {\displaystyle \mathbf {f_{0:t}} (i)\cdot \mathbf {b_{t:T}} (i)}
  
 provides the probability for observing the given events in a way that passes through state 
  
    
      
        
          x
          
            i
          
        
      
    
    {\displaystyle x_{i}}
  
 at time t.  This probability includes the forward probabilities covering all events up to time t as well as the backward probabilities which include all future events.  This is the numerator we are looking for in our equation, and we divide by the total probability of the observation sequence to normalize this value and extract only the probability that 
  
    
      
        
          X
          
            t
          
        
        =
        
          x
          
            i
          
        
      
    
    {\displaystyle X_{t}=x_{i}}
  
.  These values are sometimes called the "smoothed values" as they combine the forward and backward probabilities to compute a final probability.
The values 
  
    
      
        
          
            γ
            
              t
            
          
        
        (
        i
        )
      
    
    {\displaystyle \mathbf {\gamma _{t}} (i)}
  
 thus provide the probability of being in each state at time t.  As such, they are useful for determining the most probable state at any time. The term "most probable state" is somewhat ambiguous.  While the most probable state is the most likely to be correct at a given point, the sequence of individually probable states is not likely to be the most probable sequence.  This is because the probabilities for each point are calculated independently of each other. They do not take into account the transition probabilities between states, and it is thus possible to get states at two moments (t and t+1) that are both most probable at those time points but which have very little probability of occurring together, i.e. 
  
    
      
        
          P
        
        (
        
          X
          
            t
          
        
        =
        
          x
          
            i
          
        
        ,
        
          X
          
            t
            +
            1
          
        
        =
        
          x
          
            j
          
        
        )
        ≠
        
          P
        
        (
        
          X
          
            t
          
        
        =
        
          x
          
            i
          
        
        )
        
          P
        
        (
        
          X
          
            t
            +
            1
          
        
        =
        
          x
          
            j
          
        
        )
      
    
    {\displaystyle \mathbf {P} (X_{t}=x_{i},X_{t+1}=x_{j})\neq \mathbf {P} (X_{t}=x_{i})\mathbf {P} (X_{t+1}=x_{j})}
  
. The most probable sequence of states that produced an observation sequence can be found using the Viterbi algorithm.


== Example ==
This example takes as its basis the umbrella world in Russell & Norvig 2010 Chapter 15 pp. 567 in which we would like to infer the weather given observation of another person either carrying or not carrying an umbrella.  We assume two possible states for the weather: state 1 = rain, state 2 = no rain.  We assume that the weather has a 70% chance of staying the same each day and a 30% chance of changing.  The transition probabilities are then:

  
    
      
        
          T
        
        =
        
          
            (
            
              
                
                  0.7
                
                
                  0.3
                
              
              
                
                  0.3
                
                
                  0.7
                
              
            
            )
          
        
      
    
    {\displaystyle \mathbf {T} ={\begin{pmatrix}0.7&0.3\\0.3&0.7\end{pmatrix}}}
  

We also assume each state generates one of two possible events: event 1 = umbrella, event 2 = no umbrella.  The conditional probabilities for these occurring in each state are given by the probability matrix:

  
    
      
        
          B
        
        =
        
          
            (
            
              
                
                  0.9
                
                
                  0.1
                
              
              
                
                  0.2
                
                
                  0.8
                
              
            
            )
          
        
      
    
    {\displaystyle \mathbf {B} ={\begin{pmatrix}0.9&0.1\\0.2&0.8\end{pmatrix}}}
  

We then observe the following sequence of events: {umbrella, umbrella, no umbrella, umbrella, umbrella} which we will represent in our calculations as:

  
    
      
        
          
            O
            
              1
            
          
        
        =
        
          
            (
            
              
                
                  0.9
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.2
                
              
            
            )
          
        
         
         
        
          
            O
            
              2
            
          
        
        =
        
          
            (
            
              
                
                  0.9
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.2
                
              
            
            )
          
        
         
         
        
          
            O
            
              3
            
          
        
        =
        
          
            (
            
              
                
                  0.1
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.8
                
              
            
            )
          
        
         
         
        
          
            O
            
              4
            
          
        
        =
        
          
            (
            
              
                
                  0.9
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.2
                
              
            
            )
          
        
         
         
        
          
            O
            
              5
            
          
        
        =
        
          
            (
            
              
                
                  0.9
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.2
                
              
            
            )
          
        
      
    
    {\displaystyle \mathbf {O_{1}} ={\begin{pmatrix}0.9&0.0\\0.0&0.2\end{pmatrix}}~~\mathbf {O_{2}} ={\begin{pmatrix}0.9&0.0\\0.0&0.2\end{pmatrix}}~~\mathbf {O_{3}} ={\begin{pmatrix}0.1&0.0\\0.0&0.8\end{pmatrix}}~~\mathbf {O_{4}} ={\begin{pmatrix}0.9&0.0\\0.0&0.2\end{pmatrix}}~~\mathbf {O_{5}} ={\begin{pmatrix}0.9&0.0\\0.0&0.2\end{pmatrix}}}
  

Note that 
  
    
      
        
          
            O
            
              3
            
          
        
      
    
    {\displaystyle \mathbf {O_{3}} }
  
 differs from the others because of the "no umbrella" observation.
In computing the forward probabilities we begin with:

  
    
      
        
          
            f
            
              0
              :
              0
            
          
        
        =
        
          
            (
            
              
                
                  0.5
                
                
                  0.5
                
              
            
            )
          
        
      
    
    {\displaystyle \mathbf {f_{0:0}} ={\begin{pmatrix}0.5&0.5\end{pmatrix}}}
  

which is our prior state vector indicating that we don't know which state the weather is in before our observations.  While a state vector should be given as a row vector, we will use the transpose of the matrix so that the calculations below are easier to read.  Our calculations are then written in the form:

  
    
      
        (
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              t
            
          
        
        
          )
          
            T
          
        
        =
        
          c
          
            t
          
          
            −
            1
          
        
        
          
            O
            
              t
            
          
        
        (
        
          T
        
        
          )
          
            T
          
        
        (
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              t
              −
              1
            
          
        
        
          )
          
            T
          
        
      
    
    {\displaystyle (\mathbf {{\hat {f}}_{0:t}} )^{T}=c_{t}^{-1}\mathbf {O_{t}} (\mathbf {T} )^{T}(\mathbf {{\hat {f}}_{0:t-1}} )^{T}}
  

instead of:

  
    
      
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              t
            
          
        
        =
        
          c
          
            t
          
          
            −
            1
          
        
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              t
              −
              1
            
          
        
        
          T
        
        
          
            O
            
              t
            
          
        
      
    
    {\displaystyle \mathbf {{\hat {f}}_{0:t}} =c_{t}^{-1}\mathbf {{\hat {f}}_{0:t-1}} \mathbf {T} \mathbf {O_{t}} }
  

Notice that the transformation matrix is also transposed, but in our example the transpose is equal to the original matrix.  Performing these calculations and normalizing the results provides:

  
    
      
        (
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              1
            
          
        
        
          )
          
            T
          
        
        =
        
          c
          
            1
          
          
            −
            1
          
        
        
          
            (
            
              
                
                  0.9
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.2
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.7
                
                
                  0.3
                
              
              
                
                  0.3
                
                
                  0.7
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.5000
                
              
              
                
                  0.5000
                
              
            
            )
          
        
        =
        
          c
          
            1
          
          
            −
            1
          
        
        
          
            (
            
              
                
                  0.4500
                
              
              
                
                  0.1000
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.8182
                
              
              
                
                  0.1818
                
              
            
            )
          
        
      
    
    {\displaystyle (\mathbf {{\hat {f}}_{0:1}} )^{T}=c_{1}^{-1}{\begin{pmatrix}0.9&0.0\\0.0&0.2\end{pmatrix}}{\begin{pmatrix}0.7&0.3\\0.3&0.7\end{pmatrix}}{\begin{pmatrix}0.5000\\0.5000\end{pmatrix}}=c_{1}^{-1}{\begin{pmatrix}0.4500\\0.1000\end{pmatrix}}={\begin{pmatrix}0.8182\\0.1818\end{pmatrix}}}
  

  
    
      
        (
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              2
            
          
        
        
          )
          
            T
          
        
        =
        
          c
          
            2
          
          
            −
            1
          
        
        
          
            (
            
              
                
                  0.9
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.2
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.7
                
                
                  0.3
                
              
              
                
                  0.3
                
                
                  0.7
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.8182
                
              
              
                
                  0.1818
                
              
            
            )
          
        
        =
        
          c
          
            2
          
          
            −
            1
          
        
        
          
            (
            
              
                
                  0.5645
                
              
              
                
                  0.0745
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.8834
                
              
              
                
                  0.1166
                
              
            
            )
          
        
      
    
    {\displaystyle (\mathbf {{\hat {f}}_{0:2}} )^{T}=c_{2}^{-1}{\begin{pmatrix}0.9&0.0\\0.0&0.2\end{pmatrix}}{\begin{pmatrix}0.7&0.3\\0.3&0.7\end{pmatrix}}{\begin{pmatrix}0.8182\\0.1818\end{pmatrix}}=c_{2}^{-1}{\begin{pmatrix}0.5645\\0.0745\end{pmatrix}}={\begin{pmatrix}0.8834\\0.1166\end{pmatrix}}}
  

  
    
      
        (
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              3
            
          
        
        
          )
          
            T
          
        
        =
        
          c
          
            3
          
          
            −
            1
          
        
        
          
            (
            
              
                
                  0.1
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.8
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.7
                
                
                  0.3
                
              
              
                
                  0.3
                
                
                  0.7
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.8834
                
              
              
                
                  0.1166
                
              
            
            )
          
        
        =
        
          c
          
            3
          
          
            −
            1
          
        
        
          
            (
            
              
                
                  0.0653
                
              
              
                
                  0.2772
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.1907
                
              
              
                
                  0.8093
                
              
            
            )
          
        
      
    
    {\displaystyle (\mathbf {{\hat {f}}_{0:3}} )^{T}=c_{3}^{-1}{\begin{pmatrix}0.1&0.0\\0.0&0.8\end{pmatrix}}{\begin{pmatrix}0.7&0.3\\0.3&0.7\end{pmatrix}}{\begin{pmatrix}0.8834\\0.1166\end{pmatrix}}=c_{3}^{-1}{\begin{pmatrix}0.0653\\0.2772\end{pmatrix}}={\begin{pmatrix}0.1907\\0.8093\end{pmatrix}}}
  

  
    
      
        (
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              4
            
          
        
        
          )
          
            T
          
        
        =
        
          c
          
            4
          
          
            −
            1
          
        
        
          
            (
            
              
                
                  0.9
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.2
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.7
                
                
                  0.3
                
              
              
                
                  0.3
                
                
                  0.7
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.1907
                
              
              
                
                  0.8093
                
              
            
            )
          
        
        =
        
          c
          
            4
          
          
            −
            1
          
        
        
          
            (
            
              
                
                  0.3386
                
              
              
                
                  0.1247
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.7308
                
              
              
                
                  0.2692
                
              
            
            )
          
        
      
    
    {\displaystyle (\mathbf {{\hat {f}}_{0:4}} )^{T}=c_{4}^{-1}{\begin{pmatrix}0.9&0.0\\0.0&0.2\end{pmatrix}}{\begin{pmatrix}0.7&0.3\\0.3&0.7\end{pmatrix}}{\begin{pmatrix}0.1907\\0.8093\end{pmatrix}}=c_{4}^{-1}{\begin{pmatrix}0.3386\\0.1247\end{pmatrix}}={\begin{pmatrix}0.7308\\0.2692\end{pmatrix}}}
  

  
    
      
        (
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              5
            
          
        
        
          )
          
            T
          
        
        =
        
          c
          
            5
          
          
            −
            1
          
        
        
          
            (
            
              
                
                  0.9
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.2
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.7
                
                
                  0.3
                
              
              
                
                  0.3
                
                
                  0.7
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.7308
                
              
              
                
                  0.2692
                
              
            
            )
          
        
        =
        
          c
          
            5
          
          
            −
            1
          
        
        
          
            (
            
              
                
                  0.5331
                
              
              
                
                  0.0815
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.8673
                
              
              
                
                  0.1327
                
              
            
            )
          
        
      
    
    {\displaystyle (\mathbf {{\hat {f}}_{0:5}} )^{T}=c_{5}^{-1}{\begin{pmatrix}0.9&0.0\\0.0&0.2\end{pmatrix}}{\begin{pmatrix}0.7&0.3\\0.3&0.7\end{pmatrix}}{\begin{pmatrix}0.7308\\0.2692\end{pmatrix}}=c_{5}^{-1}{\begin{pmatrix}0.5331\\0.0815\end{pmatrix}}={\begin{pmatrix}0.8673\\0.1327\end{pmatrix}}}
  

For the backward probabilities, we start with:

  
    
      
        
          
            b
            
              5
              :
              5
            
          
        
        =
        
          
            (
            
              
                
                  1.0
                
              
              
                
                  1.0
                
              
            
            )
          
        
      
    
    {\displaystyle \mathbf {b_{5:5}} ={\begin{pmatrix}1.0\\1.0\end{pmatrix}}}
  

We are then able to compute (using the observations in reverse order and normalizing with different constants):

  
    
      
        
          
            
              
                
                  b
                  ^
                
              
            
            
              4
              :
              5
            
          
        
        =
        α
        
          
            (
            
              
                
                  0.7
                
                
                  0.3
                
              
              
                
                  0.3
                
                
                  0.7
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.9
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.2
                
              
            
            )
          
        
        
          
            (
            
              
                
                  1.0000
                
              
              
                
                  1.0000
                
              
            
            )
          
        
        =
        α
        
          
            (
            
              
                
                  0.6900
                
              
              
                
                  0.4100
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.6273
                
              
              
                
                  0.3727
                
              
            
            )
          
        
      
    
    {\displaystyle \mathbf {{\hat {b}}_{4:5}} =\alpha {\begin{pmatrix}0.7&0.3\\0.3&0.7\end{pmatrix}}{\begin{pmatrix}0.9&0.0\\0.0&0.2\end{pmatrix}}{\begin{pmatrix}1.0000\\1.0000\end{pmatrix}}=\alpha {\begin{pmatrix}0.6900\\0.4100\end{pmatrix}}={\begin{pmatrix}0.6273\\0.3727\end{pmatrix}}}
  

  
    
      
        
          
            
              
                
                  b
                  ^
                
              
            
            
              3
              :
              5
            
          
        
        =
        α
        
          
            (
            
              
                
                  0.7
                
                
                  0.3
                
              
              
                
                  0.3
                
                
                  0.7
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.9
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.2
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.6273
                
              
              
                
                  0.3727
                
              
            
            )
          
        
        =
        α
        
          
            (
            
              
                
                  0.4175
                
              
              
                
                  0.2215
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.6533
                
              
              
                
                  0.3467
                
              
            
            )
          
        
      
    
    {\displaystyle \mathbf {{\hat {b}}_{3:5}} =\alpha {\begin{pmatrix}0.7&0.3\\0.3&0.7\end{pmatrix}}{\begin{pmatrix}0.9&0.0\\0.0&0.2\end{pmatrix}}{\begin{pmatrix}0.6273\\0.3727\end{pmatrix}}=\alpha {\begin{pmatrix}0.4175\\0.2215\end{pmatrix}}={\begin{pmatrix}0.6533\\0.3467\end{pmatrix}}}
  

  
    
      
        
          
            
              
                
                  b
                  ^
                
              
            
            
              2
              :
              5
            
          
        
        =
        α
        
          
            (
            
              
                
                  0.7
                
                
                  0.3
                
              
              
                
                  0.3
                
                
                  0.7
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.1
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.8
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.6533
                
              
              
                
                  0.3467
                
              
            
            )
          
        
        =
        α
        
          
            (
            
              
                
                  0.1289
                
              
              
                
                  0.2138
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.3763
                
              
              
                
                  0.6237
                
              
            
            )
          
        
      
    
    {\displaystyle \mathbf {{\hat {b}}_{2:5}} =\alpha {\begin{pmatrix}0.7&0.3\\0.3&0.7\end{pmatrix}}{\begin{pmatrix}0.1&0.0\\0.0&0.8\end{pmatrix}}{\begin{pmatrix}0.6533\\0.3467\end{pmatrix}}=\alpha {\begin{pmatrix}0.1289\\0.2138\end{pmatrix}}={\begin{pmatrix}0.3763\\0.6237\end{pmatrix}}}
  

  
    
      
        
          
            
              
                
                  b
                  ^
                
              
            
            
              1
              :
              5
            
          
        
        =
        α
        
          
            (
            
              
                
                  0.7
                
                
                  0.3
                
              
              
                
                  0.3
                
                
                  0.7
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.9
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.2
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.3763
                
              
              
                
                  0.6237
                
              
            
            )
          
        
        =
        α
        
          
            (
            
              
                
                  0.2745
                
              
              
                
                  0.1889
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.5923
                
              
              
                
                  0.4077
                
              
            
            )
          
        
      
    
    {\displaystyle \mathbf {{\hat {b}}_{1:5}} =\alpha {\begin{pmatrix}0.7&0.3\\0.3&0.7\end{pmatrix}}{\begin{pmatrix}0.9&0.0\\0.0&0.2\end{pmatrix}}{\begin{pmatrix}0.3763\\0.6237\end{pmatrix}}=\alpha {\begin{pmatrix}0.2745\\0.1889\end{pmatrix}}={\begin{pmatrix}0.5923\\0.4077\end{pmatrix}}}
  

  
    
      
        
          
            
              
                
                  b
                  ^
                
              
            
            
              0
              :
              5
            
          
        
        =
        α
        
          
            (
            
              
                
                  0.7
                
                
                  0.3
                
              
              
                
                  0.3
                
                
                  0.7
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.9
                
                
                  0.0
                
              
              
                
                  0.0
                
                
                  0.2
                
              
            
            )
          
        
        
          
            (
            
              
                
                  0.5923
                
              
              
                
                  0.4077
                
              
            
            )
          
        
        =
        α
        
          
            (
            
              
                
                  0.3976
                
              
              
                
                  0.2170
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.6469
                
              
              
                
                  0.3531
                
              
            
            )
          
        
      
    
    {\displaystyle \mathbf {{\hat {b}}_{0:5}} =\alpha {\begin{pmatrix}0.7&0.3\\0.3&0.7\end{pmatrix}}{\begin{pmatrix}0.9&0.0\\0.0&0.2\end{pmatrix}}{\begin{pmatrix}0.5923\\0.4077\end{pmatrix}}=\alpha {\begin{pmatrix}0.3976\\0.2170\end{pmatrix}}={\begin{pmatrix}0.6469\\0.3531\end{pmatrix}}}
  

Finally, we will compute the smoothed probability values.  These results must also be scaled so that its entries sum to 1 because we did not scale the backward probabilities with the 
  
    
      
        
          c
          
            t
          
        
      
    
    {\displaystyle c_{t}}
  
's found earlier.  The backward probability vectors above thus actually represent the likelihood of each state at time t given the future observations.  Because these vectors are proportional to the actual backward probabilities, the result has to be scaled an additional time.

  
    
      
        (
        
          
            γ
            
              0
            
          
        
        
          )
          
            T
          
        
        =
        α
        
          
            (
            
              
                
                  0.5000
                
              
              
                
                  0.5000
                
              
            
            )
          
        
        ∘
        
          
            (
            
              
                
                  0.6469
                
              
              
                
                  0.3531
                
              
            
            )
          
        
        =
        α
        
          
            (
            
              
                
                  0.3235
                
              
              
                
                  0.1765
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.6469
                
              
              
                
                  0.3531
                
              
            
            )
          
        
      
    
    {\displaystyle (\mathbf {\gamma _{0}} )^{T}=\alpha {\begin{pmatrix}0.5000\\0.5000\end{pmatrix}}\circ {\begin{pmatrix}0.6469\\0.3531\end{pmatrix}}=\alpha {\begin{pmatrix}0.3235\\0.1765\end{pmatrix}}={\begin{pmatrix}0.6469\\0.3531\end{pmatrix}}}
  

  
    
      
        (
        
          
            γ
            
              1
            
          
        
        
          )
          
            T
          
        
        =
        α
        
          
            (
            
              
                
                  0.8182
                
              
              
                
                  0.1818
                
              
            
            )
          
        
        ∘
        
          
            (
            
              
                
                  0.5923
                
              
              
                
                  0.4077
                
              
            
            )
          
        
        =
        α
        
          
            (
            
              
                
                  0.4846
                
              
              
                
                  0.0741
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.8673
                
              
              
                
                  0.1327
                
              
            
            )
          
        
      
    
    {\displaystyle (\mathbf {\gamma _{1}} )^{T}=\alpha {\begin{pmatrix}0.8182\\0.1818\end{pmatrix}}\circ {\begin{pmatrix}0.5923\\0.4077\end{pmatrix}}=\alpha {\begin{pmatrix}0.4846\\0.0741\end{pmatrix}}={\begin{pmatrix}0.8673\\0.1327\end{pmatrix}}}
  

  
    
      
        (
        
          
            γ
            
              2
            
          
        
        
          )
          
            T
          
        
        =
        α
        
          
            (
            
              
                
                  0.8834
                
              
              
                
                  0.1166
                
              
            
            )
          
        
        ∘
        
          
            (
            
              
                
                  0.3763
                
              
              
                
                  0.6237
                
              
            
            )
          
        
        =
        α
        
          
            (
            
              
                
                  0.3324
                
              
              
                
                  0.0728
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.8204
                
              
              
                
                  0.1796
                
              
            
            )
          
        
      
    
    {\displaystyle (\mathbf {\gamma _{2}} )^{T}=\alpha {\begin{pmatrix}0.8834\\0.1166\end{pmatrix}}\circ {\begin{pmatrix}0.3763\\0.6237\end{pmatrix}}=\alpha {\begin{pmatrix}0.3324\\0.0728\end{pmatrix}}={\begin{pmatrix}0.8204\\0.1796\end{pmatrix}}}
  

  
    
      
        (
        
          
            γ
            
              3
            
          
        
        
          )
          
            T
          
        
        =
        α
        
          
            (
            
              
                
                  0.1907
                
              
              
                
                  0.8093
                
              
            
            )
          
        
        ∘
        
          
            (
            
              
                
                  0.6533
                
              
              
                
                  0.3467
                
              
            
            )
          
        
        =
        α
        
          
            (
            
              
                
                  0.1246
                
              
              
                
                  0.2806
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.3075
                
              
              
                
                  0.6925
                
              
            
            )
          
        
      
    
    {\displaystyle (\mathbf {\gamma _{3}} )^{T}=\alpha {\begin{pmatrix}0.1907\\0.8093\end{pmatrix}}\circ {\begin{pmatrix}0.6533\\0.3467\end{pmatrix}}=\alpha {\begin{pmatrix}0.1246\\0.2806\end{pmatrix}}={\begin{pmatrix}0.3075\\0.6925\end{pmatrix}}}
  

  
    
      
        (
        
          
            γ
            
              4
            
          
        
        
          )
          
            T
          
        
        =
        α
        
          
            (
            
              
                
                  0.7308
                
              
              
                
                  0.2692
                
              
            
            )
          
        
        ∘
        
          
            (
            
              
                
                  0.6273
                
              
              
                
                  0.3727
                
              
            
            )
          
        
        =
        α
        
          
            (
            
              
                
                  0.4584
                
              
              
                
                  0.1003
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.8204
                
              
              
                
                  0.1796
                
              
            
            )
          
        
      
    
    {\displaystyle (\mathbf {\gamma _{4}} )^{T}=\alpha {\begin{pmatrix}0.7308\\0.2692\end{pmatrix}}\circ {\begin{pmatrix}0.6273\\0.3727\end{pmatrix}}=\alpha {\begin{pmatrix}0.4584\\0.1003\end{pmatrix}}={\begin{pmatrix}0.8204\\0.1796\end{pmatrix}}}
  

  
    
      
        (
        
          
            γ
            
              5
            
          
        
        
          )
          
            T
          
        
        =
        α
        
          
            (
            
              
                
                  0.8673
                
              
              
                
                  0.1327
                
              
            
            )
          
        
        ∘
        
          
            (
            
              
                
                  1.0000
                
              
              
                
                  1.0000
                
              
            
            )
          
        
        =
        α
        
          
            (
            
              
                
                  0.8673
                
              
              
                
                  0.1327
                
              
            
            )
          
        
        =
        
          
            (
            
              
                
                  0.8673
                
              
              
                
                  0.1327
                
              
            
            )
          
        
      
    
    {\displaystyle (\mathbf {\gamma _{5}} )^{T}=\alpha {\begin{pmatrix}0.8673\\0.1327\end{pmatrix}}\circ {\begin{pmatrix}1.0000\\1.0000\end{pmatrix}}=\alpha {\begin{pmatrix}0.8673\\0.1327\end{pmatrix}}={\begin{pmatrix}0.8673\\0.1327\end{pmatrix}}}
  

Notice that the value of 
  
    
      
        
          
            γ
            
              0
            
          
        
      
    
    {\displaystyle \mathbf {\gamma _{0}} }
  
 is equal to 
  
    
      
        
          
            
              
                
                  b
                  ^
                
              
            
            
              0
              :
              5
            
          
        
      
    
    {\displaystyle \mathbf {{\hat {b}}_{0:5}} }
  
 and that 
  
    
      
        
          
            γ
            
              5
            
          
        
      
    
    {\displaystyle \mathbf {\gamma _{5}} }
  
 is equal to 
  
    
      
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              5
            
          
        
      
    
    {\displaystyle \mathbf {{\hat {f}}_{0:5}} }
  
.  This follows naturally because both 
  
    
      
        
          
            
              
                
                  f
                  ^
                
              
            
            
              0
              :
              5
            
          
        
      
    
    {\displaystyle \mathbf {{\hat {f}}_{0:5}} }
  
 and 
  
    
      
        
          
            
              
                
                  b
                  ^
                
              
            
            
              0
              :
              5
            
          
        
      
    
    {\displaystyle \mathbf {{\hat {b}}_{0:5}} }
  
 begin with uniform priors over the initial and final state vectors (respectively) and take into account all of the observations.  However, 
  
    
      
        
          
            γ
            
              0
            
          
        
      
    
    {\displaystyle \mathbf {\gamma _{0}} }
  
 will only be equal to 
  
    
      
        
          
            
              
                
                  b
                  ^
                
              
            
            
              0
              :
              5
            
          
        
      
    
    {\displaystyle \mathbf {{\hat {b}}_{0:5}} }
  
 when our initial state vector represents a uniform prior (i.e. all entries are equal).  When this is not the case 
  
    
      
        
          
            
              
                
                  b
                  ^
                
              
            
            
              0
              :
              5
            
          
        
      
    
    {\displaystyle \mathbf {{\hat {b}}_{0:5}} }
  
 needs to be combined with the initial state vector to find the most likely initial state.  We thus find that the forward probabilities by themselves are sufficient to calculate the most likely final state.  Similarly, the backward probabilities can be combined with the initial state vector to provide the most probable initial state given the observations.  The forward and backward probabilities need only be combined to infer the most probable states between the initial and final points.
The calculations above reveal that the most probable weather state on every day except for the third one was "rain".  They tell us more than this, however, as they now provide a way to quantify the probabilities of each state at different times.  Perhaps most importantly, our value at 
  
    
      
        
          
            γ
            
              5
            
          
        
      
    
    {\displaystyle \mathbf {\gamma _{5}} }
  
 quantifies our knowledge of the state vector at the end of the observation sequence.  We can then use this to predict the probability of the various weather states tomorrow as well as the probability of observing an umbrella.


== Performance ==
The forward–backward algorithm runs with time complexity 
  
    
      
        O
        (
        
          S
          
            2
          
        
        T
        )
      
    
    {\displaystyle O(S^{2}T)}
  
 in space 
  
    
      
        O
        (
        S
        T
        )
      
    
    {\displaystyle O(ST)}
  
, where 
  
    
      
        T
      
    
    {\displaystyle T}
  
 is the length of the time sequence and 
  
    
      
        S
      
    
    {\displaystyle S}
  
 is the number of symbols in the state alphabet.  The algorithm can also run in constant space with time complexity 
  
    
      
        O
        (
        
          S
          
            2
          
        
        
          T
          
            2
          
        
        )
      
    
    {\displaystyle O(S^{2}T^{2})}
  
 by recomputing values at each step. For comparison, a brute-force procedure would generate all possible 
  
    
      
        
          S
          
            T
          
        
      
    
    {\displaystyle S^{T}}
  
 state sequences and calculate the joint probability of each state sequence with the observed series of events, which would have time complexity 
  
    
      
        O
        (
        T
        ⋅
        
          S
          
            T
          
        
        )
      
    
    {\displaystyle O(T\cdot S^{T})}
  
. Brute force is intractable for realistic problems, as the number of possible hidden node sequences typically is extremely high.
An enhancement to the general forward-backward algorithm, called the Island algorithm, trades smaller memory usage for longer running time, taking 
  
    
      
        O
        (
        
          S
          
            2
          
        
        T
        log
        ⁡
        T
        )
      
    
    {\displaystyle O(S^{2}T\log T)}
  
 time and 
  
    
      
        O
        (
        S
        log
        ⁡
        T
        )
      
    
    {\displaystyle O(S\log T)}
  
 memory. Furthermore, it is possible to invert the process model to obtain an 
  
    
      
        O
        (
        S
        )
      
    
    {\displaystyle O(S)}
  
 space, 
  
    
      
        O
        (
        
          S
          
            2
          
        
        T
        )
      
    
    {\displaystyle O(S^{2}T)}
  
 time algorithm, although the inverted process may not exist or be ill-conditioned.
In addition, algorithms have been developed to compute 
  
    
      
        
          
            f
            
              0
              :
              t
              +
              1
            
          
        
      
    
    {\displaystyle \mathbf {f_{0:t+1}} }
  
 efficiently through online smoothing such as the fixed-lag smoothing (FLS) algorithm.


== Pseudocode ==
algorithm forward_backward is
    input: guessState
           int sequenceIndex
    output: result

    if sequenceIndex is past the end of the sequence then
        return 1
    if (guessState, sequenceIndex) has been seen before then
        return saved result

    result := 0

    for each neighboring state n:
        result := result + (transition probability from guessState to 
                            n given observation element at sequenceIndex)
                            × Backward(n, sequenceIndex + 1)

    save result for (guessState, sequenceIndex)

    return result


== Python example ==
Given HMM (just like in Viterbi algorithm) represented in the Python programming language:

We can write the implementation of the forward-backward algorithm like this:

The function fwd_bkw takes the following arguments: 
x is the sequence of observations, e.g. ['normal', 'cold', 'dizzy']; 
states is the set of hidden states; 
a_0 is the start probability; 
a are the transition probabilities; 
and e are the emission probabilities.
For simplicity of code, we assume that the observation sequence x is non-empty and that  a[i][j] and e[i][j] is defined for all states i,j.
In the running example, the forward-backward algorithm is used as follows:


== See also ==
Baum–Welch algorithm
Viterbi algorithm
BCJR algorithm


== References ==

Lawrence R. Rabiner, A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition. Proceedings of the IEEE, 77 (2), p. 257–286, February 1989. 10.1109/5.18626
Lawrence R. Rabiner, B. H. Juang (January 1986). "An introduction to hidden Markov models". IEEE ASSP Magazine: 4–15.
Eugene Charniak (1993). Statistical Language Learning. Cambridge, Massachusetts: MIT Press. ISBN 978-0-262-53141-2.
Stuart Russell and Peter Norvig (2010). Artificial Intelligence A Modern Approach 3rd Edition. Upper Saddle River, New Jersey: Pearson Education/Prentice-Hall. ISBN 978-0-13-604259-4.


== External links ==
An interactive spreadsheet for teaching the forward–backward algorithm (spreadsheet and article with step-by-step walk-through)
Tutorial of hidden Markov models including the forward–backward algorithm
Collection of AI algorithms implemented in Java (including HMM and the forward–backward algorithm)