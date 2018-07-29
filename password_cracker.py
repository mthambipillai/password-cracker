import hashlib
import argparse
import time

start_time = time.time()

def check_password(hash, password):
	if(hashlib.sha256(password).hexdigest().upper()==hash.upper()):
		print("PASSWORD CRACKED : "+password)
		elapsed_time = time.time() - start_time
		print("Time to crack : "+str(elapsed_time)+" seconds.")
		quit()

def count_print(i):
	i=i+1
	if(i%1000000==0):
		print("Tried "+str(i)+" possibilities.")
	return i


### BEGIN BRUTE FORCE ATTACK

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def bruteforce_length(hash, init_password, target_length, current_length, i):
	if(current_length==target_length):
		i = count_print(i)
		check_password(hash, init_password)
	else:
		for c in chars:
			i = bruteforce_length(hash, init_password+c, target_length, current_length+1, i)
	return i

def bruteforce_attack(hash, max_length):
	i=0
	for l in range(1,max_length+1):
		i = bruteforce_length(hash, "", l, 0, i)

### END BRUTE FORCE ATTACK

### BEGIN SIMPLE DICTIONARY ATTACK

def dictionary_attack(hash, dict_filename):
	i=0
	with open(dict_filename) as f:
		for line in f:
			i = count_print(i)
			password = line.rstrip()
			check_password(hash, password)

### END SIMPLE DICTIONARY ATTACK

### BEGIN DICTIONARY ATTACK WITH REPLACEMENTS

def get_transformations(password, replacements, from_index):
	if(from_index==len(replacements)):
		return [password]
	else:
		res = []
		nexts = get_transformations(password, replacements, from_index+1)
		repl = replacements[from_index]
		for t in nexts:
			res.append(t)
			transformation = t.replace(repl[0], repl[1])
			if(transformation!=t):
				res.append(transformation)
		return res

def dict_attack_with_replacements(hash, dict_filename, replacements):
	i=0
	with open(dict_filename) as f:
		for line in f:
			i = count_print(i)
			password = line.rstrip()
			transformations = get_transformations(password, replacements, 0)
			for t in transformations:
				check_password(hash, t)

### END DICTIONARY ATTACK WITH REPLACEMENTS

### BEGIN TARGETED ATTACK

def generate_possibilities(combination, words):
	result = [combination]
	for w in words:
		without = set(words)
		without.remove(w)
		new_combination = list(combination)
		new_combination.append(w)
		result.extend(generate_possibilities(new_combination, without))
	return result

def targeted_attack(hash, words):
	possibilities = map(lambda l: "".join(l), generate_possibilities([], words))
	i=0
	for p in possibilities:
		i = count_print(i)
		check_password(hash, p)

### END TARGETED ATTACK

parser = argparse.ArgumentParser(description="Simple password cracker. "+ 
	"Only a proof-of-concept for educational purposes. "+
	" See x for the full code and documentation.")
parser.add_argument("hash", help="SHA256 hash of the password to crack.")
parser.add_argument("method",
	help="Cracking method to use. Possible values are : brute_force, dict, dict_repl, targeted. ")
parser.add_argument("-l", "--length_max", type=int, default=5,
	help="Maximum password length in 'brute_force' method. Default is 5.")
parser.add_argument("-d", "--dictionary", default="",
	help="File name of the dictionary to use in 'dict' or 'dict_repl' methods.")
parser.add_argument("-w", "--words", default="",
	help="List of words separated by commas. To be used as input to the 'targeted' method.")
parser.add_argument("-r", "--replacements", default="",
	help="List of replacements separated by commas. To be used as input to the 'dict_repl' method. "+
	"Each replacement of a char 'o' by a char 'n' must be written 'o/n'.")
args = parser.parse_args()

if(args.method=="brute_force"):
	bruteforce_attack(args.hash, args.length_max)
elif(args.method=="dict"):
	if(args.dictionary==""):
		print("Method 'dict' requires argument 'dictionary'")
		quit()
	dictionary_attack(args.hash, args.dictionary)
elif(args.method=="dict_repl"):
	if(args.dictionary==""):
		print("Method 'dict_repl' requires argument 'dictionary'")
		quit()
	if(args.replacements==""):
		print("Method 'dict_repl' requires argument 'replacements'")
		quit()
	replacements = map(lambda r: r.split("/"), args.replacements.split(","))
	dict_attack_with_replacements(args.hash, args.dictionary, replacements)
elif(args.method=="targeted"):
	if(args.words==""):
		print("Method 'targeted' requires argument 'words'")
		quit()
	words_set = set(args.words.split(","))
	targeted_attack(args.hash, words_set)
else:
	print("Cracking method '"+args.method+"' doesn't exist.")
	quit()

print("Failed to crack the password with this method and these parameters.")