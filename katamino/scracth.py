import numpy as np

pentaminos = [np.array([1, 1, 1, 1, 1], dtype=np.int),
              np.array([[1, 1, 1, 1], [1, 0, 0, 0]], dtype=np.int)]


def main():
    b = np.zeros((7, 5), dtype=np.int)
    
    b[0:4, 3:5] += np.rot90(pentaminos[1])

    print(b)

if __name__ == "__main__":
    main()
