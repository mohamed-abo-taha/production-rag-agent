# Generalized additive model for location, scale and shape

Source: Wikipedia (https://en.wikipedia.org/wiki/Generalized_additive_model_for_location%2C_scale_and_shape)

The  generalized additive model for location, scale and shape (GAMLSS) is a distributional regression model in which a parametric statistical distribution is assumed for the response (target) variable but the parameters of this distribution can vary according to explanatory variables. Therefore the shape of this distribution for the target variable can change with explanatory variables.
GAMLSS is an input output model, i.e. 
  
    
      
        X
        →
        Y
      
    
    {\displaystyle X\rightarrow Y}
  
  but differs from the classical model in that the input X  affects the distribution of the target variable as a whole  not just the mean, i.e. 
  
    
      
        X
        →
        D
        (
        Y
        
          |
        
        X
        )
      
    
    {\displaystyle X\rightarrow D(Y|X)}
  
.
GAMLSS allows flexible regression by using smoothing or machine learning techniques to model the parameters of the target variable (response). GAMLSS assumes the response variable could follows any theoretical parametric distribution, which might be heavy or light-tailed, and positively or negatively skewed. In addition, all the parameters of the distribution which often are location (e.g., mean), scale (e.g., variance) and shape (skewness and kurtosis) – can be modelled as linear, nonlinear or using algorithm modelling functions of the explanatory variables. The distributional assumption for the target variables can be checked through diagnostic plots like Q–Q plot or worm plot. GAMLSS is a supervised machine learning model since the target value (the output) is always present.


== Overview of the model ==
The generalized additive model for location, scale and shape (GAMLSS) is a statistical model introduced  by Rigby and Stasinopoulos (2005) to overcome some of the limitations associated with the popular generalized linear models (GLMs) of Nelder and Wedderburn (1972) and generalized additive models (GAMs) of Hastie and Tibshirani. Most of the limitations arise from the limited choice of distributions for the response. Both GLM and GAM assumed that the response  comes from the   exponential family a family rich enough to allow continuous and discrete responses (and very good for modelling the mean of the distribution as a function of the explanatory variables) but not very flexible enough to model other characteristics of the distribution i.e tails.
In GAMLSS the exponential family distribution assumption for the response variable, (
  
    
      
        y
      
    
    {\displaystyle y}
  
), (essential in GLMs and GAMs), is relaxed and replaced by a general distribution family, including highly skew and/or kurtotic continuous and discrete distributions.
The systematic part of the model is expanded to allow modelling not only of the mean (or location) but possibly other parameters of the distribution of response as linear and/or nonlinear, parametric and/or additive non-parametric functions of explanatory variables and/or random effects.
GAMLSS, for continuous responses, is especially suited for modelling a leptokurtic or platykurtic and/or positively or negatively skewed variables therefor modelling the tails of the distribution. For count type response variable data it deals with over-dispersion and zero-inflation by using proper over-dispersed and zero inflated distributions. Heterogeneity also is dealt with by modeling the scale or shape parameters using explanatory variables.  GAMLSS allow also mixed distributions, that is, distributions which have discrete and continuous parts, i.e the zero inflated beta is one or them. Note that while the beta distribution allow value in   
  
    
      
        (
        0
        ,
        1
        )
      
    
    {\displaystyle (0,1)}
  
 the beta inflated allows values  in 
  
    
      
        [
        0
        ,
        1
        ]
      
    
    {\displaystyle [0,1]}
  
.
There are several packages written in R related to GAMLSS models,  and tutorials for using and interpreting GAMLSS.
A GAMLSS model assumes independent observations 
  
    
      
        
          y
          
            i
          
        
      
    
    {\displaystyle y_{i}}
  
 for 
  
    
      
        i
        =
        1
        ,
        2
        ,
        …
        ,
        n
      
    
    {\displaystyle i=1,2,\dots ,n}
  

with probability (density) function 
  
    
      
        D
        (
        
          y
          
            i
          
        
        
          |
        
        
          
            θ
          
          
            i
          
        
        )
      
    
    {\displaystyle D(y_{i}|{\boldsymbol {\theta }}_{i})}
  
 conditional on 
  
    
      
        
          
            θ
          
          
            i
          
        
      
    
    {\displaystyle {\boldsymbol {\theta }}_{i}}
  
.  The parameter  
  
    
      
        
          
            θ
          
          
            i
          
        
      
    
    {\displaystyle {\boldsymbol {\theta }}_{i}}
  
 often is a vector of four distribution parameters, 
  
    
      
        
          
            θ
          
          
            i
          
        
        =
        (
        
          μ
          
            i
          
        
        ,
        
          σ
          
            i
          
        
        ,
        
          ν
          
            i
          
        
        ,
        
          τ
          
            i
          
        
        )
      
    
    {\displaystyle {\boldsymbol {\theta }}_{i}=(\mu _{i},\sigma _{i},\nu _{i},\tau _{i})}
  
 each of which can be a function of the explanatory variables, for example, 
  
    
      
        σ
        =
        g
        (
        x
        )
      
    
    {\displaystyle \sigma =g(x)}
  
 The first two distribution parameters 
  
    
      
        
          μ
          
            i
          
        
      
    
    {\displaystyle \mu _{i}}
  
 and 
  
    
      
        
          σ
          
            i
          
        
      
    
    {\displaystyle \sigma _{i}}
  
 are usually characterised as location and scale parameters, while the remaining parameter(s), if any, are characterised as shape parameters, e.g. skewness and kurtosis parameters. The model may be applied more generally to the parameters of any population distribution.
The most general formulation of a GAMLSS model is

  
    
      
        
          
            
              
                
                  g
                  
                    1
                  
                
                (
                
                  
                    θ
                  
                  
                    1
                  
                
                )
              
              
                
                =
                
                  
                    η
                  
                  
                    1
                  
                
                =
                M
                L
                (
                
                  
                    
                      x
                    
                  
                  
                    j
                    1
                  
                
                )
              
            
            
              
                
                  g
                  
                    2
                  
                
                (
                
                  
                    θ
                  
                  
                    2
                  
                
                )
              
              
                
                =
                
                  
                    η
                  
                  
                    2
                  
                
                =
                M
                L
                (
                
                  
                    
                      x
                    
                  
                  
                    j
                    2
                  
                
                )
              
            
            
              
                …
              
              
                
                =
                …
                =
                …
              
            
            
              
                
                  g
                  
                    4
                  
                
                (
                
                  
                    θ
                  
                  
                    k
                  
                
                )
              
              
                
                =
                
                  
                    η
                  
                  
                    k
                  
                
                =
                M
                L
                (
                
                  
                    
                      x
                    
                  
                  
                    j
                    4
                  
                
                )
              
            
          
        
      
    
    {\displaystyle {\begin{aligned}g_{1}({\boldsymbol {\theta }}_{1})&={\boldsymbol {\eta }}_{1}=ML({\textbf {x}}_{j1})\\g_{2}({\boldsymbol {\theta }}_{2})&={\boldsymbol {\eta }}_{2}=ML({\textbf {x}}_{j2})\\\ldots &=\ldots =\ldots \\g_{4}({\boldsymbol {\theta }}_{k})&={\boldsymbol {\eta }}_{k}=ML({\textbf {x}}_{j4})\end{aligned}}}
  

where  
  
    
      
        M
        L
        (
        )
      
    
    {\displaystyle ML()}
  
 is any machine learning (mathematical or algorithmic) model and  
  
    
      
        k
      
    
    {\displaystyle k}
  
 is the number of parameters in the distribution for the response. The original formulation of GAMLSS in the 2005 RSS paper had only four parameters and it was written as;

  
    
      
        
          
            
              
                
                  g
                  
                    1
                  
                
                (
                
                  μ
                
                )
                =
                
                  
                    η
                  
                  
                    1
                  
                
                =
                
                  
                    
                      X
                    
                  
                  
                    1
                  
                
                
                  
                    β
                  
                  
                    1
                  
                
                +
                
                  ∑
                  
                    j
                    =
                    1
                  
                  
                    
                      J
                      
                        1
                      
                    
                  
                
                
                  
                    h
                  
                  
                    j
                    1
                  
                
                (
                
                  
                    
                      
                        x
                      
                      
                        j
                        1
                      
                    
                    )
                  
                
              
            
            
              
                
                  g
                  
                    2
                  
                
                (
                
                  σ
                
                )
                =
                
                  
                    η
                  
                  
                    2
                  
                
                =
                
                  
                    
                      X
                    
                  
                  
                    2
                  
                
                
                  
                    β
                  
                  
                    2
                  
                
                +
                
                  ∑
                  
                    j
                    =
                    1
                  
                  
                    
                      J
                      
                        2
                      
                    
                  
                
                
                  
                    h
                  
                  
                    j
                    2
                  
                
                (
                
                  
                    
                      
                        x
                      
                      
                        j
                        2
                      
                    
                    )
                  
                
              
            
            
              
                
                  g
                  
                    3
                  
                
                (
                
                  ν
                
                =
                
                  
                    η
                  
                  
                    3
                  
                
                =
                
                  
                    
                      X
                    
                  
                  
                    3
                  
                
                
                  
                    β
                  
                  
                    3
                  
                
                +
                
                  ∑
                  
                    j
                    =
                    1
                  
                  
                    
                      J
                      
                        3
                      
                    
                  
                
                
                  
                    h
                  
                  
                    j
                    3
                  
                
                (
                
                  
                    
                      
                        x
                      
                      
                        j
                        3
                      
                    
                    )
                  
                
              
            
            
              
                
                  g
                  
                    4
                  
                
                (
                
                  τ
                
                )
                =
                
                  
                    η
                  
                  
                    4
                  
                
                =
                
                  
                    
                      X
                    
                  
                  
                    4
                  
                
                
                  
                    β
                  
                  
                    4
                  
                
                +
                
                  ∑
                  
                    j
                    =
                    1
                  
                  
                    
                      J
                      
                        4
                      
                    
                  
                
                
                  
                    h
                  
                  
                    j
                    4
                  
                
                (
                
                  
                    
                      
                        x
                      
                      
                        j
                        4
                      
                    
                    )
                  
                
              
            
          
        
      
    
    {\displaystyle {\begin{aligned}g_{1}({\boldsymbol {\mu }})={\boldsymbol {\eta }}_{1}={\textbf {X}}_{1}{\boldsymbol {\beta }}_{1}+\sum _{j=1}^{J_{1}}{h}_{j1}({\bf {{x}_{j1})}}\\g_{2}({\boldsymbol {\sigma }})={\boldsymbol {\eta }}_{2}={\textbf {X}}_{2}{\boldsymbol {\beta }}_{2}+\sum _{j=1}^{J_{2}}{h}_{j2}({\bf {{x}_{j2})}}\\g_{3}({\boldsymbol {\nu }}={\boldsymbol {\eta }}_{3}={\textbf {X}}_{3}{\boldsymbol {\beta }}_{3}+\sum _{j=1}^{J_{3}}{h}_{j3}({\bf {{x}_{j3})}}\\g_{4}({\boldsymbol {\tau }})={\boldsymbol {\eta }}_{4}={\textbf {X}}_{4}{\boldsymbol {\beta }}_{4}+\sum _{j=1}^{J_{4}}{h}_{j4}({\bf {{x}_{j4})}}\end{aligned}}}
  

where 
  
    
      
        
          μ
        
        ,
        
          σ
        
        ,
        
          ν
        
      
    
    {\displaystyle {\boldsymbol {\mu }},{\boldsymbol {\sigma }},{\boldsymbol {\nu }}}
  
, 
  
    
      
        
          τ
        
      
    
    {\displaystyle {\boldsymbol {\tau }}}
  
  and 
  
    
      
        
          
            η
          
          
            k
          
        
      
    
    {\displaystyle {\boldsymbol {\eta }}_{k}}
  
 are vectors of length 
  
    
      
        n
      
    
    {\displaystyle n}
  
, 
  
    
      
        
          
            β
          
          
            k
          
          
            T
          
        
        =
        (
        
          β
          
            1
            k
          
        
        ,
        
          β
          
            2
            k
          
        
        ,
        …
        ,
        
          β
          
            
              J
              
                k
              
              ′
            
            k
          
        
        )
      
    
    {\displaystyle {\boldsymbol {\beta }}_{k}^{T}=(\beta _{1k},\beta _{2k},\ldots ,\beta _{J'_{k}k})}
  
 is a parameter vector of length 
  
    
      
        
          J
          
            k
          
          ′
        
      
    
    {\displaystyle J'_{k}}
  
, 
  
    
      
        
          
             
            
              
                X
              
              
                k
              
            
          
        
      
    
    {\displaystyle {\bf {~{X}_{k}}}}
  
 is a fixed known design matrix of order 
  
    
      
        n
        ×
        
          J
          
            k
          
          ′
        
      
    
    {\displaystyle n\times J'_{k}}
  
 and 
  
    
      
        
          h
          
            j
            k
          
        
      
    
    {\displaystyle h_{jk}}
  
 is a smooth non-parametric function of explanatory variable 
  
    
      
        
          
            
              
                x
              
              
                j
                k
              
            
          
        
      
    
    {\displaystyle {\bf {{x}_{jk}}}}
  
, for 
  
    
      
        j
        =
        1
        ,
        2
        ,
        …
        ,
        
          J
          
            k
          
        
      
    
    {\displaystyle j=1,2,\ldots ,J_{k}}
  
 and 
  
    
      
        k
        =
        1
        ,
        2
        ,
        3
        ,
        4
      
    
    {\displaystyle k=1,2,3,4}
  
.

  
    
      
        
          g
          
            k
          
        
      
    
    {\displaystyle g_{k}}
  
 for 
  
    
      
        k
        =
        1
        ,
        2
        ,
        3
        ,
        4
      
    
    {\displaystyle k=1,2,3,4}
  
 are link functions to ensure that the parameter are in the correct range of values.


== Applications of the model ==
For centile estimation, the WHO Multicentre Growth Reference Study Group have recommended GAMLSS and the Box–Cox power exponential (BCPE) distributions for the construction of the WHO Child Growth Standards. Recent studies have used GAMLSS to predict the probability of cyanobacterial toxins exceeding critical health thresholds in lakes, as well as in applications related to remote sensing, biogeochemical modeling and medicine.


== What distributions can be used ==
The form of the distribution assumed for the response variable y, is very general. For example, an implementation of GAMLSS in R has around 100 different distributions available. Such implementations also allow use of truncated distributions and censored (or interval) response variables.


== References ==


== Further reading ==
Beyerlein, A.; Fahrmeir, L.; Mansmann, U.; Toschke, A. M. (2001). "Alternative regression models to assess increase in childhood BM". BMC Medical Research Methodology. 8: 59. doi:10.1186/1471-2288-8-59. PMC 2543035. PMID 18778466.
Cole, T. J., Stanojevic, S., Stocks, J., Coates, A. L., Hankinson, J. L., Wade, A. M. (2009), "Age- and size-related reference ranges: A case study of spirometry through childhood and adulthood", Statistics in Medicine, 28(5), 880–898.Link
Fenske, N., Fahrmeir, L., Rzehak, P., Hohle, M. (25 September 2008), "Detection of risk factors for obesity in early childhood with quantile regression methods for longitudinal data", Department of Statistics: Technical Reports, No.38 Link
Hudson, I. L., Kim, S. W., Keatley, M. R.  (2010), "Climatic Influences on the Flowering Phenology of Four Eucalypts: A GAMLSS Approach Phenological Research". In Phenological Research, Irene L. Hudson and Marie R. Keatley (eds), Springer Netherlands Link
Hudson, I. L., Rea, A., Dalrymple, M. L., Eilers, P. H. C. (2008), "Climate impacts on sudden infant death syndrome: a GAMLSS approach", Proceedings of the 23rd international workshop on statistical modelling pp. 277–280. Link
Nott, D (2006). "Semiparametric estimation of mean and variance functions for non-Gaussian data". Computational Statistics. 21 (3–4): 603–620. CiteSeerX 10.1.1.117.6518. doi:10.1007/s00180-006-0017-9. S2CID 16900583.
Serinaldi, F (2011). "Distributional modeling and short-term forecasting of electricity prices by Generalized Additive Models for Location, Scale and Shape". Energy Economics. 33 (6): 1216–1226. doi:10.1016/j.eneco.2011.05.001.
Serinaldi, F.; Cuomo, G. (2011). "Characterizing impulsive wave-in-deck loads on coastal bridges by probabilistic models of impact maxima and rise times". Coastal Engineering. 58 (9): 908–926. doi:10.1016/j.coastaleng.2011.05.010.
Serinaldi, F., Villarini, G., Smith, J. A., Krajewski, W. F. (2008), "Change-Point and Trend Analysis on Annual Maximum Discharge in Continental United States", American Geophysical Union Fall Meeting 2008, abstract #H21A-0803*
van Ogtrop, F. F.; Vervoort, R. W.; Heller, G. Z.; Stasinopoulos, D. M.; Rigby, R. A. (2011). "Long-range forecasting of intermittent streamflow". Hydrology and Earth System Sciences Discussions. 8 (1): 681–713. doi:10.5194/hessd-8-681-2011.
Villarini, G.; Serinaldi, F. (2011). "Development of statistical models for at-site probabilistic seasonal rainfall forecast". International Journal of Climatology. 32 (14): 2197–2212. doi:10.1002/joc.3393.
Villarini, G.; Serinaldi, F.; Smith, J. A.; Krajewski, W. F. (2009). "On the stationarity of annual flood peaks in the continental United States during the 20th century". Water Resources Research. 45 (8). Bibcode:2009WRR....45.8417V. doi:10.1029/2008wr007645. Archived from the original on 6 June 2011. Retrieved 27 May 2010.
Villarini, G.; Smith, J. A.; Napolitano, F. (2010). "Nonstationary modeling of a long record of rainfall and temperature over Rome". Advances in Water Resources. 33 (10): 1256–1267. Bibcode:2010AdWR...33.1256V. doi:10.1016/j.advwatres.2010.03.013.


== External links ==
GAMLSS official website gamlss.org
GAMLSS universe
GAMLLS BOOK 1; Flexible Regression and Smoothing
GAMLSS BOOK 2; Distributions for Modeling Location, Scale, and Shape
GAMLSS BOOK 3; Generalized Additive Models for Location, Scale and Shape