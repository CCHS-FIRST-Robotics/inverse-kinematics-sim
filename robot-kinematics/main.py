from TwoJointArm import TwoJointArm
from Translation2d import Translation2d
import matplotlib.pyplot as plt
import math
import numpy as np

# Create arm instance
elbow_length = 25
wrist_length = 6
arm = TwoJointArm(elbow_length, wrist_length)

# Tooltip position (x, y)
x = 5
y = 20

# Define elevator height bounds
ELEVATOR_MIN = 47
ELEVATOR_MAX = 91

# Get all possible solutions
solutions = arm.calculate_angles(Translation2d(x, y), ELEVATOR_MIN, ELEVATOR_MAX)

# Set up plot
fig, ax = plt.subplots(figsize=(8, 8))

def plot_arm(ax, q1, q2, elevator_height, label):
    base_x = 0
    base_y = elevator_height

    elbow_x = base_x + math.cos(q1) * arm.elbow_length
    elbow_y = base_y + math.sin(q1) * arm.elbow_length
    wrist_x = elbow_x + math.cos(q1 + q2) * arm.wrist_length
    wrist_y = elbow_y + math.sin(q1 + q2) * arm.wrist_length

    # Plot arm segments
    ax.plot([base_x, elbow_x], [base_y, elbow_y], color="blue", linewidth=2, label=f"{label} (Upper Arm)")
    ax.plot([elbow_x, wrist_x], [elbow_y, wrist_y], color="red", linewidth=2, label=f"{label} (Forearm)")

    # Plot elevator height
    ax.plot([base_x, base_x], [0, base_y], color="green", linestyle="--", label=f'Elevator {elevator_height}')

    # **🟣 Add an opaque dot (purple) for the expected end-effector position**
    ax.scatter([x], [y], color="purple", s=120, alpha=0.8, edgecolors="black", label="Expected Position")

    # Convert angles to degrees
    q1_deg = round(math.degrees(q1), 2) % 360  
    q2_deg = round(math.degrees(q2), 2) % 360  

    print(f"Elevator Height {elevator_height} -> q1: {q1_deg:.2f}°, q2: {q2_deg:.2f}°")
    print(f"Expected End-Effector: ({x}, {y})")
    print(f"Calculated End-Effector: ({wrist_x:.2f}, {wrist_y:.2f})\n")


# Plot all solutions
if len(solutions)== 0:
    print("NO SOLUTIONS")
    exit()
for i, (q1, q2, elevator_height) in enumerate(solutions):
    plot_arm(ax, q1, q2, elevator_height, label=f"Sol {i+1}")


# Set plot limits
ax.set_xlim(-50, 50)
ax.set_ylim(0, 100)
ax.set_xlabel("X Position")
ax.set_ylabel("Y Position")
ax.set_title("All Possible Arm Solutions")
ax.legend()
plt.show()
