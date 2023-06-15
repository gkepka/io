import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV file into a pandas DataFrame
data = pd.read_csv('results.csv')

# Extract the "min_var" and "curr_pop" columns
min_var = data['min_var']
curr_pop = data['curr_pop']
best_fit = data['max_fit']
print(best_fit)
# Create a figure and two subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

# Plot "min_var" on the first subplot
ax1.plot(min_var)
ax1.set_ylabel('Minimum Variance')
ax1.set_yscale('log')  # Set y-axis to a logarithmic scale

# Plot "curr_pop" on the second subplot
ax2.plot(curr_pop)
ax2.set_ylabel('Current Population')

ax3.plot(best_fit)
ax3.set_ylabel('Best Fitness')
ax3.set_yscale('log')

# Set common x-label
plt.xlabel('Epochs')

# Adjust spacing between subplots
plt.tight_layout()

# Display the plot
plt.show()