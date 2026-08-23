import pickle

import numpy as np

from config import (
    HORIZON,
    DICE_FACES,
    SHIELD_COST,
    get_new_dice_cost,
    get_upgrade_cost,
)

from env import (
    PASS,
    SCORE,
    BUY_DICE,
    UPGRADE,
    BUY_SHIELD,
    STORE_BEST_DIE,
    N_ACTIONS,
)


class RandomLegalAgent:
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed)

    def act(self, obs, env):
        action = int(self.rng.choice(env.get_valid_actions()))
        score_amount = None

        if action == SCORE:
            score_amount = int(self.rng.choice(env.get_valid_score_amounts()))

        return action, score_amount


class SimpleExpectancyAgent:

    def act(self, obs, env=None):
        turn = obs["turn"]
        gold = obs["gold"]
        num_dice = obs["num_dice"]
        dice_bonus = obs["dice_bonus"]
        shields = obs["shields"]

        turns_left = HORIZON - turn

        if turns_left == 0:
            return SCORE, gold

        if shields == 0 and gold >= SHIELD_COST:
            return BUY_SHIELD, None

        best_action = PASS
        best_value = 0.0

        dice_cost = get_new_dice_cost(num_dice)
        if gold >= dice_cost:
            buy_dice_value = (float(np.mean(DICE_FACES)) + dice_bonus) * turns_left - dice_cost
            if buy_dice_value > best_value:
                best_value = buy_dice_value
                best_action = BUY_DICE

        upgrade_cost = get_upgrade_cost(dice_bonus)
        if gold >= upgrade_cost:
            upgrade_value = num_dice * turns_left - upgrade_cost
            if upgrade_value > best_value:
                best_value = upgrade_value
                best_action = UPGRADE

        return best_action, None


# ---------------------------------------------------------------------------
# Agente Monte Carlo (nuestro)
# ---------------------------------------------------------------------------

# Cortes de gold anclados a los umbrales de decision del juego:
#   5  -> alcanza para escudo
#   18 -> alcanza para el primer dado
# 6 bins: [0-4], [5-9], [10-17], [18-35], [36-79], [80+]
GOLD_EDGES = [5, 10, 18, 36, 80]


def encode_state(obs):
    """Mapea la observacion cruda a una clave discreta (hashable) para la tabla Q.

    Variables usadas: turns_left, gold (binned), num_dice, dice_bonus, shields.
    Se dejan fuera a proposito: points (no afecta la dinamica),
    roll_max y stored_value (0% de uso en los baselines).
    """
    turns_left = HORIZON - obs["turn"]                 # 0..29
    g = obs["gold"]
    gold_bin = sum(1 for e in GOLD_EDGES if g >= e)    # 0..5
    nd = min(int(obs["num_dice"]) - 1, 6)              # 0..6  (num_dice 1..7+)
    db = min(int(obs["dice_bonus"]), 5)                # 0..5
    sh = min(int(obs["shields"]), 2)                   # 0,1,2+
    return (turns_left, gold_bin, nd, db, sh)


class MonteCarloAgent:
    """Agente de control Monte Carlo (first-visit), epsilon-greedy.

    - Q: dict {state_key: np.array(N_ACTIONS)} con los valores estimados.
    - epsilon: probabilidad de exploracion. Para JUGAR/evaluar, epsilon=0 (greedy).
    - Regla de scoring: cuando elige SCORE, puntua TODO el oro disponible.

    La tabla Q se entrena aparte (train_mc.py) y se carga desde disco.
    """

    def __init__(self, Q=None, epsilon=0.0, seed=None):
        self.Q = Q if Q is not None else {}
        self.epsilon = float(epsilon)
        self.rng = np.random.default_rng(seed)

    @classmethod
    def load(cls, path, epsilon=0.0, seed=None):
        with open(path, "rb") as f:
            Q = pickle.load(f)
        return cls(Q=Q, epsilon=epsilon, seed=seed)

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump(self.Q, f)

    def _q_row(self, state_key):
        # Estados no vistos arrancan en ceros (optimismo neutro).
        if state_key not in self.Q:
            self.Q[state_key] = np.zeros(N_ACTIONS, dtype=np.float64)
        return self.Q[state_key]

    def select_action(self, obs, env):
        """Elige un codigo de accion (0..5) valido, epsilon-greedy sobre Q."""
        valid = env.get_valid_actions()
        state_key = encode_state(obs)

        # Exploracion: accion valida al azar.
        if self.rng.random() < self.epsilon:
            return int(self.rng.choice(valid))

        # Explotacion: mejor accion segun Q, restringida a acciones validas.
        q = self._q_row(state_key)
        valid_arr = np.array(valid, dtype=int)
        best = valid_arr[np.argmax(q[valid_arr])]
        return int(best)

    def act(self, obs, env):
        action = self.select_action(obs, env)
        score_amount = int(obs["gold"]) if action == SCORE else None
        return action, score_amount