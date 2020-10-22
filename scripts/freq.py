from collections import Counter

tokens_file = open("token_per_spk.csv", 'r')

tokens_per_spk_list = [line.strip() for line in tokens_file]

tokens_dict = Counter(tokens_per_spk_list)

print(tokens_dict)