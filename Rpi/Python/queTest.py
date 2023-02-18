from collections import deque

que = deque([])

for x in range(10):
    z = []
    z.append(x)
    que.append(z)
    if len(que) > 2:
        que.popleft()
    print(que)
    z.clear()