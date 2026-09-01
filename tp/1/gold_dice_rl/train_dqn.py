"""
Entrena el DQNAgent y lo compara contra RandomLegalAgent, SimpleExpectancyAgent
y EpsilonGreedyQAgent (tabular) en Gold Dice RL. Reutiliza evaluate_agents.evaluate
y renderer.plot_episode.

Usamos:
    python train_dqn.py
"""

import numpy as np

from env import GoldDiceEnv
from agents import RandomLegalAgent, SimpleExpectancyAgent, EpsilonGreedyQAgent
from dqn_agent import DQNAgent, featurize, N_META_ACTIONS
from evaluate_agents import evaluate
from renderer import plot_episode


def quick_eval(agent, n_episodes=30, seed=999):
    """Evaluación rápida y greedy (training=False) para elegir checkpoints
    durante el entrenamiento. Usa una seed fija de evaluación, separada de
    la de entrenamiento."""
    env = GoldDiceEnv(obs_mode="dict", seed=seed, track_history=False)
    scores = []
    for ep in range(n_episodes):
        obs = env.reset(seed=seed + ep)
        done = False
        while not done:
            action, score_amount = agent.act(obs, env, training=False)
            obs, reward, done, info = env.step(action, score_amount=score_amount)
        scores.append(env.points)
    return float(np.mean(scores))


def train(n_episodes=10000, seed=0, train_every=1, eval_every=200, eval_episodes=30, **agent_kwargs):
    """
    DQN es inestable por naturaleza (la red se mueve, el target se mueve,
    y todo se retroalimenta), así que en vez de quedarnos con los pesos
    finales, evaluamos cada `eval_every` episodios con política greedy y
    guardamos el mejor checkpoint visto. Al final restauramos esos pesos.
    """
    env = GoldDiceEnv(obs_mode="dict", seed=seed, track_history=False)
    agent = DQNAgent(seed=seed, **agent_kwargs)

    episode_points = np.zeros(n_episodes)
    losses = []

    best_score = -np.inf
    best_state_dict = None

    for ep in range(n_episodes):
        agent.set_episode(ep)
        obs = env.reset()
        done = False
        step = 0

        while not done:
            action, score_amount = agent.act(obs, env, training=True)
            state = agent.last_state
            meta_action = agent.last_meta_action

            next_obs, reward, done, info = env.step(action, score_amount=score_amount)

            next_mask = (
                np.zeros(N_META_ACTIONS, dtype=np.float32) if done else agent.legal_mask(env)
            )
            agent.remember(state, meta_action, reward, featurize(next_obs), next_mask, done)

            step += 1
            if step % train_every == 0:
                loss = agent.train_step()
                if loss is not None:
                    losses.append(loss)

            obs = next_obs

        episode_points[ep] = env.points

        if (ep + 1) % eval_every == 0:
            score = quick_eval(agent, n_episodes=eval_episodes)
            if score > best_score:
                best_score = score
                best_state_dict = {k: v.clone() for k, v in agent.q_network.state_dict().items()}
            print(f"  [eval] episodio {ep + 1:>5}: {score:6.2f} puntos (mejor hasta ahora: {best_score:6.2f})")

    if best_state_dict is not None:
        agent.q_network.load_state_dict(best_state_dict)
        agent.target_network.load_state_dict(best_state_dict)

    return agent, episode_points, losses


if __name__ == "__main__":
    print("Entrenando DQNAgent...")
    agent, train_curve, losses = train(n_episodes=10000, seed=512)

    block = 500
    print("\nPuntos promedio por bloque de entrenamiento:")
    for i in range(0, len(train_curve), block):
        chunk = train_curve[i:i + block]
        print(f"  episodios {i:>5}-{i + len(chunk) - 1:<5}: {chunk.mean():6.2f}")

    if losses:
        print(f"\nLoss promedio (primeros 100 pasos entrenados): {np.mean(losses[:100]):.3f}")
        print(f"Loss promedio (últimos 100 pasos entrenados):  {np.mean(losses[-100:]):.3f}")

    #Evaluamos los Agentes
    agents = {
        "EpsilonGreedyQAgent": EpsilonGreedyQAgent(),
        "SimpleExpectancy": SimpleExpectancyAgent(),
        "DQN": agent,
    }

    print("\nResultados sobre 500 partidas de evaluación:")
    for name, a in agents.items():
        print(f"  {name:<20} {evaluate(a, n_episodes=500, seed=123)}")

    # Episodio de ejemplo con el agente entrenado, usando renderer.py
    example_env = GoldDiceEnv(obs_mode="dict", seed=777, track_history=True)
    obs = example_env.reset()
    done = False
    while not done:
        action, score_amount = agent.act(obs, example_env, training=False)
        obs, reward, done, info = example_env.step(action, score_amount=score_amount)

    print(f"\nEpisodio de ejemplo (seed=777) -> puntos finales: {example_env.points}")
    plot_episode(example_env.history, save_path="dqn_example_episode.png", show=False)
