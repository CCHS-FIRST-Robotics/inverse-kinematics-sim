import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from TwoJointArm import TwoJointArm
from Translation2d import Translation2d
import math

# Arm parameters
elbow_length = 30
wrist_length = 20
elevator_min = 47
elevator_max = 91
elbow_max = 180
elbow_max_max = 360

# Initialize arm
arm = TwoJointArm(elbow_length, wrist_length)

# Define target position
tooltip_position = Translation2d(30, 60)

# Get valid and denied solutions
solutions, denied_solutions = arm.calculate_angles(tooltip_position, elevator_min, elevator_max, elbow_max, elbow_max_max)

# Initialize plot
fig, (ax_all, ax_one) = plt.subplots(1, 2, figsize=(12, 6))
plt.subplots_adjust(bottom=0.2)  # Make space for buttons
current_index = 0

def plot_arm(ax, q1, q2, elevator_height, arm1_color="black", arm2_color="blue", highlight=False):
    """ Plots the arm given angles and elevator height """
    elbow_x = elbow_length * math.cos(math.radians(q1))
    elbow_y = elevator_height + elbow_length * math.sin(math.radians(q1))
    
    wrist_x = elbow_x + wrist_length * math.cos(math.radians(q1 + q2))
    wrist_y = elbow_y + wrist_length * math.sin(math.radians(q1 + q2))
    
    lw = 2 + (3 if highlight else 0)  # Increase line width if highlighted

    # Elevator (green dashed)
    ax.plot([0, 0], [0, elevator_height], 'g--', linewidth=2)

    # Plot arm segments
    ax.plot([0, elbow_x], [elevator_height, elbow_y], marker="o", color=arm1_color, lw=lw, markersize=5)
    ax.plot([elbow_x, wrist_x], [elbow_y, wrist_y], marker="o", color=arm2_color, lw=lw, markersize=5)

    # Highlight joint if selected
    if highlight:
        ax.plot(wrist_x, wrist_y, 'o', color='red', markersize=8, markerfacecolor="purple")

def update_plots():
    """ Updates both plots when switching solutions """
    global current_index
    ax_all.clear()
    ax_one.clear()

    # Plot all valid solutions
    for i, (q1, q2, elevator_height) in enumerate(solutions):
        arm1_color = "black"
        arm2_color = "blue"
        if i == current_index:
            arm1_color = "orange"
            arm2_color = "orange"
        plot_arm(ax_all, q1, q2, elevator_height, arm1_color, arm2_color, highlight=(i == current_index))

    # Plot all denied solutions in red
    for q1, q2, elevator_height in denied_solutions:
        plot_arm(ax_all, q1, q2, elevator_height, arm1_color="red", arm2_color="red")

    # Plot only the selected valid solution
    q1, q2, elevator_height = solutions[current_index]
    plot_arm(ax_one, q1, q2, elevator_height, arm1_color="orange", arm2_color="orange", highlight=True)

    ax_all.set_title("All Solutions")
    ax_all.set_xlim(-50, 50)
    ax_all.set_ylim(0, 100)

    ax_one.set_title(f"Selected Solution {current_index+1}")
    ax_one.set_xlim(-50, 50)
    ax_one.set_ylim(0, 100)

    fig.canvas.draw()

def next_solution(event):
    """ Switch to next solution """
    global current_index
    current_index = (current_index + 1) % len(solutions)
    update_plots()

def prev_solution(event):
    """ Switch to previous solution """
    global current_index
    current_index = (current_index - 1) % len(solutions)
    update_plots()

# Add Buttons
ax_prev = plt.axes([0.3, 0.05, 0.15, 0.075])  # Position for "Previous" button
ax_next = plt.axes([0.55, 0.05, 0.15, 0.075])  # Position for "Next" button

btn_prev = Button(ax_prev, "Previous Solution")
btn_next = Button(ax_next, "Next Solution")

btn_prev.on_clicked(prev_solution)
btn_next.on_clicked(next_solution)

update_plots()
plt.show()
