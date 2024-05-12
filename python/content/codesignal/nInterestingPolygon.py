"""
    n=1 -> 1
    n=2 -> 5
    n=3 -> 13
    n=4 -> 25
"""
# Primera iteración correcta:
def solution(n):
    if n == 1:
        return 1
    elif n == 2:
        return 5
    else:        
        return 2*(n+(n-1))-1 + 2*((n-1)*(n-2))

# Segunda iteración correcta:
def solution(n):
    if n == 1:
        return 1
    elif n == 2:
        return 5
    else:        
        return 2*n**2 - 2*n + 1

# Tercera iteración correcta, simplificada por chatGPT:
def solution(n):
    return n**2 + (n - 1)**2