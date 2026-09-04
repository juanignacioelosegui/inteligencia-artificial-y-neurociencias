import numpy as np

class Agent:
    def __init__(self, name):
        self.name = name
        self.environment = None

    def reset_internal_state(self):
        raise NotImplementedError

    def select_action(self, game_state):
        raise NotImplementedError

    def update_internal_state(self, observation, action, reward):
        raise NotImplementedError

    def get_extra_info(self):
        return None

    def play(self, n_steps:int, env):
        """
        Ejecuta una corrida de n_steps pasos en el entorno env.
        Devuelve un diccionario con las recompensas obtenidas y 
        un log de si la acción tomada fue la óptima.
        """
        self.environment = env
        self.reset_internal_state()
        
        rewards = []
        selected_best_action = []

        # --- CALCULO DE LA MEJOR ACCION ---
        # Usamos env.unwrapped para acceder al entorno base
        # Los entornos de bandit suelen tener r_dist y p_dist
        # r_dist: medias de recompensa, p_dist: probabilidades
        try:
            r_dist = np.array(env.unwrapped.r_dist)[:, 0]  # promedio de recompensa
            p_dist = np.array(env.unwrapped.p_dist)       # probabilidades
            expected_values = r_dist * p_dist
            best_action = int(np.argmax(expected_values))
        except AttributeError:
            # Si no podemos acceder a las distribuciones, simplemente marcamos best_action = None
            best_action = None

        # Reset inicial del entorno
        state = env.reset()

        for step in range(n_steps):
            # 1. Seleccionar acción
            action = self.select_action(state)

            # 2. Tomar acción en el entorno
            next_state, reward, done, info = env.step(action)

            # 3. Actualizar estado interno
            self.update_internal_state(state, action, reward)

            # 4. Guardar logs
            rewards.append(reward)
            if best_action is not None:
                selected_best_action.append(1 if action == best_action else 0)
            else:
                selected_best_action.append(0)  # si no podemos calcular best_action

            # 5. Avanzar estado
            state = next_state

        logs = {
            "rewards": rewards,
            "selected_best_action": selected_best_action
        }
        return logs, self.get_extra_info()