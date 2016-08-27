import noise


def generate_simplex(filename, size, seed=0):
    x = size // 2

    # TODO: Make the value higher the farther away from the center it is
    # Therefore the map will be bounded by solid rock
    lines = []
    for j in range(size):
        line = []
        for i in range(size):
            value = noise.snoise2(i/25 + seed, j/25 + seed)
            if value < -0.6:
                line.append('W')
            elif value < -0.4:
                line.append('T')
            elif value < 0.5:
                line.append('G')
            elif value < 1.0:
                line.append('S')
            else:
                line.append('B')
        lines.append(line)

    # Place the pyramid in the center

    # Center
    lines[x][x] = 'P'
    lines[x][x+1] = 'P'
    lines[x+1][x+1] = 'P'
    lines[x+1][x] = 'P'

    # North
    lines[x+2][x] = 'P'
    lines[x+2][x+1] = 'P'
    lines[x+2][x-1] = 'P'
    lines[x+2][x+2] = 'P'
    lines[x+3][x] = 'P'
    lines[x+3][x+1] = 'P'

    # South
    lines[x-1][x] = 'P'
    lines[x-1][x+1] = 'P'
    lines[x-1][x-1] = 'P'
    lines[x-1][x+2] = 'P'
    lines[x-2][x] = 'P'
    lines[x-2][x+1] = 'P'

    # East
    lines[x][x-1] = 'P'
    lines[x+1][x-1] = 'P'
    lines[x-1][x-1] = 'P'
    lines[x+2][x-1] = 'P'
    lines[x][x-2] = 'P'
    lines[x+1][x-2] = 'P'

    # West
    lines[x][x+2] = 'P'
    lines[x+1][x+2] = 'P'
    lines[x-1][x+2] = 'P'
    lines[x+2][x+2] = 'P'
    lines[x][x+3] = 'P'
    lines[x+1][x+3] = 'P'

    # Write to file
    with open(filename, 'w') as outfile:
        outfile.writelines("".join(line) + '\n' for line in lines)
