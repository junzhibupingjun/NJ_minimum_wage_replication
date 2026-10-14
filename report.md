## Empirical Report: Replication of Card & Krueger (1994)

1. **Research Question and Motivation**
This project replicates Card & Krueger (1994), which investigates the employment effect of a minimum wage increase. The central question is how employers respond to a binding minimum wage. Traditional competitive theory predicts employment losses. The paper uses a natural experiment (New Jersey's minimum wage rise from $4.25 to $5.05 in April 1992) with eastern Pennsylvania as the control group.

2. **Data and Variables**
**2.1 Data Source and Sample Construction**
This analysis uses the Princeton public replication dataset, containing store-level survey data from 410 fast-food restaurants across New Jersey (NJ) and eastern Pennsylvania (PA). The data includes two waves: Wave 1 (February–March 1992), collected before the minimum wage increase, and Wave 2 (November–December 1992), collected about eight months after. The sample consists of four major chains: Burger King, KFC, Roy Rogers, and Wendy’s.
To construct the final analysis sample, we carefully handle missing values and store closures. We restrict the baseline employment regressions to 357 stores with valid employment and wage data in both waves. For the price extension, the sample is further restricted to 339 stores with complete price data. Stores that permanently closed by Wave 2 are retained in the sample with their Wave 2 employment set to zero to avoid survivorship bias. Stores temporarily closed (e.g., due to renovation or fire) are treated as missing in the baseline but set to zero in robustness checks.

**2.2 Variable Definitions**
Dependent Variable: Full-time equivalent (FTE) employment is calculated as the number of full-time employees plus managers plus 0.5 times the number of part-time employees. This weighting reflects the fact that part-time workers contribute roughly half the labor input of full-time workers. The change in employment is defined as ΔFTE = FTE_2 - FTE_1.
Core Independent Variables: The NJ dummy equals 1 for New Jersey stores and 0 for Pennsylvania stores. The wage gap variable is defined as gap = (5.05 - wage_st) / wage_st for NJ stores initially paying less than $5.05, and 0 otherwise. This variable measures the proportional wage increase required for a store to comply with the new minimum wage, capturing treatment intensity.
Controls: We include chain dummies (Burger King, KFC, Roy Rogers; Wendy’s as baseline), a company-owned indicator (co_owned), and region dummies (southj, centralj, pa1, pa2) to absorb regional demand shocks.
Extension Variables: For the price pass-through analysis, the outcome is the change in full meal price, defined as Δprice = Δ(psoda + pfry + pentree).

**2.3 Data Cleaning Decisions**
Several data choices are motivated by economic reasoning. First, using FTE rather than simple headcounts prevents bias from changes in the full-time/part-time composition. Second, the gap variable is preferred over a simple NJ dummy because it exploits within-state variation: stores initially paying $4.25 were severely affected, while those paying above $5.05 were largely unaffected. Third, region dummies are included to control for local economic conditions that might differentially affect NJ and PA.

3. **Empirical Design**
**3.1 Identification Strategy**
We employ a Difference-in-Differences (DiD) framework, exploiting the April 1992 minimum wage increase in NJ as a natural experiment. NJ serves as the treatment group, while PA (where the minimum wage remained at $4.25) serves as the control group. The identifying assumption is parallel trends: absent the minimum wage increase, employment and prices in NJ and PA would have followed similar trajectories. Although the two-wave structure precludes a formal event-study test, the similarity of baseline wages and employment across states supports this assumption.

**3.2 Model Specification**
The baseline models are estimated as:
$\Delta E_i = a + bX_i + c \cdot NJ_i + \varepsilon_i$ 
and
$\Delta E_i = a' + b'X_i + c' \cdot GAP_i + \varepsilon_i'$
where Xi includes chain and ownership controls. Model 1 estimates the average treatment effect using the NJ dummy, while Model 2 uses the continuous GAP variable to test for a dose-response relationship. In extended specifications, we add region dummies to isolate the effect of the minimum wage by comparing high- and low-wage stores within the same region. 

4. **Core Replication Results**
**4.1 Table 2**
Table 2 reports the means of key variables. In Wave 1, NJ FTE employment(20.44) was lower than PA(23.33), while starting wages were similar (4.61 and 4.63 respectively). By Wave 2, NJ starting wages rose to 5.08, with 85.5% of stores paying exactly $5.05, while PA remained at 4.62. Employment changed little, which increased 0.14, suggesting no negative employment effect.
In the comparison with the original paper, the t-statistics for the last three rows of Wave 2 are very close. For the price of a full meal, the original paper reports a t-statistic of 5.0, while our replication yields 5.08. For hours open, the paper reports -0.8, and our result is -0.65. For the recruiting bonus, the paper reports -0.6, and our result is -0.57. These minor differences are consistent with the small numerical discrepancies between the public-use dataset and the published data, as well as rounding in the standard error calculations. They do not affect any qualitative conclusions.
The remaining minor discrepancies are likely driven by differences in the dataset versions and sample sizes. The publicly available Card & Krueger dataset contains slight variations in a small number of observations compared to the final published data. Specifically, the number of valid observations or the treatment of missing values may differ, which slightly shifts the calculated means and standard errors. This explains the small gap in the Wave 1 FTE employment mean and the slightly larger standard errors. Furthermore, differences in statistical software in handling floating-point precision and missing values can also contribute to these minor numerical differences. However, these discrepancies are economically trivial and do not alter the main conclusion of no negative employment effect.

**4.2 Table 3**
Table 3 reports average FTE employment before and after the policy change. The key result is the difference-in-differences estimate: the change in mean FTE employment for NJ minus PA is +2.75 (SE = 1.31), which is almost identical to the original paper's +2.76. This positive point estimate suggests that employment actually increased in NJ relative to PA after the minimum wage hike. Within NJ, low-wage stores (initially paying $4.25) gained 1.32 FTE workers, while high-wage stores (paying $5.00 or more) lost 2.04 FTE workers. The difference between low-wage and high-wage stores is +3.36 (SE = 1.26), again matching the paper's +3.36 and further indicating no negative employment effect.
The main limitation of this replication is the well-documented discrepancy between the public-use dataset and the published paper, which explains minor numerical differences such as the Wave 1 FTE mean (20.44 vs. 20.4). However, these discrepancies are economically trivial and do not alter any qualitative conclusions. 

**4.3 Table 4**
Table 4 presents the reduced-form regression models for the change in FTE employment. Models (i) and (ii) use the New Jersey dummy, while models (iii)–(v) use the proportional wage gap (gap). Across all specifications, the coefficients on both nj and gap are positive. In models (i) and (ii), the New Jersey dummy is positive and statistically significant at the 5% level. Similarly, in models (iii) and (iv), the gap variable is also positive and significant. However, once regional dummies are added in model (v), the coefficient on gap shrinks to 12.03 and becomes statistically insignificant. This pattern suggests that while there is no negative employment effect, the positive estimate may partly reflect unobserved regional economic conditions rather than the minimum wage itself.
These estimates closely mirror the original paper. For the New Jersey dummy, our estimates are 2.36 (SE = 1.15) and 2.33 (SE = 1.15), compared to the paper's 2.33 (SE = 1.19) and 2.30 (SE = 1.20). Similarly, for the gap variable, our estimates are 15.89 (SE = 5.95), 15.19 (SE = 6.08), and 12.03 (SE = 7.32), compared to the paper's 15.65 (SE = 6.08), 14.92 (SE = 6.21), and 11.91 (SE = 7.39). Moreover, the loss of significance in model (v) also mirrors the original paper exactly.

**4.4  Figure 1**
Figure 1 plots the distribution of starting wages for New Jersey and Pennsylvania before and after the minimum wage increase. In February 1992, prior to the policy change, the wage distributions in both states were nearly identical, with the largest share of stores paying exactly $4.25 per hour. However, by November 1992, the distribution in New Jersey shifted dramatically, with approximately 85% of stores reporting a starting wage of exactly $5.05. In contrast, the Pennsylvania distribution remained largely unchanged, still concentrated between $4.25 and $5.25. This visual evidence strongly confirms that the minimum wage increase was binding and effectively enforced in New Jersey.
The visual patterns in this replication perfectly match the original paper's Figure 1. The dramatic concentration of New Jersey stores at the new $5.05 minimum wage, combined with the lack of change in Pennsylvania's distribution, is identical to the published results. This close alignment demonstrates that the data cleaning and sample construction in this replication accurately capture the policy change.
There are no significant visual discrepancies between our figure and the original. Minor variations in the exact height of the bars may exist due to the same public-use data discrepancies discussed in Table 2, but the overall shape of the distributions and the economic conclusion are indistinguishable from the original paper.

5. **Independent Extension**
**5.1 Motivation**
The central finding of Card & Krueger (1994) is that after New Jersey (NJ) raised its minimum wage from $4.25 to $5.05 in April 1992, fast-food employment did not decline (relative to Pennsylvania, PA, it actually rose by about 2.76 FTE). The authors’ explanation is that restaurants passed the increased labor costs on to consumers rather than absorbing them through layoffs. This extension directly tests that transmission channel: did the minimum-wage increase lead to higher menu prices at NJ restaurants, and which types of food items absorbed the price increases?

**5.2 Data and Variables**
We use the course-provided two-wave survey data on 410 restaurants (Wave 1: February–March 1992; Wave 2: November–December 1992).
Dependent variable (outcome): full meal price = soda + fries + entree, i.e.
price_t = psoda_t + pfry_t + pentree_t (t = 1, 2).
The price change is defined as Δprice = price_2 − price_1.
Treatment variable: NJ (=1 for NJ, =0 for PA).
Treatment intensity variable: wage gap gap = (5.05 − wage_st) / wage_st, which measures the proportional increase in a store’s starting wage required to reach the new minimum wage (positive for NJ stores with starting wage < $5.05; zero for NJ stores with starting wage ≥ $5.05 or for PA stores).
Controls: chain brand (Burger King / KFC / Roy Rogers, with Wendy’s as the baseline), company-owned indicator co_owned, and region dummies (southj, centralj, pa1, pa2).
Valid sample: 339 stores (NJ 273, PA 66), i.e., stores with complete price data in both waves and available starting-wage data.

**5.3  Identification Strategy**
Treating NJ as the treatment group and PA as the control group, we compare the difference in price changes between the two groups across the two waves:
          DiD = E[Δprice | NJ] − E[Δprice | PA]
The identifying assumption is parallel trends: absent the minimum-wage increase, NJ and PA menu prices would have changed by the same amount. With only two waves, this assumption cannot be tested directly. Following the original paper, we rely on the similarity of Wave 1 price levels between the two groups (NJ $3.35 vs PA $3.04) and the shared regional market environment as supportive evidence.

**5.4 Econometric Model Specification**
We follow the five-column reduced-form specification in the original Table 4, replacing the dependent variable ΔFTE with Δprice:

Model	                       Specification
(i)	                   Δprice_i = α + β·NJ_i + ε_i
(ii)	             (i) + bk + kfc + roy + co_owned
(iii)	             Δprice_i = α + β·gap_i + ε_i
(iv)	            (iii) + bk + kfc + roy + co_owned
(v)	               (iv) + southj + centralj + pa1 + pa2

In models (i)–(ii), β is the DiD estimator: the menu price change in NJ relative to PA (in dollars).
Models (iii)–(v) replace the binary treatment variable with the continuous gap, testing for a dose-response relationship: do stores requiring larger wage increases raise prices more?
Standard errors are robust standard errors, consistent with the original Table 4. For controls, we also report the p-value of the joint F-test ("Probability value for controls").


**5.5 Expectations**
If β > 0 and significant, it suggests that the minimum-wage increase was partially passed through to consumers, which is one possible mechanism for the absence of an employment decline.

**5.6 Results Analysis**
Given that Card and Krueger (1994) found no employment losses from New Jersey's April 1992 minimum-wage increase, this extension asks how restaurants absorbed the higher labour cost. If firms did not reduce employment, they must have adjusted along some other margin. We test the price pass-through hypothesis: that restaurants raised menu prices to offset the wage increase.
We use the same reduced-form difference-in-differences design as in Table 4, but replace the dependent variable with the change in the full-meal price (soda + fries + entree). We estimate models using the New Jersey dummy and the proportional wage gap (gap), controlling for chain and ownership, and adding region controls in some specifications. The results are reported in Table E1. Full-meal prices rose by roughly $0.10–$0.115 (about 3.5%) more in New Jersey than in Pennsylvania, an effect significant at the 5% level. The proportional-wage-gap specifications further indicate a dose–response relationship: restaurants facing a larger required wage increase raised their prices by more (coefficient ≈ 0.33–0.54), and this effect becomes significant once store characteristics are controlled for. Joint F-tests show that chain, ownership, and region characteristics are significant predictors of price changes (p ≈ 0.003–0.005). These patterns suggest that price adjustment was a key margin of response.
To understand where the price increase occurred, we decompose the full-meal price into its three components: soda, fries, and entree. The results, presented in Table E2, show that the pass-through is concentrated almost entirely in the entree. Entree prices rose by about $0.075–$0.088, while soda and fry prices were essentially unchanged. This suggests that restaurants absorbed the higher labour cost primarily by raising prices on main dishes rather than on sides or drinks.
Taken together, these results support Card and Krueger's proposed explanation: rather than reducing employment, restaurants passed much of the minimum-wage increase through to consumers in the form of higher menu prices, with the burden falling mainly on entree items. This extension provides direct evidence on the price mechanism and helps explain how firms can comply with a higher minimum wage without cutting jobs.

6. **Validation, Limitations, and Conclusion**
**6.1 Validation**
We replicated Tables 2–4 and Figure 1 from Card and Krueger (1994) using the provided data and Stata. Our DiD estimates show a positive relative employment gain in New Jersey, confirming the original’s core finding of no negative employment effect. The wage-gap regressions and robustness checks also align with the paper, and our price extension yields a 3.3–3.5% relative increase in New Jersey full meal prices, consistent with the original log-price estimate of 3.7%.

**6.2 Limitations**
We cannot fully rule out local demand shocks, although the price results support a cost-push story. The findings are specific to fast food in one region during a recession, and the item-level price results rely on small samples and should be treated as suggestive.

**6.3 Conclusion**
The replication confirms that New Jersey’s minimum-wage increase did not reduce fast-food employment; instead, prices rose relative to Pennsylvania, indicating partial pass-through to consumers. This challenges the standard competitive model and is more consistent with models featuring labor-market frictions or product-market power. Overall, the project validates the original findings and adds new evidence that price adjustment, especially in entrées, helped absorb higher labor costs.

7. **AI-Use Disclosure**
Please refer to AI_USE_DISCLOSURE.md for a detailed breakdown of how AI tools were used, checked, and corrected during this project.