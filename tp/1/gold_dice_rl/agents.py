from collections import defaultdict

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
# Epsilon-greedy Q-learning agent
# ---------------------------------------------------------------------------
#
# El estado (gold, num_dice, ...) es continuo/ilimitado, así que para usar
# una Q-table tabular lo discretizamos en buckets (discretize_state).
#
# SCORE es una acción parametrizada (score_amount ∈ [0, gold]), así que la
# partimos en "meta-acciones" fijas: puntuar el 0%, 25%, 50%, 75% o 100%
# del oro disponible. Esto deja un espacio de acciones discreto y chico,
# necesario para epsilon-greedy tabular.

SCORE_FRACTIONS = [0.0, 0.25, 0.5, 0.75, 1.0]

META_PASS = 0
META_SCORE_0 = 1
META_SCORE_25 = 2
META_SCORE_50 = 3
META_SCORE_75 = 4
META_SCORE_100 = 5
META_BUY_DICE = 6
META_UPGRADE = 7
META_BUY_SHIELD = 8
META_STORE_DIE = 9

N_META_ACTIONS = 10

META_TO_BASE = {
    META_PASS: (PASS, None),
    META_SCORE_0: (SCORE, SCORE_FRACTIONS[0]),
    META_SCORE_25: (SCORE, SCORE_FRACTIONS[1]),
    META_SCORE_50: (SCORE, SCORE_FRACTIONS[2]),
    META_SCORE_75: (SCORE, SCORE_FRACTIONS[3]),
    META_SCORE_100: (SCORE, SCORE_FRACTIONS[4]),
    META_BUY_DICE: (BUY_DICE, None),
    META_UPGRADE: (UPGRADE, None),
    META_BUY_SHIELD: (BUY_SHIELD, None),
    META_STORE_DIE: (STORE_BEST_DIE, None),
}


def discretize_state(obs):
    """
    Convierte un obs (dict) en una tupla chica para la Q-table.
    Los cortes de gold están pensados para este juego (oro crece más o
    menos con num_dice * turno).
    """
    turn = obs["turn"]
    gold = obs["gold"]
    num_dice = min(int(obs["num_dice"]), 8)
    dice_bonus = min(int(obs["dice_bonus"]), 6)
    shields = min(int(obs["shields"]), 3)
    roll_max = min(int(obs["roll_max"]), 12)

    turns_left = min(HORIZON - turn, HORIZON - 1)
    gold_bucket = int(np.digitize([gold], [10, 25, 50, 100, 175, 275, 400, 600, 900])[0])

    return (turns_left, gold_bucket, num_dice, dice_bonus, shields, roll_max)


def legal_meta_actions(env):
    """Meta-acciones legales ahora mismo, según env.get_valid_actions() y el oro.
    Función a nivel de módulo para poder reutilizarla desde otros agentes
    (p. ej. agente DQN) sin duplicar la lógica.
    """
    valid_base = set(env.get_valid_actions())
    legal = []
    for meta, (base_action, _fraction) in META_TO_BASE.items():
        if base_action == SCORE:
            legal.append(meta)  # score_amount=0..gold siempre es legal
        elif base_action in valid_base:
            legal.append(meta)
    return legal


def meta_action_to_env_action(meta_action, env):
    """Traduce una meta-acción discreta a (env_action, score_amount)."""
    base_action, fraction = META_TO_BASE[meta_action]
    if base_action != SCORE:
        return base_action, None
    score_amount = int(round(fraction * env.gold))
    score_amount = max(0, min(score_amount, env.gold))
    return SCORE, score_amount


class EpsilonGreedyQAgent:
    """
    Agente de Q-learning tabular con exploración epsilon-greedy.

    - Estado: discretize_state(obs) -> tupla de buckets.
    - Acción: una de N_META_ACTIONS meta-acciones (ver META_TO_BASE).
    - Exploración: epsilon decae linealmente de epsilon_start a epsilon_end
      a lo largo de epsilon_decay_episodes episodios (llamar set_episode
      al empezar cada episodio de entrenamiento).

    """

    def __init__(
        self,
        n_actions=N_META_ACTIONS,
        alpha=0.1,
        gamma=0.97,
        epsilon_start=1.0,
        epsilon_end=0.05,
        epsilon_decay_episodes=3000,
        seed=None,
    ):
        self.n_actions = n_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay_episodes = epsilon_decay_episodes
        self.rng = np.random.default_rng(seed)

        self.Q = defaultdict(lambda: np.zeros(self.n_actions, dtype=np.float64))
        self.episode = 0
        self.epsilon = epsilon_start

    def set_episode(self, episode):
        """Actualiza epsilon según el progreso del entrenamiento (decay lineal)."""
        self.episode = episode
        progress = min(episode / max(self.epsilon_decay_episodes, 1), 1.0)
        self.epsilon = self.epsilon_start + progress * (self.epsilon_end - self.epsilon_start)

    def legal_meta_actions(self, env):
        """Ver la función a nivel de módulo `legal_meta_actions`."""
        return legal_meta_actions(env)

    def _to_env_action(self, meta_action, env):
        return meta_action_to_env_action(meta_action, env)

    def act(self, obs, env, training=False):
        """
        Interfaz compatible con evaluate_agents.py / run_example.py:
        devuelve (env_action, score_amount), igual que RandomLegalAgent y
        SimpleExpectancyAgent.

        Por default training=False (modo evaluación, greedy). Durante el
        entrenamiento hay que llamar act(obs, env, training=True) para que
        explore según epsilon. El estado y la meta-acción usados quedan
        guardados en self.last_state / self.last_meta_action para poder
        llamar a update() después de env.step().
        """
        state = discretize_state(obs)
        legal = self.legal_meta_actions(env)

        explore = training and self.rng.random() < self.epsilon
        if explore:
            meta_action = int(self.rng.choice(legal))
        else:
            q_values = self.Q[state]
            legal_q = [(a, q_values[a]) for a in legal]
            best_q = max(q for _, q in legal_q)
            best_actions = [a for a, q in legal_q if q == best_q]
            meta_action = int(self.rng.choice(best_actions))

        self.last_state = state
        self.last_meta_action = meta_action
        return self._to_env_action(meta_action, env)

    def update(self, state, meta_action, reward, next_state, next_legal_actions, done):
        """Paso de Q-learning: Q(s,a) += alpha * (r + gamma * max_a' Q(s',a') - Q(s,a))."""
        current_q = self.Q[state][meta_action]
        if done or not next_legal_actions:
            target = reward
        else:
            target = reward + self.gamma * max(self.Q[next_state][a] for a in next_legal_actions)
        self.Q[state][meta_action] += self.alpha * (target - current_q)
