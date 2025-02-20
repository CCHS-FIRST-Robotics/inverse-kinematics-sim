from TwoJointArm import TwoJointArm
from Translation2d import Translation2d
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import math

# Create arm instance
elbow_length = 25
wrist_length = 6
arm = TwoJointArm(elbow_length, wrist_length)

# Tooltip position (x, y)
x = 10
y = 30

# Define elevator height bounds
ELEVATOR_MIN = 47
ELEVATOR_MAX = 91

# Get all possible solutions
solutions = arm.calculate_angles(Translation2d(x, y), ELEVATOR_MIN, ELEVATOR_MAX)
if not solutions:
    print("NO SOLUTIONS")
    exit()

# Track the current solution index
current_index = 0

# Set up a **single** figure with two subplots
fig, (ax_all, ax_one) = plt.subplots(1, 2, figsize=(12, 6))
plt.subplots_adjust(wspace=0.3)  # Add space between the two plots

def plot_arm(ax, q1, q2, elevator_height, highlight=False):
    """Plots the arm at given angles and elevator height."""
    base_x = 0
    base_y = elevator_height

    elbow_x = base_x + math.cos(q1) * arm.elbow_length
    elbow_y = base_y + math.sin(q1) * arm.elbow_length
    wrist_x = elbow_x + math.cos(q1 + q2) * arm.wrist_length
    wrist_y = elbow_y + math.sin(q1 + q2) * arm.wrist_length

    lw = 5 if highlight else 1
    arm_color = "orange" if highlight else "black"
    
    ax.plot([base_x, elbow_x], [base_y, elbow_y], color=arm_color, linewidth=lw)
    ax.plot([elbow_x, wrist_x], [elbow_y, wrist_y], color="red" if highlight else "blue", linewidth=lw)

    ax.plot([base_x, base_x], [0, base_y], color="green", linestyle="--", linewidth=2 if highlight else 1)
    ax.scatter([wrist_x], [wrist_y], color="purple", s=200 if highlight else 80, alpha=0.8, edgecolors="black")

def update_plots():
    """Updates both plots when switching solutions."""
    global current_index
    ax_all.clear()
    ax_one.clear()

    for i, (q1, q2, elevator_height) in enumerate(solutions):
        plot_arm(ax_all, q1, q2, elevator_height, highlight=(i == current_index))

    q1, q2, elevator_height = solutions[current_index]
    plot_arm(ax_one, q1, q2, elevator_height, highlight=True)

    ax_all.set_title("All Solutions")
    ax_all.set_xlim(-x - 20 , x + 20)
    ax_all.set_ylim(0, y + 40)

    ax_one.set_title(f"Selected Solution {current_index+1}")
    ax_one.set_xlim(-x - 20, x + 20)
    ax_one.set_ylim(0, y + 40)

    fig.canvas.draw()

def next_solution(event):
    global current_index
    current_index = (current_index + 1) % len(solutions)
    update_plots()

# Initial plot setup
update_plots()

# Button for switching solutions
button_ax = fig.add_axes([0.4, 0.02, 0.2, 0.05])  
button = widgets.Button(button_ax, "Next Solution")
button.on_clicked(next_solution)

plt.show()
