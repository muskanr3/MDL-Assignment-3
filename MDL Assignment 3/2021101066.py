import numpy as np

difference = 0.0001
stepCost = -0.04
pDirection = 0.7
pPerpendcular = 0.15
gamma = 0.95

grid = np.array([[0, 1, -1],
                 [0, 0, 0], 
                 [0, 9, 0], 
                 [0, 0, 0]])

prev_utility = np.array(
    [[0.0, 1.0, -1.0], [0.0, 0.0, 0.0], [0.0, 9.0, 0.0], [0.0, 0.0, 0.0]]
)
curr_utility = np.array(
    [[0.0, 1.0, -1.0], [0.0, 0.0, 0.0], [0.0, 9.0, 0.0], [0.0, 0.0, 0.0]]
)
policy = np.array([["", "X", "X"], ["", "", ""], ["", "X", ""], ["", "", ""]])
# in policy: up = U, right = R, down = D, left = L, penalty, reward and wall have a policy of X

print("UTILITY VALUES:")
iterations = 0
while 1:
    iterations += 1

    for i in range(4):
        for j in range(3):
            if (i == 0 and j == 1) or (i == 0 and j == 2) or (i == 2 and j == 1):
                continue

            # up dir
            summationUp = 0
            if ((i - 1) < 0) or ((i - 1) == 2 and j == 1):
                summationUp += prev_utility[i][j] * pDirection
            else:
                summationUp += prev_utility[i - 1][j] * pDirection
            if ((j - 1) < 0) or (i == 2 and (j - 1) == 1):
                summationUp += prev_utility[i][j] * pPerpendcular
            else:
                summationUp += prev_utility[i][j - 1] * pPerpendcular
            if ((j + 1) > 2) or (i == 2 and (j + 1) == 1):
                summationUp += prev_utility[i][j] * pPerpendcular
            else:
                summationUp += prev_utility[i][j + 1] * pPerpendcular

            # down dir
            summationDown = 0
            if ((i + 1) > 3) or ((i + 1) == 2 and j == 1):
                summationDown += prev_utility[i][j] * pDirection
            else:
                summationDown += prev_utility[i + 1][j] * pDirection
            if ((j - 1) < 0) or (i == 2 and (j - 1) == 1):
                summationDown += prev_utility[i][j] * pPerpendcular
            else:
                summationDown += prev_utility[i][j - 1] * pPerpendcular
            if ((j + 1) > 2) or (i == 2 and (j + 1) == 1):
                summationDown += prev_utility[i][j] * pPerpendcular
            else:
                summationDown += prev_utility[i][j + 1] * pPerpendcular

            # left dir
            summationLeft = 0
            if ((i + 1) > 3) or ((i + 1) == 2 and j == 1):
                summationLeft += prev_utility[i][j] * pPerpendcular
            else:
                summationLeft += prev_utility[i + 1][j] * pPerpendcular
            if ((j - 1) < 0) or (i == 2 and (j - 1) == 1):
                summationLeft += prev_utility[i][j] * pDirection
            else:
                summationLeft += prev_utility[i][j - 1] * pDirection
            if ((i - 1) < 0) or ((i - 1) == 2 and j == 1):
                summationLeft += prev_utility[i][j] * pPerpendcular
            else:
                summationLeft += prev_utility[i - 1][j] * pPerpendcular

            # right dir
            summationRight = 0
            if ((i + 1) > 3) or ((i + 1) == 2 and j == 1):
                summationRight += prev_utility[i][j] * pPerpendcular
            else:
                summationRight += prev_utility[i + 1][j] * pPerpendcular
            if ((i - 1) < 0) or ((i - 1) == 2 and j == 1):
                summationRight += prev_utility[i][j] * pPerpendcular
            else:
                summationRight += prev_utility[i - 1][j] * pPerpendcular
            if ((j + 1) > 2) or (i == 2 and (j + 1) == 1):
                summationRight += prev_utility[i][j] * pDirection
            else:
                summationRight += prev_utility[i][j + 1] * pDirection

            direction = max(summationDown, summationLeft, summationRight, summationUp)

            if direction == summationUp:
                policy[i][j] = "U"
            elif direction == summationRight:
                policy[i][j] = "R"
            elif direction == summationDown:
                policy[i][j] = "D"
            else:
                policy[i][j] = "L"

            curr_utility[i][j] = max(
                (stepCost + gamma * summationUp),
                (stepCost + gamma * summationDown),
                (stepCost + gamma * summationLeft),
                (stepCost + gamma * summationRight),
            )

            curr_utility[i][j] = stepCost + gamma * direction

    flag = 0
    print("iteration = ", iterations)
    for i in range(4):
        for j in range(3):
            print("%.8f" % curr_utility[i][j], end=" ")
        print()
    print("---------------------------------------")

    for i in range(4):
        for j in range(3):
            if abs(prev_utility[i][j] - curr_utility[i][j]) > difference:
                prev_utility = np.copy(curr_utility)
                flag = 1
                break
        if flag == 1:
            break
    if flag == 0:
        break

print("No. of iterations: ", iterations)
print("Policy =")
print(policy)
