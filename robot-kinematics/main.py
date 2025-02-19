from TwoJointArm import TwoJointArm
from Translation2d import Translation2d
import matplotlib.pyplot as plt
import math
import numpy as np

# Create arm instance
arm = TwoJointArm(25, 6)

# Tooltip position (x, y)
x = 30
y = 60

# Compute angles and elevator height
solutions = arm.calculate_angles(Translation2d(x, y))

# Set up plot
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

def plot_arm(ax, q1, q2, elevator_height, title):
    base_x = 0
    base_y = elevator_height

    elbow_x = base_x + math.cos(q1) * arm.elbow_length
    elbow_y = base_y + math.sin(q1) * arm.elbow_length
    wrist_x = elbow_x + math.cos(q1 + q2) * arm.wrist_length
    wrist_y = elbow_y + math.sin(q1 + q2) * arm.wrist_length

    # Plot arm segments
    ax.plot([base_x, elbow_x], [base_y, elbow_y], color="blue", linewidth=2, label="Upper Arm")
    ax.plot([elbow_x, wrist_x], [elbow_y, wrist_y], color="red", linewidth=2, label="Forearm")

    # Plot elevator
    ax.plot([base_x, base_x], [0, base_y], color="green", linestyle="--", label=f'Elevator Height = {elevator_height}')

    # Convert angles to degrees (0-360 format)
    q1_deg = round(math.degrees(q1), 2) % 360  
    q2_deg = round(math.degrees(q2), 2) % 360  

    # Draw proper long-path angle arcs
    arc1_x, arc1_y = draw_angle_arc(ax, base_x, base_y, q1_deg, radius=5, color="blue")
    arc2_x, arc2_y = draw_angle_arc(ax, elbow_x, elbow_y, q2_deg, base_angle=q1_deg, radius=3, color="red")  

    # Adjust text to be near arcs
    ax.text(arc1_x, arc1_y, f"q1 = {q1_deg}°", fontsize=12, color="blue", ha='center', va='bottom')
    ax.text(arc2_x, arc2_y, f"q2 = {q2_deg}°", fontsize=12, color="red", ha='center', va='bottom')

    # Set title and legend
    ax.set_title(title)
    ax.legend()

    print(f"{title} -> q1: {q1_deg:.2f}°, q2: {q2_deg:.2f}°")
    print(f"Expected End-Effector: ({x}, {y})")
    print(f"Calculated End-Effector: ({wrist_x:.2f}, {wrist_y:.2f})\n")

def draw_angle_arc(ax, center_x, center_y, angle, base_angle=0, radius=3, color="black"):
    """ Draws an arc following the **long path**, properly oriented """

    start_angle = base_angle  # Start from base
    end_angle = start_angle + angle  # Ensure long path
    angle_range = np.linspace(start_angle, end_angle, 50)  

    arc_x = center_x + radius * np.cos(np.radians(angle_range))
    arc_y = center_y + radius * np.sin(np.radians(angle_range))
    
    # Plot arc
    ax.plot(arc_x, arc_y, color=color, linestyle="--")

    # Label placement at 1/3rd of arc
    label_idx = len(angle_range) // 3
    return arc_x[label_idx], arc_y[label_idx]

# Plot both positive and negative solutions
plot_arm(axes[0], solutions[0][0], solutions[0][1], solutions[0][2], f"X = {x}, Y = {y} POSITIVE")
plot_arm(axes[1], solutions[1][0], solutions[1][1], solutions[1][2], f"X = {x}, Y = {y} NEGATIVE")

# Show plot
plt.show()
