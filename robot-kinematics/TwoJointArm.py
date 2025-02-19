from typing import List
from Translation2d import Translation2d
import math

class TwoJointArm:
    def __init__(self, elbow_length: float, wrist_length: float) -> None:
        self.elbow_length = elbow_length
        self.wrist_length = wrist_length

    def calculate_angles(self, tooltip_position: Translation2d) -> List[List[float]]:
        x, y = tooltip_position.x, tooltip_position.y
        elevator_height = y  # Keep track of height

        # ✅ Adjust Y to include elevator height
        adjusted_y = y - elevator_height  

        # Compute r (distance from base)
        r = math.sqrt(x**2 + adjusted_y**2)

        print(f"Target Position: ({x}, {y})")
        print(f"Computed Distance (r): {r}")
        print(f"Reachable Range: {abs(self.elbow_length - self.wrist_length)} to {self.elbow_length + self.wrist_length}")

        # Check reachability
        if r > self.elbow_length + self.wrist_length or r < abs(self.elbow_length - self.wrist_length):
            print("ERROR: Target out of reach")
            return []  # No valid solutions

        ## POSITIVE SOLUTION ##
        cos_q2 = (r**2 - self.elbow_length**2 - self.wrist_length**2) / (2 * self.elbow_length * self.wrist_length)
        
        # ✅ Clamp `cos_q2` to avoid math domain errors
        cos_q2 = max(-1, min(1, cos_q2))
        
        if cos_q2 < -1 or cos_q2 > 1:
            print("ERROR: cos_q2 out of range. No solution.")
            return []

        q2 = math.acos(cos_q2)  # Wrist joint angle

        # Calculate q1
        k1 = self.elbow_length + self.wrist_length * math.cos(q2)
        k2 = self.wrist_length * math.sin(q2)
        q1 = math.atan2(adjusted_y, x) - math.atan2(k2, k1)

        # Store the solution
        solutions = [[q1, q2, elevator_height]]

        ## NEGATIVE SOLUTION ##
        q2_neg = -q2  # Flip wrist angle

        k1_neg = self.elbow_length + self.wrist_length * math.cos(q2_neg)
        k2_neg = self.wrist_length * math.sin(q2_neg)
        q1_neg = math.atan2(adjusted_y, x) - math.atan2(k2_neg, k1_neg)

        solutions.append([q1_neg, q2_neg, elevator_height])

        return solutions
