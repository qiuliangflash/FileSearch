
def  getIntegerComplement( n):
    binary = 1
    number = 0
    while binary <= n:
        number = number + binary
        binary = binary * 2
    return n ^ number

print getIntegerComplement(2)
print getIntegerComplement(0)
print getIntegerComplement(100000)
