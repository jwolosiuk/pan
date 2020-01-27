counter = 0
for a in range(5):
    for b in range(5):
        for c in range(5):
            for d in range(5):
                for e in range(5):
                    for f in range(5):
                        if (a+b+c+d+e+f) == 12:
                            counter+=1
print(counter)
