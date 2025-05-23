import hashlib

max_zero = 0
i = 0
multiply_factor = 20

print("Press Enter to add more items. Type 'q' to quit.\n")

while True:
    user_input = input("Add more? ")

    if user_input.lower() == 'q':
        break

    for _ in range(multiply_factor):
        h = hashlib.sha1(str(i).encode()).hexdigest()
        binary = bin(int(h, 16))[2:].zfill(160)
        leading_zeros = len(binary) - len(binary.lstrip('0'))
        max_zero = max(max_zero, leading_zeros)
        i += 1

    estimate = 2 ** max_zero
    print(f"Items added: {i} | Estimated unique count: {estimate}")
