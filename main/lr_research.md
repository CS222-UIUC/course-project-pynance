## Setting the Context and the Linear Regression Model

Given a dataset $\{x_1,x_2,x_3,x_4\}_{i=1}^{n}$ of $n$ data samples and a multiple variable linear regression model, we make the assumption that the relationship between the dependent variable $y$ and the vector of regressors $\bold{x}$ is linear and thus can be written as a linear combination.

$y_i=\beta_0+\beta_1 x_1+\beta_2x_2+\beta_3 x_3+\beta_4 x_4+\epsilon_i=\bold{x}_i^T\bold{\beta}+\epsilon_i$ ,

where $\mathcal{\beta}$ denotes the $5$-dimensional *****************parameter vector*****************, precisely where $\beta_0$ is the intercept term, and $\epsilon_i$ denotes the error variable — “an unobserved random variable that adds ******noise****** to the linear relationship between the dependent variable and regressors.” We will talk more about this error variable later on in our analysis so as to reduce the margin of error in our model and prediction.

Our choice for the $5-$dimensional ****************parameter vector**************** rises from the fact that we are choosing four parameters for which to define our multiple variable linear regression, which are Opening Price, High, Low, and Volume of the stock at given period $P$ and interval $I$, where period denotes the span of the time for which we are monitoring the trading activity in question and interval denotes the intervals at which the stock price is sampled.

For example, let’s say we are monitoring Google Inc.’s stock price. If we are to sample data from a period $P=\textnormal{1d}$ (which would be the abbreviation of one day) and interval $I=\textnormal{1m}$ (which would be the abbreviation of one minute), then from a whole day we would sample the stock’s price every one minute and since the stock market is open for regularly 6.5 hours, we would get approximately 390 data points for the stock price since 6.5 hours is 390 minutes.

We thus define the meaning of our independent variables $x_i$, defined for a given $P$ and $I$, 

$x_1\rightarrow\textnormal{Opening Price}$
$x_2\rightarrow\textnormal{High}$
$x_3\rightarrow\textnormal{Low}$
$x_4\rightarrow\textnormal{Volume}$

## Assumptions Made in Linear Regression and Appropriate Tests

To start off, we must first acknowledge the initial assumptions that linear regression as a model makes when using standard estimation techniques such as ordinary least squares:

### **********************************Weak exogeneity**********************************

This assumption is standard in many regression models such as ordinary least squares regression, and assumes that the independent variables $x_i$ are weakly correlated (small) with the error term of the regression equation $\epsilon_i$. They could be correlated because:

1. *Omitted variable bias:* Important variables are not included in the regression model, therefore regression coefficients become more biased and inconsistent.
2. *********Reverse causality:********* Independent variables could be endogenous (correlated with the error term) because they are affected by the dependent variable. 
3. ********************Measurement errors:******************** If there are measurement errors in the independent variables, they could very well potentally be correlated with the error term, which leads to endogeneity.
4. ****Simultaneity:**** Independent variables could be endogenous because they are jointly determined with the dependent variable. 

To test for weak exogeneity visually, we can:

→ Plot the residuals against each independent variable to check for patterns or trends.

→ Create a correlation matrix to check for any correlations between independent variables and the residuals, and if any are significant, means that independent variable is related to error term.

We can additionally use a test statistic to test for this, specifically the Hausman test, which is used to test for endogeneity; the presence of correlation between the independent variables and the error term. To test this, we can use the following script in Python:

```python
from linearmodels.iv import IV2SLS
from linearmodels.panel import PanelOLS
from linearmodels.tests.utility import hausman

# Estimate OLS model, rename vars to corresponding column names
ols_model = PanelOLS.from_formula('y ~ x1 + x2 + x3 + x4', data=df)
ols_results = ols_model.fit()

# Estimate 2SLS model, rename vars to corresponding column names
iv_model = IV2SLS.from_formula('y ~ [x1 + x2 + x3 + x4 ~ z1 + z2]', data=df)
iv_results = iv_model.fit()

# Perform Hausman test
test_results = hausman(ols_results, iv_results)
print('Hausman test statistic:', test_results.statistic)
print('p-value:', test_results.pval)
```

The details for this test statistic are omitted and left for research if needed. Made concise, the null hypothesis of the test is that the OLS estimator is consistent and efficient, while the IV estimator is consistent and inefficient. 

For reference, a consistent estimator is defined as an estimator that converges in probability to the true value of the parameter that is being estimated as the sample size increases, while an efficient estimator is an estimator that has the smallest possible variance among all unbiased estimators of that same parameter.

If p is less than a given significance value, say 0.05/5%, then we can reject the null hypothesis which suggests that the independent variables are endogenous and that we should use an IV estimator instead. We will perform further research into IV estimation if we find that the independent variables are endogenous and is necessary.

### Linearity

Mean of the dependent variable is a linear combination of the parameters, which are the regression coefficients, and the independent variables. This is something to consider much more if we are performing something like polynomial regression, which is more prone to overfitting.

We can check that a linear regression is appropriate for the data with a residual plot and verifying that it has no random patterns or trends, and if it does, suggests that it is not appropriate.

### **************************************Constant variance (homoscedasticity)**************************************

Variance of the errors does NOT depend on the values of the independent variables, so variability of the dependent variable for a fixed value of the independent variables is the same regardless of their magnitude. To check this assumption, plot of residuals versus the predicted values can be examined for a “fanning effect” (as mentioned above, verifying that it has no random patterns or trends). We can additionally test for homoscedasticity using the Bresuch-Pagan test.

To test this, we can use statsmodels in Python to test this claim with our residuals:

```python
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan

# Fit the linear regression model
X = sm.add_constant(X) # Add a constant term to the independent variables
model = sm.OLS(y, X).fit()

# Calculate the residuals
residuals = model.resid

# Perform the Breusch-Pagan test
test_results = het_breuschpagan(residuals, X)
print('Breusch-Pagan test statistic:', test_results[0])
print('p-value:', test_results[1])
print('f-value:', test_results[2])
print('f p-value:', test_results[3])
```

The nulll hypothesis of the Bresuch-Pagan test is that the variance of the errors is fixed and constant, meaning that it is homoscedastic. If the p-value is below a chosen significance, let’s say 0.05/5%, then we can reject the null hypothesis and conclude that it is heteroscedastic.

> The presence of heteroscedasticity will result in an overall "average" estimate of variance being used instead of one that takes into account the true variance structure. This leads to less precise (but in the case of ordinary least squares, not biased) parameter estimates and biased standard errors, resulting in misleading tests and interval estimates.
> 

### ************************************************Independence of errors************************************************

Errors of the dependent variable are uncorrelated with each other. This can be tested by using residual plots, which is a graphical method as mentioned before, but this can also be tested by using another test statistic for autocorrelation, like Durbin-Watson test.

```python
import numpy as np
import statsmodels.api as sm

# Perform Durbin-Watson test
test_statistic, p_value, _ = sm.stats.stattools.durbin_watson(residuals)

print(f"Durbin-Watson test statistic: {test_statistic:.3f}")
print(f"P-value: {p_value:.3f}")
```

Given that the p-value is less than a chosen significance level, say 0.05/5%, we have enough evidence to show there is autocorrelation in the residuals and this suggests that our initial assumption of independence of errors in our linear regression model may be violated. 

### ****************************************************************Lack of perfect multicollinearity (in the independent variables)****************************************************************

For standard least squares estimation methods, we must assume that the design matrix $\bold{X}$ must have full column rank $p$ where $p$ is the amount of parameters, otherwise perfect multicollinearity exists in the independent variables, meaning a linear relationship exists between two or more independent variables. Near violators of this assumption, where independent variables are highly but not perfectly correlated, can reduce the precision of parameter estimates.

This is understandably a problem for a linear regression model because it means that one independent variable is a transformation, alteration, or duplication of another because both or more depend on one another, which leads to highly unstable and sensitive predictions when the data is slightly altered. This makes sense because it could give double or more the weight to what is technically the same independent variable amidst the rest of the other independent variables. Redundantly, we also refer to our connotation of ***********independent*********** variables, such that the columns in the matrix $\bold{X}$ are linearly independent, and thus why we test for full column rank.

To check for multicollinearity, it suffices with calculating that the rank of design matrix $\bold{X}$ is $p$ so as to check if any independent variable column is a linear combination of another and thus redundant and worth eliminating so as to prevent the previously mentioned downsides.
