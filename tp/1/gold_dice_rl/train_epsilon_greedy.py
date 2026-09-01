"""
Entrena el EpsilonGreedyQAgent y lo compara contra RandomLegalAgent y
SimpleExpectancyAgent en Gold Dice RL, reutilizando evaluate_agents.evaluate.

Usamos:
    python train_epsilon_greedy.py
"""

import numpy as np

from env import GoldDiceEnv
from agents import (
    EpsilonGreedyQAgent,
    RandomLegalAgent,
    SimpleExpectancyAgent,
    discretize_state,
)
from evaluate_agents import evaluate


def train(n_episodes=8000, seed=0, **agent_kwargs):
    env = GoldDiceEnv(obs_mode="dict", seed=seed, track_history=False)
    agent = EpsilonGreedyQAgent(seed=seed, **agent_kwargs)

    episode_points = np.zeros(n_episodes)

    for ep in range(n_episodes):
        agent.set_episode(ep)
        obs = env.reset()
        done = False

        while not done:
            action, score_amount = agent.act(obs, env, training=True)
            state, meta_action = agent.last_state, agent.last_meta_action

            next_obs, reward, done, info = env.step(action, score_amount=score_amount)

            next_state = discretize_state(next_obs)
            next_legal = agent.legal_meta_actions(env) if not done else []
            agent.update(state, meta_action, reward, next_state, next_legal, done)

            obs = next_obs

        episode_points[ep] = env.points

    return agent, episode_points


if __name__ == "__main__":
    print("Entrenando EpsilonGreedyQAgent...")
    agent, train_curve = train(n_episodes=8000, seed=0)

    block = 1000
    print("\nPuntos promedio por bloque de entrenamiento:")
    for i in range(0, len(train_curve), block):
        chunk = train_curve[i:i + block]
        print(f"  episodios {i:>5}-{i + len(chunk) - 1:<5}: {chunk.mean():6.2f}")

    # agent.act ya devuelve (action, score_amount) en modo evaluación
    # (training=False por default), así que evaluate() de evaluate_agents.py
    # funciona sin modificaciones para cualquiera de los agentes.
    agents = {
        "RandomLegal": RandomLegalAgent(seed=123),
        "SimpleExpectancy": SimpleExpectancyAgent(),
        "EpsilonGreedyQ": agent,
    }

    print("\nResultados sobre 500 partidas de evaluación:")
    for name, a in agents.items():
        print(f"  {name:<20} {evaluate(a, n_episodes=500, seed=123)}")

    print(f"\nQ-table: {len(agent.Q)} estados visitados")
