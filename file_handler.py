def write_to_all(num, filepath):
    with open(filepath, "a") as f:
        f.write(str(num) + "\n")

def write_to_even(num, filepath):
    with open(filepath, "a") as f:
        f.write(str(num) + "\n")

def write_to_odd(num, filepath):
    with open(filepath, "a") as f:
        f.write(str(num) + "\n")
