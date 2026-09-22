import os

import matplotlib
matplotlib.use("Agg")

import pandas as pd
import matplotlib.pyplot as plt


def process_file(filepath, output_folder):

    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".csv":
        df = pd.read_csv(filepath)

    elif extension == ".xlsx":
        df = pd.read_excel(filepath)

    else:
        raise ValueError(
            "Only CSV and Excel files are supported."
        )

    # Remove empty rows
    df = df.dropna(how="all")

    # Clean column names
    df.columns = df.columns.astype(str).str.strip()

    # Find email column
    email_column = None

    possible_columns = [
        "Customer_Email",
        "Email",
        "email",
        "customer_email"
    ]

    for column in possible_columns:
        if column in df.columns:
            email_column = column
            break

    if email_column is None:
        raise ValueError(
            "Customer_Email column not found in Excel file."
        )

    # Get recipient email
    emails = (
        df[email_column]
        .dropna()
        .astype(str)
        .str.strip()
    )

    emails = emails[emails != ""]

    if emails.empty:
        raise ValueError(
            "No recipient email found in Excel file."
        )

    recipient_email = emails.iloc[0]

    # Basic information
    total_records = len(df)
    total_columns = len(df.columns)
    columns = list(df.columns)

    # Numeric statistics
    numeric_columns = (
        df.select_dtypes(include="number")
        .columns
        .tolist()
    )

    statistics = {}

    for column in numeric_columns:
        statistics[column] = {
            "total": float(df[column].sum()),
            "average": float(df[column].mean()),
            "maximum": float(df[column].max()),
            "minimum": float(df[column].min())
        }

    # Create report folder
    os.makedirs(output_folder, exist_ok=True)

    chart_files = []
    main_numeric_column = None

    # Create charts
    if numeric_columns:

        main_numeric_column = numeric_columns[0]

        # Bar chart
        plt.figure(figsize=(8, 5))

        df[main_numeric_column].head(10).plot(
            kind="bar"
        )

        plt.title(
            f"{main_numeric_column} - First 10 Records"
        )

        plt.xlabel("Record")
        plt.ylabel(main_numeric_column)
        plt.tight_layout()

        bar_path = os.path.join(
            output_folder,
            "bar_chart.png"
        )

        plt.savefig(bar_path, dpi=150)
        plt.close("all")

        chart_files.append(bar_path)

        # Line chart
        plt.figure(figsize=(8, 5))

        df[main_numeric_column].head(20).plot(
            kind="line",
            marker="o"
        )

        plt.title(
            f"{main_numeric_column} Trend"
        )

        plt.xlabel("Record")
        plt.ylabel(main_numeric_column)
        plt.tight_layout()

        line_path = os.path.join(
            output_folder,
            "line_chart.png"
        )

        plt.savefig(line_path, dpi=150)
        plt.close("all")

        chart_files.append(line_path)

    # Category chart
    categorical_columns = (
        df.select_dtypes(exclude="number")
        .columns
        .tolist()
    )

    categorical_columns = [
        column
        for column in categorical_columns
        if column != email_column
    ]

    if categorical_columns and numeric_columns:

        category_column = categorical_columns[0]

        category_data = (
            df.groupby(category_column)[
                main_numeric_column
            ]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        plt.figure(figsize=(8, 5))

        category_data.plot(
            kind="bar"
        )

        plt.title(
            f"{main_numeric_column} by {category_column}"
        )

        plt.xlabel(category_column)
        plt.ylabel(main_numeric_column)

        plt.xticks(rotation=45)
        plt.tight_layout()

        category_path = os.path.join(
            output_folder,
            "category_chart.png"
        )

        plt.savefig(category_path, dpi=150)
        plt.close("all")

        chart_files.append(category_path)

    # Preview
    preview = (
        df.head(10)
        .fillna("")
        .to_dict(orient="records")
    )

    # Return result
    return {
        "filename": os.path.basename(filepath),
        "total_records": total_records,
        "total_columns": total_columns,
        "columns": columns,
        "numeric_columns": numeric_columns,
        "statistics": statistics,
        "main_numeric_column": main_numeric_column,
        "chart_files": chart_files,
        "preview": preview,
        "recipient_email": recipient_email
    }