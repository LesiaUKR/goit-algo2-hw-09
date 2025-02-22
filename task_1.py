import random
import math
import colorama
import numpy as np
import matplotlib.pyplot as plt
from colorama import Fore

colorama.init(autoreset=True)


def sphere_function(x):
    return sum(xi ** 2 for xi in x)


def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6):
    best_solution = [random.uniform(b[0], b[1]) for b in bounds]
    best_value = func(best_solution)
    history = [best_solution]

    for _ in range(iterations):
        candidate = [best_solution[i] + random.uniform(-0.1, 0.1) for i in
                     range(len(bounds))]
        candidate = [max(min(candidate[i], bounds[i][1]), bounds[i][0]) for i
                     in range(len(bounds))]
        candidate_value = func(candidate)

        if candidate_value < best_value:
            best_solution, best_value = candidate, candidate_value
            history.append(best_solution)

        if abs(best_value) < epsilon:
            break

    return best_solution, best_value, history


def random_local_search(func, bounds, iterations=1000, epsilon=1e-6):
    best_solution = [random.uniform(b[0], b[1]) for b in bounds]
    best_value = func(best_solution)
    history = [best_solution]

    for _ in range(iterations):
        candidate = [random.uniform(b[0], b[1]) for b in bounds]
        candidate_value = func(candidate)

        if candidate_value < best_value:
            best_solution, best_value = candidate, candidate_value
            history.append(best_solution)

        if abs(best_value) < epsilon:
            break

    return best_solution, best_value, history


def simulated_annealing(func, bounds, iterations=1000, temp=1000,
                        cooling_rate=0.95, epsilon=1e-6):
    current_solution = [random.uniform(b[0], b[1]) for b in bounds]
    current_value = func(current_solution)
    best_solution, best_value = current_solution, current_value
    history = [current_solution]

    for _ in range(iterations):
        candidate = [current_solution[i] + random.uniform(-0.5, 0.5) for i in
                     range(len(bounds))]
        candidate = [max(min(candidate[i], bounds[i][1]), bounds[i][0]) for i
                     in range(len(bounds))]
        candidate_value = func(candidate)

        delta = candidate_value - current_value
        if delta < 0 or math.exp(-delta / temp) > random.random():
            current_solution, current_value = candidate, candidate_value
            history.append(current_solution)

            if candidate_value < best_value:
                best_solution, best_value = candidate, candidate_value

        temp *= cooling_rate
        if temp < epsilon:
            break

    return best_solution, best_value, history


if __name__ == "__main__":
    bounds = [(-5, 5), (-5, 5)]

    print(Fore.YELLOW + "Hill Climbing:")
    hc_solution, hc_value, hc_history = hill_climbing(sphere_function, bounds)
    print(Fore.GREEN + "Solution:", hc_solution, Fore.CYAN + "Value:",
          hc_value)

    print(Fore.YELLOW + "\nRandom Local Search:")
    rls_solution, rls_value, rls_history = random_local_search(sphere_function,
                                                               bounds)
    print(Fore.GREEN + "Solution:", rls_solution, Fore.CYAN + "Value:",
          rls_value)

    print(Fore.YELLOW + "\nSimulated Annealing:")
    sa_solution, sa_value, sa_history = simulated_annealing(sphere_function,
                                                            bounds)
    print(Fore.GREEN + "Solution:", sa_solution, Fore.CYAN + "Value:",
          sa_value)

    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection="3d")

    x = np.linspace(bounds[0][0], bounds[0][1], 100)
    y = np.linspace(bounds[1][0], bounds[1][1], 100)
    X, Y = np.meshgrid(x, y)
    Z = X ** 2 + Y ** 2

    ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.6)


    def plot_trajectory(history, color, label):
        points = np.array(history)
        sampled_points = points[::max(1,
                                      len(points) // 20)]
        ax.plot(
            sampled_points[:, 0],
            sampled_points[:, 1],
            [sphere_function(p) for p in sampled_points],
            color=color,
            marker="o",
            label=label,
        )


    plot_trajectory(hc_history, "red", "Hill Climbing")
    plot_trajectory(rls_history, "blue", "Random Local Search")
    plot_trajectory(sa_history, "green", "Simulated Annealing")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z (Sphere Function Value)")
    ax.set_title("Optimization Search for Sphere Function")
    ax.legend()
    plt.show()



