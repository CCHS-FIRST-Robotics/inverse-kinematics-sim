from typing import List
from Translation2d import Translation2d
import math

class TwoJointArm:
    def __init__(self, elbow_length: float, wrist_length: float) -> None:
        self.elbow_length = elbow_length
        self.wrist_length = wrist_length

    def calculate_angles(self, tooltip_position: Translation2d, elevator_min: int, elevator_max: int, elbow_max: float, elbow_max_max: float) -> List[List[float]]:
        x, y = tooltip_position.x, tooltip_position.y
        solutions = []
        denied_solutions = []

        for elevator_height in range(elevator_min, elevator_max + 1):
            adjusted_y = y - elevator_height
            r = math.sqrt(x**2 + adjusted_y**2)

            if r > self.elbow_length + self.wrist_length or r < abs(self.elbow_length - self.wrist_length):
                print(f"Position ({x}, {y}) unreachable for elevator height {elevator_height}")
                continue  # Skip unreachable positions

            cos_q2 = (r**2 - self.elbow_length**2 - self.wrist_length**2) / (2 * self.elbow_length * self.wrist_length)
            cos_q2 = max(-1, min(1, cos_q2))  # Clamp to avoid math errors
            q2 = math.degrees(math.acos(cos_q2))  # Convert to degrees
            q2_neg = 360 - q2  # Ensure q2 is within 0-360 range

            for q2_val in [q2, q2_neg]:  # Try both solutions
                k1 = self.elbow_length + self.wrist_length * math.cos(math.radians(q2_val))
                k2 = self.wrist_length * math.sin(math.radians(q2_val))
                q1 = math.degrees(math.atan2(adjusted_y, x) - math.atan2(k2, k1))  # Convert to degrees
                q1 = q1 % 360  # Ensure q1 is within 0-360 range

                # Run FK to verify correctness
                fk_x, fk_y = self.forward_kinematics(math.radians(q1), math.radians(q2_val), elevator_height)

                if (fk_x, fk_y) == (round(x, 2), round(y, 2)):  
                    if q1 > elbow_max:  
                        denied_solutions.append([q1, q2_val, elevator_height])
                        print(f"Denied due to angle limit: q1={q1:.2f}°, q2={q2_val:.2f}°, elevator={elevator_height}")
                    elif elevator_height > elevator_min + 1 and q1 <= elbow_max_max:
                        solutions.append([q1, q2_val, elevator_height])
                    else:
                        denied_solutions.append([q1, q2_val, elevator_height])
                        print(f"Denied due to angle limit: q1={q1:.2f}°, q2={q2_val:.2f}°, elevator={elevator_height}")
                else:
                    denied_solutions.append([q1, q2_val, elevator_height])
                    print(f"Denied by FK: q1={q1:.2f}°, q2={q2_val:.2f}°, elevator={elevator_height} -> FK ({fk_x}, {fk_y}) != ({round(x, 2)}, {round(y, 2)})")

        print("\nFinal valid solutions:")
        for sol in solutions:
            print(f"q1={sol[0]:.2f}°, q2={sol[1]:.2f}°, elevator={sol[2]}")
        print("\nDenied solutions:")
        for dsol in denied_solutions:
            print(f"q1={dsol[0]:.2f}°, q2={dsol[1]:.2f}°, elevator={dsol[2]}")

        return solutions, denied_solutions

    def forward_kinematics(self, q1, q2, elevator_height):
        """ Compute (x, y) position given joint angles (in radians) and elevator height """
        elbow_x = math.cos(q1) * self.elbow_length
        elbow_y = elevator_height + math.sin(q1) * self.elbow_length
        wrist_x = elbow_x + math.cos(q1 + q2) * self.wrist_length
        wrist_y = elbow_y + math.sin(q1 + q2) * self.wrist_length

        return round(wrist_x, 2), round(wrist_y, 2)  # Round to avoid floating-point issues
