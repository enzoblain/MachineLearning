from models.linearRegression.adamLinearRegression import adamLinearRegression

def main() -> None:
    adamLinearRegression(learning_rate = 0.01, max_iterations = 10000, convergence_threshold = 1e-6, file_path = 'datasets/LinearRegression1.csv')

if __name__ == '__main__':
    main()