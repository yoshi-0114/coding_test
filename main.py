def main():
    N, C = map(int, input().split())
    vw = [tuple(map(int, input().split())) for _ in range(N)]

    dp = [0] * (C + 1)

    for i in range(N):
        v, w = vw[i]
        for j in range(C, v - 1, -1):
            dp[j] = max(dp[j], dp[j-v] + w)

    print(dp[C])

if __name__ == "__main__":
    main()
