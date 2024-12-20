# tests/attackers/test_attacker.py
from typing import Dict, Any

import pytest
from collections import deque
from midone.attackers.attacker import Attacker
from midone.accounting.pnl import Pnl
from midone.gameconfig import EPSILON, HORIZON, DEFAULT_HISTORY_LEN, DEFAULT_TRADE_BACKOFF

class ExampleAttacker(Attacker):
    def __init__(self, epsilon=EPSILON, max_history_len=DEFAULT_HISTORY_LEN, backoff=DEFAULT_TRADE_BACKOFF):
        super().__init__(epsilon=epsilon, max_history_len=max_history_len, backoff=backoff)
        self.data = []

    def tick(self, x):
        # For testing, simply store the incoming data
        self.data.append(x)

    def predict_using_history(self, xs, horizon=HORIZON):
        # Simple prediction: return the average of the history
        if not xs:
            return 0.0
        return sum(xs) / len(xs)

    def to_dict(self) -> Dict[str, Any]:
        state = super().to_dict()
        state.update({'data': self.data})
        return state

    @classmethod
    def from_dict(cls, state: dict):
        pnl_state = state.get('pnl', {})
        epsilon = pnl_state.get('epsilon', EPSILON)
        backoff = pnl_state.get('backoff', DEFAULT_TRADE_BACKOFF)
        max_history_len = state.get('max_history_len', DEFAULT_HISTORY_LEN)

        instance = cls(epsilon=epsilon, max_history_len=max_history_len, backoff=backoff)
        instance.history = deque(state.get('history', []), maxlen=max_history_len)
        instance.pnl = Pnl.from_dict(pnl_state)
        instance.data = state.get('data', [])
        return instance

@pytest.fixture
def attacker_instance():
    return ExampleAttacker()

def test_attacker_initialization_default(attacker_instance):
    assert attacker_instance.pnl.epsilon == EPSILON
    assert attacker_instance.pnl.backoff == DEFAULT_TRADE_BACKOFF
    assert attacker_instance.max_history_len == DEFAULT_HISTORY_LEN
    assert isinstance(attacker_instance.history, deque)
    assert attacker_instance.history.maxlen == DEFAULT_HISTORY_LEN
    assert len(attacker_instance.history) == 0
    assert isinstance(attacker_instance.pnl, Pnl)

def test_attacker_initialization_custom():
    custom_epsilon = 0.5
    custom_max_history = 50
    custom_backoff = 75
    attacker = ExampleAttacker(epsilon=custom_epsilon, max_history_len=custom_max_history, backoff=custom_backoff)

    assert attacker.pnl.epsilon == custom_epsilon
    assert attacker.pnl.backoff == custom_backoff
    assert attacker.max_history_len == custom_max_history
    assert attacker.history.maxlen == custom_max_history
    assert len(attacker.history) == 0

def test_attacker_tick_and_predict_not_full_history(attacker_instance):
    """
    Test tick_and_predict when history is not full.
    Should return 0 as per the predict method.
    """
    decisions = []
    inputs = [10, 20, 30]
    for x in inputs:
        decision = attacker_instance.tick_and_predict(x)
        decisions.append(decision)

    # Since history is not full, predict should return 0 each time
    assert decisions == [0, 0, 0]
    assert list(attacker_instance.get_recent_history()) == inputs
    assert list(attacker_instance.data) == inputs


def test_attacker_tick_and_predict_full_history(attacker_instance):
    """
    Test tick_and_predict when history is full.
    The predict method should return the average of the history.
    """
    # Fill the history
    for i in range(DEFAULT_HISTORY_LEN+1):
        attacker_instance.tick_and_predict(float(i))

    # Now the history is full
    assert attacker_instance.is_history_full()

    # Make a prediction
    next_value = 200
    decision = attacker_instance.tick_and_predict(next_value)
    import numpy as np
    all_data = attacker_instance.data[-DEFAULT_HISTORY_LEN:]
    expected_prediction = (np.mean(all_data))
    assert decision == expected_prediction
    assert len(attacker_instance.history) == DEFAULT_HISTORY_LEN


def test_attacker_history_overflow(attacker_instance):
    """
    Test that the history does not exceed max_history_len.
    """
    for i in range(DEFAULT_HISTORY_LEN + 10):
        attacker_instance.tick_and_predict(float(i))

    assert len(attacker_instance.history) == DEFAULT_HISTORY_LEN
    assert list(attacker_instance.history) == [float(i) for i in range(10, DEFAULT_HISTORY_LEN + 10)]

def test_attacker_serialization(attacker_instance):
    inputs = [1.0, 2.0, 3.0]
    for x in inputs:
        attacker_instance.tick_and_predict(x)

    state = attacker_instance.to_dict()

    assert state['max_history_len'] == DEFAULT_HISTORY_LEN
    assert state['history'] == inputs
    assert state['pnl'] == attacker_instance.pnl.to_dict()
    assert state['data'] == inputs

    new_attacker = ExampleAttacker.from_dict(state)

    assert new_attacker.pnl.epsilon == attacker_instance.pnl.epsilon
    assert new_attacker.pnl.backoff == attacker_instance.pnl.backoff
    assert new_attacker.max_history_len == attacker_instance.max_history_len
    assert list(new_attacker.history) == list(attacker_instance.history)
    assert new_attacker.pnl.to_dict() == attacker_instance.pnl.to_dict()
    assert new_attacker.data == attacker_instance.data


def test_attacker_empty_serialization():
    """
    Test serialization and deserialization when history is empty.
    """
    attacker = ExampleAttacker()
    state = attacker.to_dict()

    expected_state = {
        'max_history_len': DEFAULT_HISTORY_LEN,
        'history': [],
        'pnl': attacker.pnl.to_dict(),
        'data': []
    }
    assert state == expected_state

    # Deserialize
    new_attacker = ExampleAttacker()
    new_attacker.from_dict(state)

    assert new_attacker.pnl.epsilon == attacker.pnl.epsilon
    assert new_attacker.max_history_len == attacker.max_history_len
    assert list(new_attacker.history) == []
    assert new_attacker.pnl.to_dict() == attacker.pnl.to_dict()
    assert new_attacker.data == []


def test_attacker_predict_without_history(attacker_instance):
    """
    Test the predict method when history is empty.
    """
    decision = attacker_instance.predict()
    assert decision == 0


def test_attacker_is_history_full(attacker_instance):
    """
    Test the is_history_full method.
    """
    for i in range(DEFAULT_HISTORY_LEN):
        attacker_instance.tick_history(float(i))
        assert not attacker_instance.is_history_full() if i < DEFAULT_HISTORY_LEN - 1 else attacker_instance.is_history_full()


def test_attacker_get_recent_history(attacker_instance):
    """
    Test retrieving recent history.
    """
    inputs = [10, 20, 30, 40, 50]
    for x in inputs:
        attacker_instance.tick_history(x)

    recent = attacker_instance.get_recent_history(3)
    assert recent == [30, 40, 50]


def test_attacker_history_full_behavior(attacker_instance):
    """
    Test that oldest entries are removed when history exceeds max length.
    """
    max_len = 5
    attacker = ExampleAttacker(max_history_len=max_len)
    for i in range(7):
        attacker.tick_history(float(i))

    assert len(attacker.history) == max_len
    assert list(attacker.history) == [2.0, 3.0, 4.0, 5.0, 6.0]


def test_attacker_multiple_tick_and_predict(attacker_instance):
    """
    Test multiple tick_and_predict calls and ensure state consistency.
    """
    inputs = [5, 15, 25, 35, 45]
    expected_decisions = []
    for i, x in enumerate(inputs):
        decision = attacker_instance.tick_and_predict(x)
        if i < DEFAULT_HISTORY_LEN - 1:
            expected_decisions.append(0)
        else:
            avg = sum(range(i - (DEFAULT_HISTORY_LEN - 1), i + 1)) / DEFAULT_HISTORY_LEN
            expected_decisions.append(avg)

    assert attacker_instance.data == inputs
    assert list(attacker_instance.history) == [float(a) for a in inputs]


# Running all tests using pytest
if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
