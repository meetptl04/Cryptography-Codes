def generate_matrix(key):
    key = "".join(dict.fromkeys(key.upper().replace('J','I')+'ABCDEFGHIKLMNOPQRSTUVWXYZ'))
    return [list(key[i:i+5]) for i in range(0,25,5)]

def findposition(matrix,letter):
    for r,row in enumerate(matrix):
        if letter in row:
            return r,row.index(letter)

def playfair_encrypt(text,key):
    text = text.upper().replace('J','I').replace(" ",'')
    if len(text)%2 : text += 'X'
    matrix = generate_matrix(key)
    encrypted = ""
    for i in range(0,len(text),2):
        r1,c1 = findposition(matrix,text[i])
        r2,c2 = findposition(matrix,text[i+1])
        if r1 == r2 :
            encrypted += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2 :
            encrypted += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else:
            encrypted += matrix[r1][c2] + matrix[r2][c1]
    return encrypted

def playfair_decrypt(text, key):
    matrix = generate_matrix(key)
    decrypted = ""

    for i in range(0, len(text), 2):
        r1, c1 = findposition(matrix, text[i])
        r2, c2 = findposition(matrix, text[i+1])
        if r1 == r2:
            decrypted += matrix[r1][(c1-1) % 5] + matrix[r2][(c2-1) % 5]
        elif c1 == c2:
            decrypted += matrix[(r1-1) % 5][c1] + matrix[(r2-1) % 5][c2]
        else:
            decrypted += matrix[r1][c2] + matrix[r2][c1]
            
    if decrypted[-1] == "X":
        decrypted = decrypted[:-1]

    return decrypted
