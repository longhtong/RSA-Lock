#Encrypt NumMess
#NumMess: an integer value
#N: product of two prime numbers
#e: a number that is coprime to the two numbers
def encrypt(NumMess, N, e):
    if N == 0:
        raise TypeError("Invalid N value.")
    return pow(NumMess, e, N)
    #(NumMess**e) % N
    

