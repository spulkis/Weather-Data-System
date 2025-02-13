#Return a length of a given number without using len
def count_length(number: int):
    numberx = str(number)
    cnt = 0
    for c in numberx:
        cnt = cnt + 1
    print(cnt)

count_length(100)