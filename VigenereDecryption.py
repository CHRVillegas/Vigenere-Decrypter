ENGLISH_FREQUENCIES = [.082,.015,.028,.043,.127,.022,.020,.061,.070,.002,.008,.040,.024,.067,.015,.019,.001,.060,.063,.091,.028,.010,.024,.002,.020,.001]

def maxId(list):                                                                    #Iterates through given list and returns index from that list that holds that represents the largest value in that list
    max_index = 0                                                                   #Considering single for-loop completion, operates in O(n) time
    max_int = 0
    for id, val in enumerate(list):
        if max_int < val:
            max_int = val
            max_index = id
    return max_index

def score(frequencies):                                                             #Aquires frequency of different characters found in the ciphertext
    length = sum(frequencies)                                                       #Operates over single list, O(n) time
    return sum([(float(f) / length)**2 for f in frequencies])

def aquireLength(CipherText, max, min):
    allScores = []
    for i in range(min, max+1):
        allBytes = [[0]*256 for x in range(i)]                                      #Using character frequencies calculated from counting counted characters in the cipher text aquires most likely key length
        for j, byte in enumerate(CipherText):                                       #Considering nested for loops, operating in O(n*m) time and calling the score function which operates in O(n) time. aquireLength's complexity will be at worst O(mnl) Where m 
            allBytes[j%i][byte]+=1                                                  #Is the total length of the list applied to the score function and l is the length of the desired ciphertext to process.
        individualScores = [score(bf) for bf in allBytes]
        average = sum(individualScores) / i
        allScores.append(average)
    return maxId(allScores) + min

def guessScore(frequencies):
    return sum([f1 * f2 for f1, f2 in zip(frequencies, ENGLISH_FREQUENCIES)])      #Using English character frequencies and frequencies of characters appearing in a new XOR'd sequence, sum their multiplications to aquire a meaningful score for that ith key guess
                                                                                   #Operating over two lists with zip causes a runtime of O(n*m) where M is the average length of the iterables used.

def getKey(streams):                                                               #Using Generated Streams applys a score to different ascii characters based on how their resulting stream after XORing
    allScores = []                                                                 #Nested for loop results in a time complexity of O(256n) where n is the size of the length of the ciphertext and 256 represents the constance number of possible keys for each sequence
    for keyGuess in range(0, 255):
        bs = [b^keyGuess for b in streams]
        lowerFrequency = [0] * 26
        invalid = False
        for b in bs:
            if b < 32 or b > 127:
                invalid = True
                break
            if chr(b) in 'abcdefghijklmnopqrstuvwxyz':
                #print(b-ord('a'))
                lowerFrequency[b - ord('a')] += 1
        score = guessScore(lowerFrequency)
        allScores.append((keyGuess, score))
    #print(allScores)
    return max(allScores, key=lambda x: x[1])[0]

def getStreams(cipherText, keyLength):                                             #Generates streams from given ciphertext based off of the desired keyLength
    byteStreams = [[] for i in range(keyLength)]                                   #Single loop bound by n which is the length of the ciphertext. O(n)
    for i, b in enumerate(cipherText):
        byteStreams[i % keyLength].append(b)
    return byteStreams

def decryption(cipherText, key):                                                   #Decryptes the ciphertext with the aquired key.
    decryptedMsg = ""                                                              #Single loop bound by the length of the ciphertext, O(n)
    for i, b in enumerate(cipherText):
        char = chr(key[i%len(key)] ^ b)
        decryptedMsg += char
    return decryptedMsg

f = open("cipher.txt")
data = f.read().strip()
f.close()
cipher = [(int(data[i:i+2], 16)) for i in range(0, len(data), 2)]

keyLength = aquireLength(cipher, 10, 2)
streams = getStreams(cipher, keyLength)
key = []
for bs in streams:
    key.append(getKey(bs))

print("Key = ", key)
for keyPoint in key:
    print(hex(keyPoint))
print("Decrypted Message")
print(decryption(cipher, key))


