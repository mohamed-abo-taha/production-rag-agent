# Characteristic samples

Source: Wikipedia (https://en.wikipedia.org/wiki/Characteristic_samples)

Characteristic samples is a concept in the field of grammatical inference, related to passive learning. In passive learning, an inference algorithm 
  
    
      
        I
      
    
    {\displaystyle I}
  
 is given a set of pairs of strings and labels 
  
    
      
        S
      
    
    {\displaystyle S}
  
, and returns a representation 
  
    
      
        R
      
    
    {\displaystyle R}
  
 that is consistent with 
  
    
      
        S
      
    
    {\displaystyle S}
  
. Characteristic samples consider the scenario when the goal is not only finding a representation consistent with 
  
    
      
        S
      
    
    {\displaystyle S}
  
, but finding a representation that recognizes a specific target language.
A characteristic sample of language 
  
    
      
        L
      
    
    {\displaystyle L}
  
 is a set of pairs of the form 
  
    
      
        (
        s
        ,
        l
        (
        s
        )
        )
      
    
    {\displaystyle (s,l(s))}
  
 where:

  
    
      
        l
        (
        s
        )
        =
        1
      
    
    {\displaystyle l(s)=1}
  
 if and only if 
  
    
      
        s
        ∈
        L
      
    
    {\displaystyle s\in L}
  

  
    
      
        l
        (
        s
        )
        =
        −
        1
      
    
    {\displaystyle l(s)=-1}
  
 if and only if 
  
    
      
        s
        ∉
        L
      
    
    {\displaystyle s\notin L}
  

Given the characteristic sample 
  
    
      
        S
      
    
    {\displaystyle S}
  
, 
  
    
      
        I
      
    
    {\displaystyle I}
  
's output on it is a representation 
  
    
      
        R
      
    
    {\displaystyle R}
  
, e.g. an automaton, that recognizes 
  
    
      
        L
      
    
    {\displaystyle L}
  
.


== Formal Definition ==


=== The Learning Paradigm associated with Characteristic Samples ===
There are three entities in the learning paradigm connected to characteristic samples, the adversary, the teacher and the inference algorithm.
Given a class of languages 
  
    
      
        
          C
        
      
    
    {\displaystyle \mathbb {C} }
  
 and a class of representations for the languages 
  
    
      
        
          R
        
      
    
    {\displaystyle \mathbb {R} }
  
, the paradigm goes as follows:

The adversary 
  
    
      
        A
      
    
    {\displaystyle A}
  
 selects a language 
  
    
      
        L
        ∈
        
          C
        
      
    
    {\displaystyle L\in \mathbb {C} }
  
 and reports it to the teacher
The teacher 
  
    
      
        T
      
    
    {\displaystyle T}
  
 then computes a set of strings and label them correctly according to 
  
    
      
        L
      
    
    {\displaystyle L}
  
, trying to make sure that the inference algorithm will compute 
  
    
      
        L
      
    
    {\displaystyle L}
  

The adversary can add correctly labeled words to the set in order to confuse the inference algorithm
The inference algorithm 
  
    
      
        I
      
    
    {\displaystyle I}
  
 gets the sample and computes a representation 
  
    
      
        R
        ∈
        
          R
        
      
    
    {\displaystyle R\in \mathbb {R} }
  
 consistent with the sample.
The goal is that when the inference algorithm receives a characteristic sample for a language 
  
    
      
        L
      
    
    {\displaystyle L}
  
, or a sample that subsumes a characteristic sample for 
  
    
      
        L
      
    
    {\displaystyle L}
  
, it will return a representation that recognizes exactly the language 
  
    
      
        L
      
    
    {\displaystyle L}
  
.


=== Sample ===
Sample 
  
    
      
        S
      
    
    {\displaystyle S}
  
 is a set of pairs of the form 
  
    
      
        (
        s
        ,
        l
        (
        s
        )
        )
      
    
    {\displaystyle (s,l(s))}
  
 such that 
  
    
      
        l
        (
        s
        )
        ∈
        {
        −
        1
        ,
        1
        }
      
    
    {\displaystyle l(s)\in \{-1,1\}}
  


==== Sample consistent with a language ====
We say that a sample 
  
    
      
        S
      
    
    {\displaystyle S}
  
 is consistent with language 
  
    
      
        L
      
    
    {\displaystyle L}
  
 if for every pair 
  
    
      
        (
        s
        ,
        l
        (
        s
        )
        )
      
    
    {\displaystyle (s,l(s))}
  
 in 
  
    
      
        S
      
    
    {\displaystyle S}
  
:

  
    
      
        l
        (
        s
        )
        =
        1
        
           if and only if 
        
        s
        ∈
        L
      
    
    {\displaystyle l(s)=1{\text{ if and only if }}s\in L}
  

  
    
      
        l
        (
        s
        )
        =
        −
        1
        
           if and only if 
        
        s
        ∉
        L
      
    
    {\displaystyle l(s)=-1{\text{ if and only if }}s\notin L}
  


=== Characteristic sample ===
Given an inference algorithm 
  
    
      
        I
      
    
    {\displaystyle I}
  
 and a language 
  
    
      
        L
      
    
    {\displaystyle L}
  
, a sample 
  
    
      
        S
      
    
    {\displaystyle S}
  
 that is consistent with 
  
    
      
        L
      
    
    {\displaystyle L}
  
 is called a characteristic sample of 
  
    
      
        L
      
    
    {\displaystyle L}
  
 for 
  
    
      
        I
      
    
    {\displaystyle I}
  
 if:

  
    
      
        I
      
    
    {\displaystyle I}
  
's output on 
  
    
      
        S
      
    
    {\displaystyle S}
  
 is a representation 
  
    
      
        R
      
    
    {\displaystyle R}
  
 that recognizes 
  
    
      
        L
      
    
    {\displaystyle L}
  
.
For every sample 
  
    
      
        D
      
    
    {\displaystyle D}
  
 that is consistent with 
  
    
      
        L
      
    
    {\displaystyle L}
  
 and also fulfils 
  
    
      
        S
        ⊆
        D
      
    
    {\displaystyle S\subseteq D}
  
, 
  
    
      
        I
      
    
    {\displaystyle I}
  
's output on 
  
    
      
        D
      
    
    {\displaystyle D}
  
 is a representation 
  
    
      
        R
      
    
    {\displaystyle R}
  
 that recognizes 
  
    
      
        L
      
    
    {\displaystyle L}
  
.
A Class of languages 
  
    
      
        
          C
        
      
    
    {\displaystyle \mathbb {C} }
  
 is said to have charistaristic samples if every 
  
    
      
        L
        ∈
        
          C
        
      
    
    {\displaystyle L\in \mathbb {C} }
  
 has a characteristic sample.


== Related Theorems ==


=== Theorem ===
If equivalence is undecidable for a class 
  
    
      
        
          C
        
      
    
    {\textstyle \mathbb {C} }
  
 over 
  
    
      
        Σ
      
    
    {\textstyle \Sigma }
  
 of cardinality bigger than 1, then 
  
    
      
        
          C
        
      
    
    {\textstyle \mathbb {C} }
  
 doesn't have characteristic samples.


==== Proof ====
Given a class of representations 
  
    
      
        
          C
        
      
    
    {\textstyle \mathbb {C} }
  
 such that equivalence is undecidable, for every polynomial 
  
    
      
        p
        (
        x
        )
      
    
    {\displaystyle p(x)}
  
 and every 
  
    
      
        n
        ∈
        
          N
        
      
    
    {\displaystyle n\in \mathbb {N} }
  
, there exist two representations 
  
    
      
        
          r
          
            1
          
        
      
    
    {\displaystyle r_{1}}
  
 and 
  
    
      
        
          r
          
            2
          
        
      
    
    {\displaystyle r_{2}}
  
 of sizes bounded by 
  
    
      
        n
      
    
    {\displaystyle n}
  
, that recognize different languages but are inseparable by any string of size bounded by 
  
    
      
        p
        (
        n
        )
      
    
    {\displaystyle p(n)}
  
. Assuming this is not the case, we can decide if 
  
    
      
        
          r
          
            1
          
        
      
    
    {\displaystyle r_{1}}
  
 and 
  
    
      
        
          r
          
            2
          
        
      
    
    {\displaystyle r_{2}}
  
 are equivalent by simulating their run on all strings of size smaller than 
  
    
      
        p
        (
        n
        )
      
    
    {\displaystyle p(n)}
  
, contradicting the assumption that equivalence is undecidable.


=== Theorem ===
If 
  
    
      
        
          S
          
            1
          
        
      
    
    {\displaystyle S_{1}}
  
 is a characteristic sample for 
  
    
      
        
          L
          
            1
          
        
      
    
    {\displaystyle L_{1}}
  
 and is also consistent with 
  
    
      
        
          L
          
            2
          
        
      
    
    {\displaystyle L_{2}}
  
, then every characteristic sample of 
  
    
      
        
          L
          
            2
          
        
      
    
    {\displaystyle L_{2}}
  
, is inconsistent with 
  
    
      
        
          L
          
            1
          
        
      
    
    {\displaystyle L_{1}}
  
.


==== Proof ====
Given a class 
  
    
      
        
          C
        
      
    
    {\textstyle \mathbb {C} }
  
 that has characteristic samples, let 
  
    
      
        
          R
          
            1
          
        
      
    
    {\displaystyle R_{1}}
  
 and 
  
    
      
        
          R
          
            2
          
        
      
    
    {\displaystyle R_{2}}
  
 be representations that recognize 
  
    
      
        
          L
          
            1
          
        
      
    
    {\displaystyle L_{1}}
  
 and 
  
    
      
        
          L
          
            2
          
        
      
    
    {\displaystyle L_{2}}
  
 respectively. Under the assumption that there is a characteristic sample for 
  
    
      
        
          L
          
            1
          
        
      
    
    {\displaystyle L_{1}}
  
, 
  
    
      
        
          S
          
            1
          
        
      
    
    {\displaystyle S_{1}}
  
 that is also consistent with 
  
    
      
        
          L
          
            2
          
        
      
    
    {\displaystyle L_{2}}
  
, we'll assume falsely that there exist a characteristic sample for 
  
    
      
        
          L
          
            2
          
        
      
    
    {\displaystyle L_{2}}
  
, 
  
    
      
        
          S
          
            2
          
        
      
    
    {\displaystyle S_{2}}
  
 that is consistent with 
  
    
      
        
          L
          
            1
          
        
      
    
    {\displaystyle L_{1}}
  
. By the definition of characteristic sample, the inference algorithm 
  
    
      
        I
      
    
    {\displaystyle I}
  
 must return a representation which recognizes the language if given a sample that subsumes the characteristic sample itself. But for the sample 
  
    
      
        
          S
          
            1
          
        
        ∪
        
          S
          
            2
          
        
      
    
    {\displaystyle S_{1}\cup S_{2}}
  
, the answer of the inferring algorithm needs to recognize both 
  
    
      
        
          L
          
            1
          
        
      
    
    {\displaystyle L_{1}}
  
 and 
  
    
      
        
          L
          
            2
          
        
      
    
    {\displaystyle L_{2}}
  
, in contradiction.


=== Theorem ===
If a class is polynomially learnable by example based queries, it is learnable with characteristic samples.


== Polynomialy characterizable classes ==


=== Regular languages ===
The proof that DFA's are learnable using characteristic samples, relies on the fact that every regular language has a finite number of equivalence classes with respect to the right congruence relation, 
  
    
      
        
          ∼
          
            L
          
        
      
    
    {\displaystyle \sim _{L}}
  
 (where 
  
    
      
        x
        
          ∼
          
            L
          
        
        y
      
    
    {\displaystyle x\sim _{L}y}
  
 for 
  
    
      
        x
        ,
        y
        ∈
        
          Σ
          
            ∗
          
        
      
    
    {\displaystyle x,y\in \Sigma ^{*}}
  
 if and only if 
  
    
      
        ∀
        z
        ∈
        
          Σ
          
            ∗
          
        
        :
        x
        z
        ∈
        L
        ↔
        y
        z
        ∈
        L
      
    
    {\displaystyle \forall z\in \Sigma ^{*}:xz\in L\leftrightarrow yz\in L}
  
). Note that if 
  
    
      
        x
      
    
    {\displaystyle x}
  
, 
  
    
      
        y
      
    
    {\displaystyle y}
  
 are not congruent with respect to 
  
    
      
        
          ∼
          
            L
          
        
      
    
    {\displaystyle \sim _{L}}
  
, there exists a string 
  
    
      
        z
      
    
    {\displaystyle z}
  
 such that 
  
    
      
        x
        z
        ∈
        L
      
    
    {\displaystyle xz\in L}
  
 but 
  
    
      
        y
        z
        ∉
        L
      
    
    {\displaystyle yz\notin L}
  
 or vice versa, this string is called a separating suffix.


==== Constructing a characteristic sample ====
The construction of a characteristic sample for a language 
  
    
      
        L
      
    
    {\displaystyle L}
  
 by the teacher goes as follows. Firstly, by running a depth first search on a deterministic automaton 
  
    
      
        A
      
    
    {\displaystyle A}
  
 recognizing 
  
    
      
        L
      
    
    {\displaystyle L}
  
, starting from its initial state, we get a suffix closed set of words, 
  
    
      
        W
      
    
    {\displaystyle W}
  
, ordered in shortlex order. From the fact above, we know that for every two states in the automaton, there exists a separating suffix that separates between every two strings that the run of 
  
    
      
        A
      
    
    {\displaystyle A}
  
 on them ends in the respective states. We refer to the set of separating suffixes as 
  
    
      
        S
      
    
    {\displaystyle S}
  
. The labeled set (sample) of words the teacher gives the adversary is 
  
    
      
        {
        (
        w
        ,
        l
        (
        w
        )
        )
        
          |
        
        w
        ∈
        W
        ⋅
        S
        ∪
        W
        ⋅
        Σ
        ⋅
        S
        }
      
    
    {\displaystyle \{(w,l(w))|w\in W\cdot S\cup W\cdot \Sigma \cdot S\}}
  
 where 
  
    
      
        l
        (
        w
        )
      
    
    {\displaystyle l(w)}
  
 is the correct label of 
  
    
      
        w
      
    
    {\displaystyle w}
  
 (whether it is in 
  
    
      
        L
      
    
    {\displaystyle L}
  
 or not). We may assume that 
  
    
      
        ϵ
        ∈
        S
      
    
    {\displaystyle \epsilon \in S}
  
.


==== Constructing a deterministic automata ====
Given the sample from the adversary 
  
    
      
        W
      
    
    {\displaystyle W}
  
, the construction of the automaton by the inference algorithm 
  
    
      
        I
      
    
    {\displaystyle I}
  
 starts with defining 
  
    
      
        P
        =
        
          prefix
        
        (
        W
        )
      
    
    {\displaystyle P={\text{prefix}}(W)}
  
 and 
  
    
      
        S
        =
        
          suffix
        
        (
        W
        )
      
    
    {\displaystyle S={\text{suffix}}(W)}
  
, which are the set of prefixes and suffixes of 
  
    
      
        W
      
    
    {\displaystyle W}
  
 respectively. Now the algorithm constructs a matrix 
  
    
      
        M
      
    
    {\displaystyle M}
  
 where the elements of 
  
    
      
        P
      
    
    {\displaystyle P}
  
 function as the rows, ordered by the shortlex order, and the elements of 
  
    
      
        S
      
    
    {\displaystyle S}
  
 function as the columns, ordered by the shortlex order. Next, the cells in the matrix are filled in the following manner for prefix 
  
    
      
        
          p
          
            i
          
        
      
    
    {\displaystyle p_{i}}
  
 and suffix 
  
    
      
        
          s
          
            j
          
        
      
    
    {\displaystyle s_{j}}
  
:

If 
  
    
      
        
          p
          
            i
          
        
        
          s
          
            j
          
        
        ∈
        W
        →
        
          M
          
            i
            j
          
        
        =
        l
        (
        
          p
          
            i
          
        
        
          s
          
            j
          
        
        )
      
    
    {\displaystyle p_{i}s_{j}\in W\rightarrow M_{ij}=l(p_{i}s_{j})}
  

else, 
  
    
      
        
          M
          
            i
            j
          
        
        =
        0
      
    
    {\displaystyle M_{ij}=0}
  

Now, we say row 
  
    
      
        i
      
    
    {\displaystyle i}
  
 and 
  
    
      
        t
      
    
    {\displaystyle t}
  
 are distinguishable if there exists an index 
  
    
      
        j
      
    
    {\displaystyle j}
  
 such that 
  
    
      
        
          M
          
            i
            j
          
        
        =
        −
        1
        ×
        
          M
          
            t
            j
          
        
      
    
    {\displaystyle M_{ij}=-1\times M_{tj}}
  
. The next stage of the inference algorithm is to construct the set 
  
    
      
        Q
      
    
    {\displaystyle Q}
  
 of distinguishable rows in 
  
    
      
        M
      
    
    {\displaystyle M}
  
, by initializing 
  
    
      
        Q
      
    
    {\displaystyle Q}
  
 with 
  
    
      
        ϵ
      
    
    {\displaystyle \epsilon }
  
 and iterating from the first row of 
  
    
      
        M
      
    
    {\displaystyle M}
  
 downwards and doing the following for row 
  
    
      
        
          r
          
            i
          
        
      
    
    {\displaystyle r_{i}}
  
:

If 
  
    
      
        
          r
          
            i
          
        
      
    
    {\displaystyle r_{i}}
  
 is distinguishable from all elements in 
  
    
      
        Q
      
    
    {\displaystyle Q}
  
, add it to 
  
    
      
        Q
      
    
    {\displaystyle Q}
  

else, pass on it to the next row
From the way the teacher constructed the sample it passed to the adversary, we know that for every 
  
    
      
        s
        ∈
        Q
      
    
    {\displaystyle s\in Q}
  
 and every 
  
    
      
        σ
        ∈
        Σ
      
    
    {\displaystyle \sigma \in \Sigma }
  
, the row 
  
    
      
        s
        σ
      
    
    {\displaystyle s\sigma }
  
 exists in 
  
    
      
        M
      
    
    {\displaystyle M}
  
, and from the construction of 
  
    
      
        Q
      
    
    {\displaystyle Q}
  
, there exists a row 
  
    
      
        
          s
          ′
        
        ∈
        Q
      
    
    {\displaystyle s'\in Q}
  
 such that 
  
    
      
        
          s
          ′
        
      
    
    {\displaystyle s'}
  
 and 
  
    
      
        s
        σ
      
    
    {\displaystyle s\sigma }
  
 are indistinguishable. The output automaton will be defined as follows:

The set of states is 
  
    
      
        Q
      
    
    {\displaystyle Q}
  
.
The initial state is the state corresponding to row 
  
    
      
        ϵ
        ∈
        Q
      
    
    {\displaystyle \epsilon \in Q}
  
.
The accepting states is the set 
  
    
      
        {
        s
        ∈
        Q
        
          |
        
        
           
        
        l
        (
        s
        )
        =
        1
        }
      
    
    {\displaystyle \{s\in Q|{\text{ }}l(s)=1\}}
  
.
The transitions function will be defined 
  
    
      
        δ
        (
        s
        ,
        σ
        )
        =
        
          s
          ′
        
      
    
    {\displaystyle \delta (s,\sigma )=s'}
  
, where 
  
    
      
        
          s
          ′
        
      
    
    {\displaystyle s'}
  
 is the element in 
  
    
      
        Q
      
    
    {\displaystyle Q}
  
 that is indistinguishable from 
  
    
      
        s
        σ
      
    
    {\displaystyle s\sigma }
  
.


=== Other polynomially characterizable classes ===
Class of languages recognizable by multiplicity automatons
Class of languages recognizable by tree automata
Class of languages recognizable by multiplicity tree automata
Class of languages recognizable by Fully-Ordered Lattice Automata
Class of languages recognizable by Visibly One-Counter Automata
Class of fully informative omega regular languages


== Non polynomially characterizable classes ==
There are some classes that do not have polynomially sized characteristic samples. For example, from the first theorem in the Related theorems segment, it has been shown that the following classes of languages do not have polynomial sized characteristic samples:

  
    
      
        
          C
          F
          G
        
      
    
    {\displaystyle \mathbb {CFG} }
  
 - The class of context-free grammars Languages over 
  
    
      
        Σ
      
    
    {\displaystyle \Sigma }
  
 of cardinality larger than 
  
    
      
        1
      
    
    {\displaystyle 1}
  

  
    
      
        
          L
          I
          N
          G
        
      
    
    {\displaystyle \mathbb {LING} }
  
 - The class of linear grammar languages over 
  
    
      
        Σ
      
    
    {\displaystyle \Sigma }
  
 of cardinality larger than 
  
    
      
        1
      
    
    {\displaystyle 1}
  

  
    
      
        
          S
          D
          G
        
      
    
    {\displaystyle \mathbb {SDG} }
  
 - The class of simple deterministic grammars Languages

  
    
      
        
          N
          F
          A
        
      
    
    {\displaystyle \mathbb {NFA} }
  
 - The class of nondeterministic finite automata Languages


== Relations to other learning paradigms ==
Classes of representations that has characteristic samples relates to the following learning paradigms:


=== Class of semi-poly teachable languages ===
A representation class 
  
    
      
        
          C
        
      
    
    {\displaystyle \mathbb {C} }
  
 is semi-poly 
  
    
      
        T
        
          /
        
        L
      
    
    {\displaystyle T/L}
  
 teachable if there exist 3 polynomials 
  
    
      
        p
        ,
        q
        ,
        r
      
    
    {\displaystyle p,q,r}
  
, a teacher 
  
    
      
        T
      
    
    {\displaystyle T}
  
 and an inference algorithm 
  
    
      
        I
      
    
    {\displaystyle I}
  
, such that for any adversary 
  
    
      
        A
      
    
    {\displaystyle A}
  
 the following holds:

  
    
      
        A
      
    
    {\displaystyle A}
  
 Selects a representation 
  
    
      
        R
      
    
    {\displaystyle R}
  
 of size 
  
    
      
        n
      
    
    {\displaystyle n}
  
 from 
  
    
      
        
          C
        
      
    
    {\displaystyle \mathbb {C} }
  

  
    
      
        T
      
    
    {\displaystyle T}
  
 computes a sample that is consistent with the language that 
  
    
      
        R
      
    
    {\displaystyle R}
  
 recognize, of size bounded by 
  
    
      
        p
        (
        n
        )
      
    
    {\displaystyle p(n)}
  
 and the strings in the sample bounded by length 
  
    
      
        q
        (
        n
        )
      
    
    {\displaystyle q(n)}
  

  
    
      
        A
      
    
    {\displaystyle A}
  
 adds correctly labeled strings to the sample computed by 
  
    
      
        T
      
    
    {\displaystyle T}
  
, making the new sample of size 
  
    
      
        m
      
    
    {\displaystyle m}
  

  
    
      
        I
      
    
    {\displaystyle I}
  
 then computes a representation equivalent to 
  
    
      
        R
      
    
    {\displaystyle R}
  
 in time bounded by 
  
    
      
        r
        (
        m
        )
      
    
    {\displaystyle r(m)}
  

The class of languages that there exists a polynomial algorithm that given a sample, returns a representation consistent with the sample is called consistency easy.


=== Polynomially characterizable languages ===
Given a representation class 
  
    
      
        
          R
        
      
    
    {\displaystyle \mathbb {R} }
  
, and 
  
    
      
        
          
            I
          
        
      
    
    {\displaystyle {\mathcal {I}}}
  
 a set of identification algorithms for 
  
    
      
        
          R
        
      
    
    {\displaystyle \mathbb {R} }
  
, 
  
    
      
        
          R
        
      
    
    {\displaystyle \mathbb {R} }
  
 is polynomially characterizable for 
  
    
      
        
          
            I
          
        
      
    
    {\displaystyle {\mathcal {I}}}
  
 if any 
  
    
      
        R
        ∈
        
          R
        
      
    
    {\displaystyle R\in \mathbb {R} }
  
 has a characteristic sample of size polynomial of 
  
    
      
        R
      
    
    {\displaystyle R}
  
's size, 
  
    
      
        S
      
    
    {\displaystyle S}
  
, that for every 
  
    
      
        I
        ∈
        
          
            I
          
        
      
    
    {\displaystyle I\in {\mathcal {I}}}
  
, 
  
    
      
        I
      
    
    {\displaystyle I}
  
's output on 
  
    
      
        S
      
    
    {\displaystyle S}
  
 is 
  
    
      
        R
      
    
    {\displaystyle R}
  
.


=== Releations between the paradigms ===


==== Theorem ====
A consistency-easy class 
  
    
      
        
          C
        
      
    
    {\displaystyle \mathbb {C} }
  
 has characteristic samples if and only if it is semi-poly 
  
    
      
        T
        
          /
        
        L
      
    
    {\displaystyle T/L}
  
 teachable.


===== Proof =====
Assuming 
  
    
      
        
          C
        
      
    
    {\displaystyle \mathbb {C} }
  
 has characteristic samples, then for every representation  
  
    
      
        R
        ∈
        
          C
        
      
    
    {\displaystyle R\in \mathbb {C} }
  
, its characteristic sample 
  
    
      
        S
      
    
    {\displaystyle S}
  
 holds the conditions for the sample computaed by the teacher, and the output of 
  
    
      
        I
      
    
    {\displaystyle I}
  
 on every sample 
  
    
      
        
          S
          ′
        
      
    
    {\displaystyle S'}
  
 such that 
  
    
      
        S
        ⊆
        
          S
          ′
        
      
    
    {\displaystyle S\subseteq S'}
  
 is equivalent to 
  
    
      
        R
      
    
    {\displaystyle R}
  
 from the definition of characteristic sample.
Assuming that 
  
    
      
        
          C
        
      
    
    {\displaystyle \mathbb {C} }
  
 is semi-poly 
  
    
      
        T
        
          /
        
        L
      
    
    {\displaystyle T/L}
  
 teachable, then for every representation 
  
    
      
        R
        ∈
        
          C
        
      
    
    {\displaystyle R\in \mathbb {C} }
  
, the computed sample by the teacher 
  
    
      
        S
      
    
    {\displaystyle S}
  
 is a characteristic sample for 
  
    
      
        R
      
    
    {\displaystyle R}
  
.


==== Theorem ====
If 
  
    
      
        
          C
        
      
    
    {\displaystyle \mathbb {C} }
  
 has characteristic sample, then 
  
    
      
        
          C
        
      
    
    {\displaystyle \mathbb {C} }
  
 is polynomially characterizable.


===== Proof =====
Assuming falsely that 
  
    
      
        
          C
        
      
    
    {\displaystyle \mathbb {C} }
  
 is not polynomially characterizable, there are two non equivalent representations 
  
    
      
        
          R
          
            1
          
        
        ,
        
          R
          
            2
          
        
        ∈
        
          C
        
      
    
    {\displaystyle R_{1},R_{2}\in \mathbb {C} }
  
, with characteristic samples 
  
    
      
        
          S
          
            1
          
        
      
    
    {\displaystyle S_{1}}
  
 and 
  
    
      
        
          S
          
            2
          
        
      
    
    {\displaystyle S_{2}}
  
 respectively. From the definition of characteristic samples, any inference algorithm 
  
    
      
        I
      
    
    {\displaystyle I}
  
 need to infer from the sample 
  
    
      
        
          S
          
            1
          
        
        ∪
        
          S
          
            2
          
        
      
    
    {\displaystyle S_{1}\cup S_{2}}
  
 a representation compatible with 
  
    
      
        
          R
          
            1
          
        
      
    
    {\displaystyle R_{1}}
  
 and 
  
    
      
        
          R
          
            2
          
        
      
    
    {\displaystyle R_{2}}
  
, in contradiction.


== See also ==
Grammar induction
Passive learning
Induction of regular languages
Deterministic finite automaton


== References ==