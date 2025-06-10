import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime
import pandas as pd

# Base directory for saving visualizations
CAPSTONE_HOME = os.getenv(
    "CAPSTONE_HOME",
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
DEFAULT_LOG_FOLDER = os.path.join(CAPSTONE_HOME, "logs", "visualizations")

def ask_for_visualization(df, title, log_folder=None):
    """Visualize dataframe columns using various chart types.

    The ``title`` argument sets a default chart title.  Individual
    visualizations may override this with a more specific title.
    """

    if df.empty:
        print("\nNo data available to visualize.")
        return

    choice = input("\nWould you like a visualization of this information? (yes/no): ").strip().lower()
    if choice != 'yes':
        return

    if log_folder is None:
        log_folder = DEFAULT_LOG_FOLDER
    os.makedirs(log_folder, exist_ok=True)

    print("\nChoose a visualization type:")
    viz_options = {
        "1": "Bar Chart",
        "2": "Line Chart",
        "3": "Scatter Plot",
        "4": "Pie Chart",
        "5": "Histogram",
        "6": "Box Plot",
        "7": "Heatmap",
        "8": "Grouped Bar Chart"
    }

    for key, val in viz_options.items():
        print(f"{key}. {val}")

    option = input("\nEnter option number: ").strip()
    plt.figure(figsize=(10, 6))
    plt.title(title)

    all_columns = list(df.columns)

    print("\nAvailable columns:")
    for i, col in enumerate(all_columns, 1):
        print(f"{i}. {col}")

    def get_column_index(prompt):
        while True:
            try:
                idx = int(input(prompt)) - 1
                if 0 <= idx < len(all_columns):
                    return idx
                else:
                    print("Invalid column number. Try again.")
            except ValueError:
                print("Please enter a valid number.")

    try:
        if option in ['1', '2', '3']:  # Bar, Line, Scatter
            x_idx = get_column_index("Enter number for X-axis column: ")
            y_idx = get_column_index("Enter number for Y-axis column: ")
            x, y = all_columns[x_idx], all_columns[y_idx]

            if not pd.api.types.is_numeric_dtype(df[y]):
                print(f"Column '{y}' is not numeric. Cannot plot {viz_options[option]}.")
                return

            if option == '1':
                df.groupby(x)[y].sum().plot(kind='bar')
                plt.title(f"Bar Chart: {y} by {x}")
            elif option == '2':
                plt.plot(df[x], df[y], marker='o')
                plt.title(f"Line Chart: {y} over {x}")
            elif option == '3':
                plt.scatter(df[x], df[y])
                plt.title(f"Scatter Plot: {y} vs {x}")

            plt.xlabel(x)
            plt.ylabel(y)

        elif option == '4':  # Pie Chart
            col_idx = get_column_index("Enter number for column: ")
            col = all_columns[col_idx]
            df[col].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90)
            plt.title(f"Pie Chart of {col}")
            plt.ylabel('')  # Hide y-axis

        elif option == '5':  # Histogram
            col_idx = get_column_index("Enter number for column: ")
            col = all_columns[col_idx]

            if not pd.api.types.is_numeric_dtype(df[col]):
                print(f"Column '{col}' is not numeric. Cannot plot histogram.")
                return

            df[col].plot(kind='hist', bins=10, edgecolor='black')
            plt.title(f"Histogram of {col}")
            plt.xlabel(col)

        elif option == '6':  # Box Plot
            col_idx = get_column_index("Enter number for column: ")
            col = all_columns[col_idx]

            if not pd.api.types.is_numeric_dtype(df[col]):
                print(f"Column '{col}' is not numeric. Cannot plot boxplot.")
                return

            sns.boxplot(data=df[[col]])
            plt.title(f"Box Plot of {col}")

        elif option == '7':  # Heatmap
            print("Using correlation matrix of numeric columns.")
            corr = df.select_dtypes(include='number').corr()
            sns.heatmap(corr, annot=True, cmap="coolwarm")
            plt.title("Heatmap of Correlations")

        elif option == '8':  # Grouped Bar Chart
            group_idx = get_column_index("Enter number for X-axis (categorical) column: ")
            value_idx = get_column_index("Enter number for Y-axis (numeric) column: ")
            group_col, value_col = all_columns[group_idx], all_columns[value_idx]

            if not pd.api.types.is_numeric_dtype(df[value_col]):
                print(f"Column '{value_col}' is not numeric. Cannot plot grouped bar chart.")
                return

            df.groupby(group_col)[value_col].sum().plot(kind='bar')
            plt.title(f"Grouped Bar Chart: {value_col} by {group_col}")
            plt.xlabel(group_col)
            plt.ylabel(value_col)

        else:
            print("Invalid option selected.")
            return

        plt.tight_layout()

        save_choice = input("\nWould you like to save this visualization? (1 for Yes, 2 for No): ").strip()

        if save_choice == '1':
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(log_folder, f"visualization_{timestamp}.png")
            plt.savefig(filename)
            print(f"\nVisualization saved as: {filename}")

        plt.show()
        plt.close()

    except Exception as e:
        print(f"Error generating visualization: {e}")

