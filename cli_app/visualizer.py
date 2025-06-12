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


def generate_visualization(df, chart_type, x_col=None, y_col=None):
    """Return a matplotlib figure for the requested chart type."""

    plt.figure(figsize=(10, 6))

    if chart_type in {"bar", "line", "scatter"}:
        if x_col is None or y_col is None:
            raise ValueError("x_col and y_col must be provided for this chart type")
        if not pd.api.types.is_numeric_dtype(df[y_col]):
            raise ValueError(f"Column '{y_col}' is not numeric")

        if chart_type == "bar":
            df.groupby(x_col)[y_col].sum().plot(kind="bar")
            plt.title(f"Bar Chart: {y_col} by {x_col}")
        elif chart_type == "line":
            plt.plot(df[x_col], df[y_col], marker="o")
            plt.title(f"Line Chart: {y_col} over {x_col}")
        else:  # scatter
            plt.scatter(df[x_col], df[y_col])
            plt.title(f"Scatter Plot: {y_col} vs {x_col}")

        plt.xlabel(x_col)
        plt.ylabel(y_col)

    elif chart_type == "pie":
        if x_col is None:
            raise ValueError("x_col must be provided for pie chart")

        if y_col is not None:
            if not pd.api.types.is_numeric_dtype(df[y_col]):
                raise ValueError(f"Column '{y_col}' is not numeric")
            df.groupby(x_col)[y_col].sum().plot(
                kind="pie", autopct="%1.1f%%", startangle=90
            )
            plt.title(f"Pie Chart of {y_col} by {x_col}")
        else:
            df[x_col].value_counts().plot(
                kind="pie", autopct="%1.1f%%", startangle=90
            )
            plt.title(f"Pie Chart of {x_col}")

        plt.ylabel("")

    elif chart_type == "hist":
        if x_col is None:
            raise ValueError("x_col must be provided for histogram")
        if not pd.api.types.is_numeric_dtype(df[x_col]):
            raise ValueError(f"Column '{x_col}' is not numeric")
        df[x_col].plot(kind="hist", bins=10, edgecolor="black")
        plt.title(f"Histogram of {x_col}")
        plt.xlabel(x_col)

    elif chart_type == "box":
        if x_col is None:
            raise ValueError("x_col must be provided for box plot")
        if not pd.api.types.is_numeric_dtype(df[x_col]):
            raise ValueError(f"Column '{x_col}' is not numeric")
        sns.boxplot(data=df[[x_col]])
        plt.title(f"Box Plot of {x_col}")

    elif chart_type == "heatmap":
        corr = df.select_dtypes(include="number").corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm")
        plt.title("Heatmap of Correlations")

    elif chart_type == "grouped_bar":
        if x_col is None or y_col is None:
            raise ValueError("x_col and y_col must be provided for grouped_bar")
        if not pd.api.types.is_numeric_dtype(df[y_col]):
            raise ValueError(f"Column '{y_col}' is not numeric")
        df.groupby(x_col)[y_col].sum().plot(kind="bar")
        plt.title(f"Grouped Bar Chart: {y_col} by {x_col}")
        plt.xlabel(x_col)
        plt.ylabel(y_col)

    else:
        raise ValueError("Unsupported chart type")

    plt.tight_layout()
    return plt.gcf()

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
        log_folder = os.environ.get(
            "VIS_LOG_FOLDER",
            DEFAULT_LOG_FOLDER,
        )
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
        chart_map = {
            '1': 'bar',
            '2': 'line',
            '3': 'scatter',
            '4': 'pie',
            '5': 'hist',
            '6': 'box',
            '7': 'heatmap',
            '8': 'grouped_bar'
        }

        chart_type = chart_map.get(option)
        if not chart_type:
            print("Invalid option selected.")
            return

        x = y = None
        if chart_type in {"bar", "line", "scatter", "grouped_bar"}:
            x_idx = get_column_index("Enter number for X-axis column: ")
            y_idx = get_column_index("Enter number for Y-axis column: ")
            x, y = all_columns[x_idx], all_columns[y_idx]
        elif chart_type in {"pie", "hist", "box"}:
            col_idx = get_column_index("Enter number for column: ")
            x = all_columns[col_idx]

        fig = generate_visualization(df, chart_type, x, y)

        save_choice = input("\nWould you like to save this visualization? (1 for Yes, 2 for No): ").strip()

        if save_choice == '1':
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(log_folder, f"visualization_{timestamp}.png")
            fig.savefig(filename)
            print(f"\nVisualization saved as: {filename}")

        plt.show()
        plt.close(fig)

    except Exception as e:
        print(f"Error generating visualization: {e}")

