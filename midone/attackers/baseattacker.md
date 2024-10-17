


# BaseAttacker

A minimalist class outlining the task at hand.

## Overview

The `BaseAttacker` class provides a pattern for designing and implementing an "attacker" model that consumes a univariate sequence of numerical data points (such as stock prices, bond prices, or any time series) $x_1, x_2, \dots x_t$ and attempts to predict its future movement. It looks for small deviations from a martingale property, which is to say that we expect the series $x_t$ to satisfy:

$$ E[x_{t+k}] \approx x_t $$

The attacker need only *occasionally* signal whether the future value will deviate upward or downward from the current point. This is useful in scenarios where the attacker attempts to exploit trends or patterns for profit. However, it is also beneficial in much greater generally, as a means of performing ongoing analysis of prediction model residuals in any application in any industry. 

## Usage

To create an minimalist attacker, you might extend the `BaseAttacker` class and implement (`tick` and `predict`). For example:

```python
class MyAttacker(BaseAttacker):
    def tick(self, x: float):
        # Put your logic for internal state updating here
    
    def predict(self, horizon: int = None) -> float:
        # Put your prediction logic here. Return a directional prediction: -1 for down, 1 for up, 0 for no opinion
        
```

## Design and responsibilities  

It is strongly recommended that you read the [FAQ](https://github.com/microprediction/midone/blob/main/midone/attackers/FAQ.md). 
