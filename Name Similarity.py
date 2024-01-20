'''
한글 문자 순서 = 한글 문자 코드 - 0xAC00

초성 순서 = 한글 문자 순서 / (21 * 28)
중성 순서 = (한글 문자 순서 % (21 * 28)) / 28
종성 순서 = (한글 문자 순서 % (21 * 28)) % 28
'''

consonant_list = [['ㄱ', 1], ['ㄲ', 2], ['ㄴ', 1], ['ㄷ', 2], ['ㄸ', 4], ['ㄹ', 3], ['ㅁ', 3], ['ㅂ', 4], ['ㅃ', 8], ['ㅅ', 2], ['ㅆ', 4], ['ㅇ', 1], ['ㅈ', 2], ['ㅉ', 4], ['ㅊ', 3], ['ㅋ', 2], ['ㅌ', 3], ['ㅍ', 4], ['ㅎ', 3]]
consonant2_list = [['ㄱ', 1], ['ㄲ', 2], ['ㄳ', 3], ['ㄴ', 1], ['ㄵ', 3], ['ㄶ', 4], ['ㄷ', 2], ['ㄹ', 3], ['ㄺ', 4], ['ㄻ', 6], ['ㄼ', 7], ['ㄽ', 5], ['ㄾ', 6], ['ㄿ', 7], ['ㅀ', 6], ['ㅁ', 3], ['ㅂ', 4], ['ㅄ', 6], ['ㅅ', 2], ['ㅆ', 4], ['ㅇ', 1], ['ㅈ', 2], ['ㅊ', 3], ['ㅋ', 2] , ['ㅌ', 3], ['ㅍ', 4], ['ㅎ', 3], [None]]
vowel_list = [['ㅏ', 2], ['ㅐ', 3], ['ㅑ', 3], ['ㅒ', 4], ['ㅓ', 2], ['ㅔ', 3], ['ㅕ', 3], ['ㅖ', 4], ['ㅗ', 2], ['ㅘ', 4], ['ㅙ', 5], ['ㅚ', 3], ['ㅛ', 3], ['ㅜ', 2], ['ㅝ', 4], ['ㅞ', 5], ['ㅟ', 3], ['ㅠ', 3], ['ㅡ', 1], ['ㅢ', 2], ['ㅣ', 1]]

def order_letter(word):
    return int(ord(word) - int(0xAC00))
def start_letter(word): # return into list : ['letter', stroke count]
    return consonant_list[(order_letter(word) // (21 * 28))]
def mid_letter(word):   # return into list : ['letter', stroke count]
    return vowel_list[((order_letter(word) % (21 * 28)) // 28)]
def last_letter(word):  # return into list : ['letter', stroke count]
    return consonant2_list[((((order_letter(word) % (21 * 28)) % 28)) - 1)]

name1, name2 = map(str, input('Put two names with space split: ').split())
X = [] ; Y = []
def fill(name, list):
    temp = (start_letter(name), mid_letter(name), last_letter(name))
    for j in range(3):
        if (j == 2) and (not temp[2][0]):
            continue
        # print(f'{name} . {temp[j]}')
        list.append(str(temp[j][1]))
for i in range(3):
    fill(name1[i], X)
    fill(name2[i], Y)
# print(f'X = {X}\nY = {Y}')

# Alignment
import numpy as np

x = "".join(X)
y = "".join(Y)
n = len(x) ; m = len(y)
matrix = np.zeros((n+1, m+1))

def needleman(x, y, match=8, mismatch=-5, gap=-3):

    # 열, 행 초기화
    for i in range(1, n+1):
        matrix[i][0] = matrix[i-1][0] + gap
    for j in range(1, m+1):
        matrix[0][j] = matrix[0][j-1] + gap

    # 본격적 Algorithm
    for i in range(1, n+1):
        for j in range(1, m+1):
            if x[i-1] == y[j-1]:
                diagonal = matrix[i-1][j-1] + match
            else:
                diagonal = matrix[i-1][j-1] + mismatch

            left = matrix[i][j-1] + gap ; up = matrix[i-1][j] + gap
            matrix[i][j] = max(diagonal, left, up)

    # Back-Tracking
    aligned_x = [] ; aligned_y = []
    i, j = n, m
    while (i > 0) and (j > 0):
        if matrix[i][j] == matrix[i-1][j-1] + (match if x[i-1] == y[j-1] else mismatch):
            aligned_x.insert(0, x[i-1])
            aligned_y.insert(0, y[j-1])
            i -= 1 ; j -= 1
        elif matrix[i][j] == matrix[i][j-1] + gap:
            aligned_x.insert(0, "-")
            aligned_y.insert(0, y[j-1])
            j -= 1
        else:
            aligned_x.insert(0, x[i-1])
            aligned_y.insert(0, "-")
            i -= 1

    # 끝 부분
    while i > 0:
        aligned_x.insert(0, x[i-1])
        aligned_y.insert(0, "-")
        i -= 1
    while j > 0:
        aligned_x.insert(0, "-")
        aligned_y.insert(0, y[j-1])
        j -= 1

    # 문자열 변환
    aligned_x = "".join(aligned_x)
    aligned_y = "".join(aligned_y)

    # 점수 계산
    score = 0
    for i in range(len(aligned_x)):
        if aligned_x[i] == aligned_y[i]:
            score += match
        elif (aligned_x[i] == '-') or (aligned_y[i] == '-'):
            score += gap
        else:
            score += mismatch

    return aligned_x, aligned_y, score

aligned_x, aligned_y, score = needleman(x, y)
print(f'Name Similarity: {score}%')

# // EOF