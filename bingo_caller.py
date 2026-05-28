import random

# Number ranges for each letter
RANGES = {
    'R': range(1,  19),
    'O': range(19, 37),
    'M': range(37, 55),
    'A': range(55, 73),
    'N': range(73, 91),
}

def letter_for(n):
    for letter, r in RANGES.items():
        if n in r:
            return letter

def display_called(called):
    """Print called numbers organized by letter column."""
    print("\nNumbers called so far:")
    for letter in 'ROMAN':
        nums = [str(n) for (l, n) in called if l == letter]
        print(f"  {letter}: {', '.join(nums) if nums else '-'}")
    print()

def main():
    pool = list(range(1, 91))
    random.shuffle(pool)
    called = []

    print("=" * 45)
    print("   Roman Galactic Bulge BINGO -- Caller")
    print("=" * 45)
    print("Press Enter to draw the next number.")
    print("Type 'q' and Enter to end the game.\n")

    while pool:
        try:
            cmd = input(f"[{len(called)}/90 called] Press Enter to draw: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if cmd == 'q':
            break

        n = pool.pop()
        letter = letter_for(n)
        called.append((letter, n))

        print("\n" + "=" * 45)
        print(f"         >>> {letter} - {n} <<<")
        print("=" * 45)
        display_called(called)

    print(f"Game over. {len(called)} number(s) called, {len(pool)} remaining.")

if __name__ == '__main__':
    main()
