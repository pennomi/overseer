import noise


def generate_simplex(filename, w, h):
    # TODO: Make the value higher the farther away from the center it is
    # Therefore the map will be bounded by solid rock
    lines = []
    for y in range(h):
        line = ""
        for x in range(w):
            value = noise.snoise2(x/50, y/50)
            if value < -0.4:
                line += 'W'
            elif value < -0.1:
                line += 'T'
            elif value < 0.3:
                line += 'G'
            elif value < 0.7:
                line += 'S'
            elif value <= 1.0:
                line += 'B'
            else:
                raise AssertionError()
        lines.append(line + '\n')
    with open(filename, 'w') as outfile:
        outfile.writelines(lines)
