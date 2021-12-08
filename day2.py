def apply_command(x: int, y: int, command: str):
    command, units = command.split()
    units = int(units)
    if command == "forward":
        x += units
    elif command == "up":
        y -= units
    elif command == "down":
        y += units
    else:
        raise ValueError(f"Unknown command: {command}")
    return x, y

def apply_command_fixed(x: int, y: int, phi: int, command: str):
    command, units = command.split()
    units = int(units)
    if command == "forward":
        x += units
        y += units * phi
    elif command == "down":
        phi += units
    elif command == "up":
        phi -= units
    else:
        raise ValueError(f"Unknown command: {command}")
    return x, y, phi


with open("day2.txt", "r") as f:
    commands = [c.strip() for c in f.readlines()]

x, y = 0, 0
for command in commands:
    x, y = apply_command(x, y, command)
print(x * y)

x, y, phi = 0, 0, 0
for command in commands:
    x, y, phi = apply_command_fixed(x, y, phi, command)
print(x * y)
