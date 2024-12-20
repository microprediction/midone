


# Attackers


The `Attacker` class and cousins like `AttackerWithPnL` can be found in 
[attackers](https://github.com/microprediction/midone/tree/main/midone/attackers). These 
provide patterns for designing and implementing an "attacker" model that consumes a univariate sequence of numerical data points (such as stock prices, bond prices, or any time series) $x_1, x_2, \dots x_t$ and attempts to predict its future movement. It looks for small deviations from a martingale property, which is to say that we expect the series $x_t$ to satisfy:

$$ E[x_{t+k}] \approx x_t $$

The attacker’s need only *occasionally* signal whether the future value will deviate upward or downward from the current point. This is useful in scenarios where the attacker attempts to exploit trends or patterns for profit. However, it is also beneficial in much greater generally, as a means of performing ongoing analysis of prediction model residuals in any application in any industry. 

We suggest [attacker.md](https://github.com/microprediction/midone/blob/main/midone/attackers/attacker.md) as a starting point. 


### See also 

 - Attacker [FAQ.md](https://github.com/microprediction/midone/blob/main/midone/attackers/FAQ.md)
 - The tournament at [CrunchDAO.com](https://www.crunchdao.com) where you can use them to win rewards. 
