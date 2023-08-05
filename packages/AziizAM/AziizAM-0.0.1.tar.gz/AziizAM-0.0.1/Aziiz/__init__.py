
def print_percentage_bar(iterate, total_iterations, length):
    percentage = (iterate / total_iterations)
    filled_length = int(length * percentage)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r[{bar}] {percentage * 100:.1f}%', end='')