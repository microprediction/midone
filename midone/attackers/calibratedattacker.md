
# CalibratedAttacker

`CalibratedAttacker` is an example class that takes a raw, "uncalibrated" attacker and uses empirical performance to govern its decisions. The core idea is to treat the attacker's decisions as a signal that needs standardization before making real trading decisions.

The class tracks the performance (profit and loss) of threshold-based trades that are triggered by a standardized signal exceeding a specified threshold. Based on this performance, the `predict` method provides decisions in the set `{ -1, 0, 1 }`, corresponding to sell, hold, or buy actions.


See [demo_calibratedattacker.md](https://github.com/microprediction/midone/blob/main/tests/attackers/demo_calibratedattacker.md)
