import numpy as np
import re

def parse_gcode(filepath):
    time_array = []
    position_array = []

    # Current state
    x = y = z = 0.0
    feedrate = 1000.0  # mm/min default
    current_time = 0.0

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()

            # Skip comments
            if line.startswith(";") or line == "":
                continue

            # Extract feedrate if present
            f_match = re.search(r'F([-+]?[0-9]*\.?[0-9]+)', line)
            if f_match:
                feedrate = float(f_match.group(1))

            # Only process motion commands
            if line.startswith(("G0", "G1")):

                new_x, new_y, new_z = x, y, z

                x_match = re.search(r'X([-+]?[0-9]*\.?[0-9]+)', line)
                y_match = re.search(r'Y([-+]?[0-9]*\.?[0-9]+)', line)
                z_match = re.search(r'Z([-+]?[0-9]*\.?[0-9]+)', line)

                if x_match:
                    new_x = float(x_match.group(1))
                if y_match:
                    new_y = float(y_match.group(1))
                if z_match:
                    new_z = float(z_match.group(1))

                # Distance traveled
                dist = np.sqrt((new_x - x)**2 + (new_y - y)**2 + (new_z - z)**2)

                # Convert feedrate mm/min → mm/sec
                speed = feedrate / 60.0

                # Time step
                if speed > 0:
                    dt = dist / speed
                else:
                    dt = 0

                current_time += dt

                # Save data
                time_array.append(current_time)
                position_array.append([new_x, new_y, new_z])

                # Update current position
                x, y, z = new_x, new_y, new_z

    return np.array(time_array), np.array(position_array)


if __name__ == "__main__":
    time_array, position_array = parse_gcode("example.gcode")

    print("Times:")
    print(time_array)

    print("\nPositions:")
    print(position_array)
