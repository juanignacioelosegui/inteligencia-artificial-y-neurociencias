"""
Deep Q-Learning (DQN) para Gold Dice RL.

Reemplaza la Q-table tabular del EpsilonGreedyQAgent por una red 
neuronal que aproxima Q(s, a) directamente sobre el estado continuo
(sin discretizar).

Tenemos:
  - N_META_ACTIONS, META_TO_BASE: mismo esquema de meta-acciones que el
    agente tabular (SCORE partido en fracciones 0/25/50/75/100% del oro).
  - legal_meta_actions(env), meta_action_to_env_action(meta, env): misma
    lógica de acciones válidas y traducción a la acción del entorno.

Requiere que instalemos PyTorch (pip install torch).
"""

import random
from collections import deque

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from agents import N_META_ACTIONS, legal_meta_actions, meta_action_to_env_action
from config import HORIZON


# Features usadas como entrada de la red. Se excluye "points": no afecta
# la dinámica futura del juego, así que no debería influir en Q(s,a).
FEATURE_KEYS = [
    "turn",
    "gold",
    "num_dice",
    "dice_bonus",
    "shields",
    "stored_value",
    "roll_sum",
    "roll_max",
]

# Escalas aproximadas para llevar cada feature a un rango ~[0, 2-3].
# Están calibradas para este juego (30 turnos, oro típico < 1000); 

FEATURE_SCALE = {
    "turn": HORIZON,
    "gold": 150.0,
    "num_dice": 6.0,
    "dice_bonus": 4.0,
    "shields": 2.0,
    "stored_value": 10.0,
    "roll_sum": 40.0,
    "roll_max": 8.0,
}


def featurize(obs):
    """Convierte el obs (dict) en un vector normalizado float32."""
    return np.array(
        [obs[k] / FEATURE_SCALE[k] for k in FEATURE_KEYS],
        dtype=np.float32,
    )


STATE_DIM = len(FEATURE_KEYS)


class QNetwork(nn.Module):
    def __init__(self, state_dim=STATE_DIM, n_actions=N_META_ACTIONS, hidden_sizes=(64, 64)):
        super().__init__()
        layers = []
        in_dim = state_dim
        for h in hidden_sizes:
            layers += [nn.Linear(in_dim, h), nn.ReLU()]
            in_dim = h
        layers.append(nn.Linear(in_dim, n_actions))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)


class ReplayBuffer:
    def __init__(self, capacity=20000, seed=None):
        self.buffer = deque(maxlen=capacity)
        self.rng = random.Random(seed)

    def push(self, state, action, reward, next_state, next_legal_mask, done):
        self.buffer.append((state, action, reward, next_state, next_legal_mask, done))

    def sample(self, batch_size):
        batch = self.rng.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, next_masks, dones = zip(*batch)
        return (
            np.array(states, dtype=np.float32),
            np.array(actions, dtype=np.int64),
            np.array(rewards, dtype=np.float32),
            np.array(next_states, dtype=np.float32),
            np.array(next_masks, dtype=np.float32),
            np.array(dones, dtype=np.float32),
        )

    def __len__(self):
        return len(self.buffer)


class DQNAgent:
    """
    Agente DQN con exploración epsilon-greedy para Gold Dice RL.

    Misma interfaz que RandomLegalAgent / EpsilonGreedyQAgent: act(obs, env) -> (action, score_amount),
    compatible con evaluate_agents.evaluate() y run_example.py.

    Uso de entrenamiento:

        agent = DQNAgent(seed=0)
        for ep in range(n_episodes):
            agent.set_episode(ep)
            obs = env.reset()
            done = False
            while not done:
                action, score_amount = agent.act(obs, env, training=True)
                state, meta_action, mask = agent.last_state, agent.last_meta_action, agent.last_legal_mask
                next_obs, reward, done, info = env.step(action, score_amount=score_amount)
                next_mask = agent.legal_mask(env) if not done else np.zeros(N_META_ACTIONS, dtype=np.float32)
                agent.remember(state, meta_action, reward, featurize(next_obs), next_mask, done)
                agent.train_step()
                obs = next_obs

    Uso de evaluación, greedy:

        action, score_amount = agent.act(obs, env)  # training=False por default
    """

    def __init__(
        self,
        n_actions=N_META_ACTIONS,
        hidden_sizes=(64, 64),
        lr=5e-4,
        gamma=0.98,
        buffer_size=20000,
        batch_size=64,
        min_buffer_size=500,
        target_update_freq=500,
        epsilon_start=1.0,
        epsilon_end=0.05,
        epsilon_decay_episodes=3000,
        grad_clip=1.0,
        reward_scale=1.0 / 50.0,
        double_dqn=True,
        seed=None,
    ):
        torch.manual_seed(0 if seed is None else seed)

        self.n_actions = n_actions
        self.gamma = gamma
        self.batch_size = batch_size
        self.min_buffer_size = min_buffer_size
        self.target_update_freq = target_update_freq
        self.grad_clip = grad_clip
        self.reward_scale = reward_scale
        self.double_dqn = double_dqn

        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay_episodes = epsilon_decay_episodes
        self.epsilon = epsilon_start

        self.rng = np.random.default_rng(seed)

        self.q_network = QNetwork(STATE_DIM, n_actions, hidden_sizes)
        self.target_network = QNetwork(STATE_DIM, n_actions, hidden_sizes)
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.target_network.eval()

        self.optimizer = torch.optim.Adam(self.q_network.parameters(), lr=lr)
        self.replay_buffer = ReplayBuffer(capacity=buffer_size, seed=seed)

        self.train_steps = 0
        self.last_state = None
        self.last_meta_action = None
        self.last_legal_mask = None

    # -- exploración 

    def set_episode(self, episode):
        """Decay lineal de epsilon a lo largo del entrenamiento."""
        progress = min(episode / max(self.epsilon_decay_episodes, 1), 1.0)
        self.epsilon = self.epsilon_start + progress * (self.epsilon_end - self.epsilon_start)

    # -- acciones legales 

    def legal_mask(self, env):
        mask = np.zeros(self.n_actions, dtype=np.float32)
        mask[legal_meta_actions(env)] = 1.0
        return mask

    # -- actuar 

    def act(self, obs, env, training=False):
        state = featurize(obs)
        legal = legal_meta_actions(env)
        legal_mask = np.zeros(self.n_actions, dtype=np.float32)
        legal_mask[legal] = 1.0

        if training and self.rng.random() < self.epsilon:
            meta_action = int(self.rng.choice(legal))
        else:
            with torch.no_grad():
                q_values = self.q_network(torch.from_numpy(state).unsqueeze(0)).squeeze(0).numpy()
            q_values = np.where(legal_mask == 1.0, q_values, -np.inf)
            meta_action = int(np.argmax(q_values))

        self.last_state = state
        self.last_meta_action = meta_action
        self.last_legal_mask = legal_mask
        return meta_action_to_env_action(meta_action, env)

    # -- entrenamiento 

    def remember(self, state, action, reward, next_state, next_legal_mask, done):
        self.replay_buffer.push(state, action, reward * self.reward_scale, next_state, next_legal_mask, done)

    def train_step(self):
        """Un paso de SGD sobre un minibatch del replay buffer. Devuelve la
        loss (float) o None si todavía no hay suficientes transiciones."""
        if len(self.replay_buffer) < max(self.batch_size, self.min_buffer_size):
            return None

        states, actions, rewards, next_states, next_masks, dones = self.replay_buffer.sample(self.batch_size)

        states_t = torch.from_numpy(states)
        actions_t = torch.from_numpy(actions).unsqueeze(1)
        rewards_t = torch.from_numpy(rewards)
        next_states_t = torch.from_numpy(next_states)
        next_masks_t = torch.from_numpy(next_masks)
        dones_t = torch.from_numpy(dones)

        q_values = self.q_network(states_t).gather(1, actions_t).squeeze(1)

        with torch.no_grad():
            if self.double_dqn:
                online_next_q = self.q_network(next_states_t)
                online_next_q = online_next_q.masked_fill(next_masks_t == 0, float("-inf"))
                best_next_actions = online_next_q.argmax(dim=1, keepdim=True)
                target_next_q = self.target_network(next_states_t).gather(1, best_next_actions).squeeze(1)
            else:
                next_q = self.target_network(next_states_t)
                next_q = next_q.masked_fill(next_masks_t == 0, float("-inf"))
                target_next_q = next_q.max(dim=1).values

            # Estados terminales (o sin acciones legales registradas) -> 0;
            # el término (1 - dones_t) ya los anula, esto solo evita -inf/nan.
            target_next_q = torch.nan_to_num(target_next_q, neginf=0.0, posinf=0.0)
            target = rewards_t + self.gamma * target_next_q * (1.0 - dones_t)

        loss = F.smooth_l1_loss(q_values, target)

        self.optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(self.q_network.parameters(), self.grad_clip)
        self.optimizer.step()

        self.train_steps += 1
        if self.train_steps % self.target_update_freq == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())

        return float(loss.item())
