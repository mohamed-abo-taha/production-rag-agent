# Targeted maximum likelihood estimation

Source: Wikipedia (https://en.wikipedia.org/wiki/Targeted_maximum_likelihood_estimation)

Targeted Maximum Likelihood Estimation (TMLE) (also more accurately referred to as Targeted Minimum Loss-Based Estimation) is a general statistical estimation framework for causal inference and semiparametric models. TMLE combines ideas from maximum likelihood estimation, semiparametric efficiency theory, and machine learning. It was introduced by Mark J. van der Laan and colleagues in the mid-2000s as a method that yields asymptotically efficient plug-in estimators while allowing the use of flexible, data-adaptive algorithms such as ensemble machine learning for nuisance parameter estimation.
TMLE is used in epidemiology, biostatistics, and the social sciences to estimate causal effects in observational and experimental studies. Applications of TMLE include Longitudinal TMLE (LTMLE) for time-varying treatments and confounders. Variations in how the targeting step in TMLE is carried out have resulted in various versions of TMLE such as  Collaborative TMLE (CTMLE)  and Adaptive TMLE for improved finite-sample performance and automated variable selection.


== History ==
The TMLE framework was first described by van der Laan and Rubin (2006) as a general approach for the construction of efficient plug-in estimators of smooth features of the data density. It was demonstrated in the context of causal inference and missing data problems. It was developed to address limitations of traditional doubly robust methods, such as Augmented Inverse Probability Weighting (AIPW), by respecting the plug-in principle in the sense that it respects that the target parameter is a function of the data density that is an element of the statistical model. TMLE estimates the data density or relevant parts of it with machine learning and targets these machine learning fits before it is plugged in the target parameter mapping. In this manner, a TMLE always respects global knowledge and satisfies known bounds such as that the target parameter is a probability .
Since its introduction, TMLE has been developed in a series of theoretical and applied papers, culminating in book-length treatments of the method and its applications to survival analysis, adaptive designs, and longitudinal data.


== Methodology ==
At its core, TMLE is a two-step estimation procedure:

Initial estimation: Machine learning methods (such as the Super Learner ensemble) are used to obtain flexible estimates of nuisance parameters, such as outcome regressions and propensity scores.
Targeting step: The initial estimate is updated by solving a score equation (the efficient influence function) so that the final estimator is consistent, asymptotically normal, and efficient under mild regularity conditions. The targeted machine learning fit is then mapped into the corresponding estimator of the target parameter by simply plugging it in the target parameter mapping.
This approach balances the bias–variance trade-off by combining data-adaptive estimation with semiparametric efficiency theory. TMLE is doubly robust, meaning it remains consistent if either the outcome model or the treatment model is consistently estimated.


=== Formula ===
Here we explain the TMLE of the average treatment effect of a binary treatment on an outcome adjusting for baseline covariates. Consider i.i.d. observations 
  
    
      
        
          O
          
            i
          
        
        =
        (
        
          W
          
            i
          
        
        ,
        
          A
          
            i
          
        
        ,
        
          Y
          
            i
          
        
        )
      
    
    {\displaystyle O_{i}=(W_{i},A_{i},Y_{i})}
  
 from a distribution 
  
    
      
        
          P
          
            0
          
        
      
    
    {\displaystyle P_{0}}
  
, where 
  
    
      
        W
      
    
    {\displaystyle W}
  
 are baseline covariates, 
  
    
      
        A
      
    
    {\displaystyle A}
  
 is a binary treatment, and 
  
    
      
        Y
      
    
    {\displaystyle Y}
  
 is an outcome. Let 
  
    
      
        
          
            
              Q
              ¯
            
          
        
        (
        a
        ,
        w
        )
        =
        
          E
        
        [
        Y
        ∣
        A
        =
        a
        ,
        W
        =
        w
        ]
      
    
    {\displaystyle {\bar {Q}}(a,w)=\mathbb {E} [Y\mid A=a,W=w]}
  
 represent the outcome model and 
  
    
      
        g
        (
        a
        ∣
        w
        )
        =
        P
        (
        A
        =
        a
        ∣
        W
        =
        w
        )
      
    
    {\displaystyle g(a\mid w)=P(A=a\mid W=w)}
  
 represent the propensity score. 
The average treatment effect (ATE) is given by 
  
    
      
        
          ψ
          
            0
          
        
        =
        
          E
        
        {
        
          
            
              Q
              ¯
            
          
        
        (
        1
        ,
        W
        )
        −
        
          
            
              Q
              ¯
            
          
        
        (
        0
        ,
        W
        )
        }
        .
      
    
    {\displaystyle \psi _{0}=\mathbb {E} \{{\bar {Q}}(1,W)-{\bar {Q}}(0,W)\}.}
  

A basic TMLE for the ATE proceeds as follows:
Step 1: Estimate initial models. Obtain estimates 
  
    
      
        
          
            
              
                
                  Q
                  ¯
                
              
              ^
            
          
        
        (
        a
        ,
        w
        )
      
    
    {\displaystyle {\hat {\bar {Q}}}(a,w)}
  
 and 
  
    
      
        
          
            
              g
              ^
            
          
        
        (
        a
        ∣
        w
        )
      
    
    {\displaystyle {\hat {g}}(a\mid w)}
  
, often using flexible methods such as Super Learner.
Step 2: Compute the clever covariate. Define:

  
    
      
        H
        (
        A
        ,
        W
        )
        =
        
          
            A
            
              
                
                  
                    g
                    ^
                  
                
              
              (
              1
              ∣
              W
              )
            
          
        
        −
        
          
            
              1
              −
              A
            
            
              
                
                  
                    g
                    ^
                  
                
              
              (
              0
              ∣
              W
              )
            
          
        
        .
      
    
    {\displaystyle H(A,W)={\frac {A}{{\hat {g}}(1\mid W)}}-{\frac {1-A}{{\hat {g}}(0\mid W)}}.}
  

Step 3: Estimate the fluctuation parameter. Fit a logistic regression of 
  
    
      
        Y
      
    
    {\displaystyle Y}
  
 on 
  
    
      
        H
        (
        A
        ,
        W
        )
      
    
    {\displaystyle H(A,W)}
  
 with 
  
    
      
        logit
        ⁡
        (
        
          
            
              
                
                  Q
                  ¯
                
              
              ^
            
          
        
        (
        A
        ,
        W
        )
        )
      
    
    {\displaystyle \operatorname {logit} ({\hat {\bar {Q}}}(A,W))}
  
 as offset. This yields 
  
    
      
        
          
            
              ε
              ^
            
          
        
      
    
    {\displaystyle {\hat {\varepsilon }}}
  
, the MLE that solves the score equation:

  
    
      
        
          
            1
            n
          
        
        
          ∑
          
            i
            =
            1
          
          
            n
          
        
        H
        (
        
          A
          
            i
          
        
        ,
        
          W
          
            i
          
        
        )
        
          
            {
          
        
        
          Y
          
            i
          
        
        −
        
          
            
              
                
                  
                    Q
                    ¯
                  
                
                ^
              
            
          
          
            ε
          
        
        (
        
          A
          
            i
          
        
        ,
        
          W
          
            i
          
        
        )
        
          
            }
          
        
        =
        0.
      
    
    {\displaystyle {\frac {1}{n}}\sum _{i=1}^{n}H(A_{i},W_{i}){\big \{}Y_{i}-{\hat {\bar {Q}}}^{\varepsilon }(A_{i},W_{i}){\big \}}=0.}
  

Step 4: Update the initial estimate. Apply the "blip" to obtain the targeted estimate:
  
    
      
        
          
            
              
                
                  
                    Q
                    ¯
                  
                
                ^
              
            
          
          
            ∗
          
        
        (
        A
        ,
        W
        )
        =
        expit
        ⁡
        
          
            (
          
        
        logit
        ⁡
        
          
            (
          
        
        
          
            
              
                
                  Q
                  ¯
                
              
              ^
            
          
        
        (
        A
        ,
        W
        )
        
          
            )
          
        
        +
        
          
            
              ε
              ^
            
          
        
        
        H
        (
        A
        ,
        W
        )
        
          
            )
          
        
        .
      
    
    {\displaystyle {\hat {\bar {Q}}}^{*}(A,W)=\operatorname {expit} {\Big (}\operatorname {logit} {\big (}{\hat {\bar {Q}}}(A,W){\big )}+{\hat {\varepsilon }}\,H(A,W){\Big )}.}
  

Step 5: Compute the TMLE. The ATE estimate is:

  
    
      
        
          
            
              
                ψ
                ^
              
            
          
          
            TMLE
          
        
        =
        
          
            1
            n
          
        
        
          ∑
          
            i
            =
            1
          
          
            n
          
        
        
          
            [
          
        
        
          
            
              
                
                  
                    Q
                    ¯
                  
                
                ^
              
            
          
          
            ∗
          
        
        (
        1
        ,
        
          W
          
            i
          
        
        )
        −
        
          
            
              
                
                  
                    Q
                    ¯
                  
                
                ^
              
            
          
          
            ∗
          
        
        (
        0
        ,
        
          W
          
            i
          
        
        )
        
          
            ]
          
        
        .
      
    
    {\displaystyle {\hat {\psi }}_{\text{TMLE}}={\frac {1}{n}}\sum _{i=1}^{n}{\big [}{\hat {\bar {Q}}}^{*}(1,W_{i})-{\hat {\bar {Q}}}^{*}(0,W_{i}){\big ]}.}
  

Inference. The efficient influence function (EIF) for the ATE is:

  
    
      
        
          D
          
            ∗
          
        
        (
        O
        )
        =
        H
        (
        A
        ,
        W
        )
        {
        Y
        −
        
          
            
              
                Q
                ¯
              
            
          
          
            ∗
          
        
        (
        A
        ,
        W
        )
        }
        +
        
          
            
              
                Q
                ¯
              
            
          
          
            ∗
          
        
        (
        1
        ,
        W
        )
        −
        
          
            
              
                Q
                ¯
              
            
          
          
            ∗
          
        
        (
        0
        ,
        W
        )
        −
        ψ
        .
      
    
    {\displaystyle D^{*}(O)=H(A,W)\{Y-{\bar {Q}}^{*}(A,W)\}+{\bar {Q}}^{*}(1,W)-{\bar {Q}}^{*}(0,W)-\psi .}
  

The variance is estimated by 
  
    
      
        
          
            
              
                σ
                ^
              
            
          
          
            2
          
        
        =
        
          n
          
            −
            1
          
        
        
          ∑
          
            i
            =
            1
          
          
            n
          
        
        
          
            (
          
        
        
          D
          
            ∗
          
        
        (
        
          O
          
            i
          
        
        )
        
          
            
              )
            
          
          
            2
          
        
      
    
    {\displaystyle {\hat {\sigma }}^{2}=n^{-1}\sum _{i=1}^{n}{\big (}D^{*}(O_{i}){\big )}^{2}}
  
, yielding Wald-type confidence intervals 
  
    
      
        
          
            
              
                ψ
                ^
              
            
          
          
            TMLE
          
        
        ±
        
          z
          
            1
            −
            α
            
              /
            
            2
          
        
        
        
          
            
              σ
              ^
            
          
        
        
          /
        
        
          
            n
          
        
      
    
    {\displaystyle {\hat {\psi }}_{\text{TMLE}}\pm z_{1-\alpha /2}\,{\hat {\sigma }}/{\sqrt {n}}}
  
.
Remark. For continuous outcomes, a linear fluctuation 
  
    
      
        
          
            
              
                
                  
                    Q
                    ¯
                  
                
                ^
              
            
          
          
            ∗
          
        
        =
        
          
            
              
                
                  Q
                  ¯
                
              
              ^
            
          
        
        +
        
          
            
              ε
              ^
            
          
        
        
        H
      
    
    {\displaystyle {\hat {\bar {Q}}}^{*}={\hat {\bar {Q}}}+{\hat {\varepsilon }}\,H}
  
 may be used instead. For bounded continuous outcomes, the logistic fluctuation (after rescaling 
  
    
      
        Y
      
    
    {\displaystyle Y}
  
 to 
  
    
      
        [
        0
        ,
        1
        ]
      
    
    {\displaystyle [0,1]}
  
) is often preferred for improved finite-sample performance.


== Applications ==
TMLE has been applied in:

Epidemiology: Estimating causal effects of exposures and interventions in observational cohort studies.
Clinical trials and real-world evidence: The Targeted Learning roadmap provides a structured framework for generating and validating real-world evidence (RWE), bridging randomized trials and observational data using TMLE and related estimation techniques. This approach enables transparency, sensitivity analysis, and stronger causal inference for regulatory and clinical trial contexts.
High-dimensional settings: Integration with ensemble methods for causal effect estimation. TMLE has been successfully applied in pharmacoepidemiology where a large number of covariates are automatically selected to adjust for confounding. In a study of post–myocardial infarction statin use and 1-year mortality, TMLE demonstrated robust performance relative to inverse probability weighting in scenarios with hundreds of potential confounders.


== Derivatives and extensions ==
Longitudinal TMLE (LTMLE): A methodological extension of TMLE for longitudinal data with time-varying treatments, confounders, and censoring. It allows the estimation of dynamic treatment regimes and intervention-specific causal effects over time. This framework was originally introduced by van der Laan & Gruber (2012).
Collaborative TMLE (CTMLE): Enhances finite-sample performance and variable selection by collaboratively fitting the treatment mechanism in conjunction with the target parameter.


== Software ==
Several R packages implement TMLE and related methods:

tmle: Functions for binary, categorical, and continuous outcomes.
ltmle: Implementation for longitudinal data with time-varying treatments and outcomes.
ctmle: Algorithms for collaborative TMLE and adaptive variable selection.
SuperLearner: A theoretically grounded, cross-validated ensemble learning method that combines predictions from multiple algorithms to minimize predictive risk. Widely used in TMLE for estimating nuisance parameters. The original implementation is available as the R package SuperLearner.   Recent machine learning platforms like H2O AutoML implement similar ensemble strategies, combining diverse learners in parallel and leveraging stacking and blending techniques, effectively functioning as a large-scale Super Learner.


== See also ==
Causal inference


== References ==