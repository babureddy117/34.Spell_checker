import re

class SpellChecker:
    def __init__(self, dictionary_file):
        self.dictionary = set()
        self.load_dictionary(dictionary_file)

    def load_dictionary(self, filename):
        try:
            with open(filename, 'r') as f:
                self.dictionary = set(word.strip().lower() for word in f)
            print(f"Loaded {len(self.dictionary)} words from dictionary\n")
        except FileNotFoundError:
            print(f"Error: {filename} not found")

    def is_correct(self, word):
        return word.lower() in self.dictionary

    def edit_distance(self, word1, word2):
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
        
        return dp[m][n]

    def get_suggestions(self, word, max_suggestions=5):
        word = word.lower()
        suggestions = []
        
        for dict_word in self.dictionary:
            if abs(len(word) - len(dict_word)) > 2:
                continue
            
            distance = self.edit_distance(word, dict_word)
            if distance <= 2:
                suggestions.append((dict_word, distance))
        
        suggestions.sort(key=lambda x: x[1])
        return [word for word, _ in suggestions[:max_suggestions]]

    def check_word(self, word):
        if self.is_correct(word):
            print(f"✓ '{word}' is spelled correctly")
        else:
            print(f"✗ '{word}' is misspelled")
            suggestions = self.get_suggestions(word)
            if suggestions:
                print(f"  Suggestions: {', '.join(suggestions)}")
            else:
                print("  No suggestions found")

    def check_text(self, text):
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        misspelled = []
        
        for word in words:
            if not self.is_correct(word):
                misspelled.append(word)
        
        if not misspelled:
            print("\n✓ No spelling errors found!")
            return
        
        print(f"\n✗ Found {len(misspelled)} misspelled word(s):\n")
        
        for word in set(misspelled):
            print(f"'{word}'")
            suggestions = self.get_suggestions(word)
            if suggestions:
                print(f"  → {', '.join(suggestions)}")
            print()

    def check_file(self, filename):
        try:
            with open(filename, 'r') as f:
                text = f.read()
            print(f"Checking file: {filename}\n")
            self.check_text(text)
        except FileNotFoundError:
            print(f"Error: {filename} not found")

    def add_word(self, word):
        word = word.lower()
        if word in self.dictionary:
            print(f"'{word}' already in dictionary")
        else:
            self.dictionary.add(word)
            print(f"'{word}' added to dictionary")

    def interactive_check(self):
        print("Enter text to check (or 'done' to finish):")
        lines = []
        while True:
            line = input()
            if line.lower() == 'done':
                break
            lines.append(line)
        
        text = ' '.join(lines)
        self.check_text(text)

def main():
    checker = SpellChecker('dictionary.txt')
    
    if not checker.dictionary:
        return
    
    print("=== Spell Checker ===")
    print("Commands: check <word>, text, file <filename>, add <word>, exit\n")
    
    while True:
        command = input("spell> ").strip().split(maxsplit=1)
        
        if not command:
            continue
        
        cmd = command[0]
        
        if cmd == "check":
            if len(command) < 2:
                print("Usage: check <word>")
            else:
                checker.check_word(command[1])
        
        elif cmd == "text":
            checker.interactive_check()
        
        elif cmd == "file":
            if len(command) < 2:
                print("Usage: file <filename>")
            else:
                checker.check_file(command[1])
        
        elif cmd == "add":
            if len(command) < 2:
                print("Usage: add <word>")
            else:
                checker.add_word(command[1])
        
        elif cmd == "exit":
            break
        
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()
