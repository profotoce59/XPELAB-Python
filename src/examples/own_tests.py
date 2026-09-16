def main() -> None:
    original = [1, 2, 3]
    alias = original       # NOT a copy - the same list, under two names
    alias.append(4)
    print(original)
    
    original = "My name is"
    alias = original       # NOT a copy - the same list, under two names
    alias += " Romain"
    print(alias)
    print(original)

if __name__ == "__main__":
    main()



