"""
Linear Regression model using Adam optimizer.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def linearFunction(x: float, weight: float, bias: float) -> float:
    return weight * x + bias

def updatePredictions(data: pd.DataFrame, weight: float, bias: float) -> None:
    data['predicted'] = linearFunction(data['x'], weight, bias)

def derivativeWeight(data: pd.DataFrame) -> float:
    return ((data['predicted'] - data['y']) * data['x']).mean() * 2

def derivativeBias(data: pd.DataFrame) -> float:
    return ((data['predicted'] - data['y']).mean()) * 2

def adamUpdate(weight: float, bias: float, dW: float, dB: float, mW: float, vW: float, mB: float, vB: float, learning_rate: float = 0.01, t: int = 1, beta1: float = 0.9, beta2: float = 0.999, epsilon: float = 1e-8) -> tuple:
    mW = beta1 * mW + (1 - beta1) * dW
    mB = beta1 * mB + (1 - beta1) * dB
    
    vW = beta2 * vW + (1 - beta2) * (dW ** 2)
    vB = beta2 * vB + (1 - beta2) * (dB ** 2)
    
    mW_hat = mW / (1 - beta1 ** t)
    mB_hat = mB / (1 - beta1 ** t)
    
    vW_hat = vW / (1 - beta2 ** t)
    vB_hat = vB / (1 - beta2 ** t)
    
    weight -= learning_rate * mW_hat / (np.sqrt(vW_hat) + epsilon)
    bias -= learning_rate * mB_hat / (np.sqrt(vB_hat) + epsilon)
    
    return weight, bias, mW, vW, mB, vB

def loss(data: pd.DataFrame) -> float:
    return ((data['predicted'] - data['y']) ** 2).mean()

def adamLinearRegression(learning_rate: float = 0.01, max_iterations: int = 10000, convergence_threshold: float = 1e-6, file_path: str = 'datasets/LinearRegression1.csv') -> None:
    data = pd.read_csv(file_path)

    weight, bias = 0.0, 0.0
    previous_loss = float('inf')

    beta1 = 0.9
    beta2 = 0.999
    epsilon = 1e-8

    mW, vW = 0, 0
    mB, vB = 0, 0

    i = 1
    while i <= max_iterations:
        updatePredictions(data, weight, bias)
        
        dW = derivativeWeight(data)
        dB = derivativeBias(data)

        weight, bias, mW, vW, mB, vB = adamUpdate(weight, bias, dW, dB, mW, vW, mB, vB, learning_rate, i, beta1, beta2, epsilon)
        
        current_loss = loss(data)
        
        if abs(previous_loss - current_loss) < convergence_threshold:
            print(f'Converged after {i} iterations.')
            break
        
        previous_loss = current_loss
        i += 1
    
    updatePredictions(data, weight, bias)
    
    plt.figure(figsize=(12, 6))
    plt.plot(data['x'], data['y'], 'ro', label='Original data')
    plt.plot(data['x'], data['predicted'], 'b-', label='Predicted data')

    for i in range(len(data)):
        plt.vlines(x=data['x'][i], ymin=data['predicted'][i], ymax=data['y'][i], color='gray', linestyle='dashed')

    plt.xlabel('x')
    plt.ylabel('y / predicted')
    plt.legend()
    plt.title('Data vs Predicted')

    plt.tight_layout()
    plt.show()

    # Final results
    print("Final weights:", weight)
    print("Final bias:", bias)
    print("Final loss:", loss(data))
