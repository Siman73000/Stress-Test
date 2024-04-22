import multiprocessing
import sys

# Define an iterative Fibonacci function
def fibonacci_iterative(n):
    fib_sequence = [0, 1]
    for i in range(2, n+1):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    return fib_sequence

# Worker function for each core
def fibonacci_worker(start, end, result):
    for i in range(start, end):
        result.append(fibonacci_iterative(i))

if __name__ == "__main__":
    num_cores = multiprocessing.cpu_count()
    max_int = sys.maxsize
    chunk_size = 10000  # Adjust the chunk size as needed

    while True:
        # Create shared memory for results
        manager = multiprocessing.Manager()
        result = manager.list()

        # Split work for each core
        processes = []
        start = 0
        for i in range(num_cores):
            end = min(start + chunk_size, max_int)  # Avoid exceeding the maximum integer value
            p = multiprocessing.Process(target=fibonacci_worker, args=(start, end, result))
            processes.append(p)
            p.start()
            start = end

        # Wait for all processes to finish
        for p in processes:
            p.join()

        # Print results
        print("Fibonacci sequence calculated by each core:")
        for i in range(len(result)):
            print(f"Core {i+1}: {result[i][0]} ... {result[i][-1]}")

        # Reset if almost at integer limit
        if start == max_int:
            print("Reached close to the integer limit. Restarting calculation...")
