def main():
    interpolat0r = Interpolat0r()
    print("### horizontalish Line ###")
    ips = interpolat0r.interpolate(10, 0, 20.4, 2)
    print(ips)


class Interpolat0r:
    def __init__(self):
        self = self

    def interpolate(self, i0, d0, i1, d1):
        i0 = int(i0)
        i1 = int(i1)
        if i0 == i1:
            return [d0]
        values = []

        a = (d1 - d0) / (i1 - i0)
        d = d0
        print(i0, i1)
        for i in range(i0, i1):
            # values.append(int(d))
            values.append(d)
            d = d + a

        return values


if __name__ == "__main__":
    main()
