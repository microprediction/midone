
# CalibratedAttacker

`CalibratedAttacker` is an example class that takes a raw, "uncalibrated" attacker and uses empirical performance to govern its decisions. 

The class tracks the performance (profit and loss) of threshold-based trades that are triggered by a standardized signal exceeding a specified threshold. Based on this performance, the `predict` method provides decisions in the set `{ -1, 0, 1 }`, corresponding to sell, hold, or buy actions.

## Usage Example

Look at [demo_calibratedattacker.md](https://github.com/microprediction/midone/blob/main/tests/attackers/demo_calibratedattacker.md)


## How it uses StdSignalPnl

The calibrated attacker uses the `StdSignalPnl` class to standardize an attacker's signal and tracks hypothetical profit and loss (PnL) for trades that *would be* triggered by threshold-based signals. 


1. **Initialization**:
   - The class is initialized with customizable thresholds and a fading factor for calculating exponentially weighted averages (EWA). It uses the `FEWVar` and `FEWMean` classes to track signal variance and PnL, respectively.
   - It tracks both positive and negative thresholds for trading decisions.

2. **tick()**:
   - For each new data point `x`, the attacker's signal is standardized, and the class updates the PnL for any trades triggered by exceeding the thresholds.
   - The signal's variance is updated as well, allowing the standardization to adapt over time.

3. **_add_signal_to_queues()**:
   - When the standardized signal exceeds a threshold, it stores a pending trade (signal) in a queue for future resolution.

4. **_resolve_signals_on_queues()**:
   - This method checks if the pending signals have reached their time horizon. If so, it calculates the PnL for each resolved trade and updates the exponentially weighted averages.

5. **get_expected_pnl()**:
   - This method estimates the expected PnL for the current standardized signal, based on each threshold. It takes into account transaction costs and returns the expected PnLs for both positive and negative thresholds.

6. **predict()**:
   - Based on the current standardized signal, it decides whether to buy, sell, or hold. The method evaluates the best expected PnL for each threshold and returns a decision: `1` for buy, `-1` for sell, or `0` for hold.
   


