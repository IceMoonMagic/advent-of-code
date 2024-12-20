A = 0o150213210
B, C = 0, 0

out = []


def main():
    global A, B, C
    B = A % 8
    B = B ^ 2
    C = A // 2**B
    A = A // 2**3
    B = B ^ 7
    B = B ^ C
    out.append(B % 8)
    if A != 0:
        main()
    else:
        print(out)


if __name__ == "__main__":
    main()
