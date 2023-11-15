import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# Load input data
input_data = np.loadtxt("input_features.csv", delimiter=",")

# Load output data
output_data = np.loadtxt("output_features.csv", delimiter=",")

# Set the seed for reproducibility
np.random.seed(42)

# Define the proportion of the dataset to include in the test split
test_size = 0.2

# Calculate the number of samples for the test set
test_samples = int(test_size * input_data.shape[0])

# Generate random indices for the test set
test_indices = np.random.choice(input_data.shape[0], test_samples, replace=False)

# Create indices for the training set by excluding the test indices
train_indices = np.array([i for i in range(input_data.shape[0]) if i not in test_indices])

# Split the data into training and testing sets
X_train = input_data[train_indices]
y_train = output_data[train_indices]

X_test = input_data[test_indices]
y_test = output_data[test_indices]

# Converting numpy data into pytorch tensor
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32)

print(X_train_tensor.shape)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

# Reshaping the data to avoid problems during training and testing
# Reshaping X matirces to have 6 columns and y vector to have 1 column
X_train_tensor = X_train_tensor.view(-1, 6)
X_test_tensor = X_test_tensor.view(-1, 6)

y_train_tensor = y_train_tensor.view(-1, 1)
y_test_tensor = y_test_tensor.view(-1, 1)


# Define the MLP model
class MLPModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(MLPModel, self).__init__()
        self.fc1 = nn.Linear(input_size, 12)
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()
        self.fc2 = nn.Linear(12, 32)
        self.fc3 = nn.Linear(32, 16)
        self.fc4 = nn.Linear(16, 1)

    
    def forward(self, x):
        x = self.fc1(x)
        x = self.tanh(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.relu(x)
        x = self.fc4(x)
        return x
# Initialize the model
input_size = 6  # Assuming you have 6 input features
# Adjust the number of hidden units as needed
output_size = 1  # Assuming you have a single output feature

model = MLPModel(input_size, output_size)

# Define loss function and optimizer
criterion = nn.MSELoss()  # Mean Squared Error loss for regression
optimizer = optim.Adam(model.parameters(), lr=0.01)  # Adjust the learning rate as needed

# Training loop
num_epochs = 5000  # Adjust the number of epochs as needed


for epoch in range(num_epochs):
    # Forward pass
    outputs = model(X_train_tensor)
    
    # Calculate loss
    loss = criterion(outputs, y_train_tensor)
    
    # Backpropagation and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.8f}')

print('Training finished.')



# Make predictions on the test data
with torch.no_grad():
    test_predictions = model(X_test_tensor)

# Calculate the Mean Squared Error
mse = nn.MSELoss()(test_predictions, y_test_tensor)

print(f"Mean Squared Error on Test Data: {mse.item():.8f}")

# jit tracing the model using a 1000 by 6 tensor
example_forward_input = torch.rand(1000,6)

module = torch.jit.trace(model, example_forward_input)

# save the jit traced model
torch.jit.save(module, "ali_model_scripted.pt")
