import hashlib

def crack_passwords(hash_file_path, wordlist_path):
    # Load all target hashes into a set for fast lookup
    target_hashes = set()
    with open(hash_file_path, "r") as hash_file:
        for line in hash_file:
            target_hashes.add(line.strip())  # Remove newline characters

    # Open wordlist and iterate through each word
    with open(wordlist_path, "r") as wordlist_file:
        print("\n--- CRACKING STARTED ---")
        for word in wordlist_file:
            clean_word = word.strip()
            hashed_word = hashlib.md5(clean_word.encode()).hexdigest()
            if hashed_word in target_hashes:
                print(f"[+] Cracked: {hashed_word} --> {clean_word}")
                target_hashes.remove(hashed_word)  # Optional: remove cracked hash
        if target_hashes:
            for remaining_hash in target_hashes:
                print(f"[-] FAILED: {remaining_hash}")
        else:
            print("[!] All hashes cracked successfully!")
        print("--- CRACKING FINISHED ---")

def main():
    hash_file_path = input("Enter path to hash file: ")
    wordlist_path = input("Enter path to wordlist file: ")
    crack_passwords(hash_file_path, wordlist_path)

if __name__ == "__main__":
    main()
