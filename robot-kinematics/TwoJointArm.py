from typing import List
from Translation2d import Translation2d
import math

class TwoJointArm:
    def __init__(self, elbow_length: float, wrist_length: float) -> None:
        self.elbow_length = elbow_length
        self.wrist_length = wrist_length

    def calculate_angles(self, tooltip_position: Translation2d, elevator_min: int, elevator_max: int) -> List[List[float]]:
        x, y = tooltip_position.x, tooltip_position.y
        solutions = []

        for elevator_height in range(elevator_min, elevator_max + 1):
            adjusted_y = y - elevator_height
            r = math.sqrt(x**2 + adjusted_y**2)

            if r > self.elbow_length + self.wrist_length or r < abs(self.elbow_length - self.wrist_length):
                continue  # Skip unreachable positions

            cos_q2 = (r**2 - self.elbow_length**2 - self.wrist_length**2) / (2 * self.elbow_length * self.wrist_length)
            cos_q2 = max(-1, min(1, cos_q2))  # Clamp to avoid math errors
            q2 = math.acos(cos_q2)
            q2_neg = -q2

            for q2_val in [q2, q2_neg]:  # Try both solutions
                k1 = self.elbow_length + self.wrist_length * math.cos(q2_val)
                k2 = self.wrist_length * math.sin(q2_val)
                q1 = math.atan2(adjusted_y, x) - math.atan2(k2, k1)

                # Run FK to verify correctness
                if self.forward_kinematics(q1, q2_val, elevator_height) == (x, y):
                    solutions.append([q1, q2_val, elevator_height])

        return solutions

    def forward_kinematics(self, q1, q2, elevator_height):
        """ Compute (x, y) position given joint angles and elevator height """
        elbow_x = math.cos(q1) * self.elbow_length
        elbow_y = elevator_height + math.sin(q1) * self.elbow_length
        wrist_x = elbow_x + math.cos(q1 + q2) * self.wrist_length
        wrist_y = elbow_y + math.sin(q1 + q2) * self.wrist_length

        return round(wrist_x, 2), round(wrist_y, 2)  # Round to avoid floating-point issues
