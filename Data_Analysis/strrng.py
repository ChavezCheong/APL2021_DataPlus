boof = ""
with open(r'C:\Users\chave\Desktop\Duke\APL2021_DataPlus\Data_Analysis\stop_words.txt','r', encoding = "ISO-8859-1") as file:
    contents = file.readlines()
    for word in contents:
        boof += f"|{word[:-1]}"

print(boof)

def pivotIndex(nums):
    left = [0]*len(nums)
    right = [0]* len(nums)
    # Calculate left sum array
    left_sum = 0
    for i in range(len(nums)):
        left[i] = left_sum
        left_sum += nums[i]
    # Calculate right sum array
    right_sum = 0
    for j in range(len(nums)-1,-1,-1):
        right[j] = right_sum
        right_sum += nums[j]
    for k in range(len(nums)):
        if left[k] == right[k]:
            return k
    return -1

print(pivotIndex([1,7,3,6,5,6]))