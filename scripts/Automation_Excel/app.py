import streamlit as st
import pandas as pd
import plotly.express as px

from report_generator import generate_report


def load_data(uploaded_file):
    """Read and clean Excel data."""

    df = pd.read_excel(
        uploaded_file,
        sheet_name=0,
        header=7
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    df = df.dropna(how="all")

    return df


def display_metrics(df, irregular_df):
    """Display dashboard metrics."""

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Records",
            len(df)
        )

    with col2:
        st.metric(
            "Irregular Failures",
            len(irregular_df)
        )


def display_chart(df):
    """Display category distribution chart."""

    category_counts = df["CATEGORY"].value_counts()

    fig = px.bar(
        x=category_counts.index,
        y=category_counts.values,
        text=category_counts.values,
        color=category_counts.index,
        labels={
            "x": "Category",
            "y": "Count"
        },
        title="Failure Category Distribution"
    )

    fig.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def main():

    st.set_page_config(
        page_title="Irregular Failure Report Generator",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 Irregular Failure Report Generator")

    uploaded_file = st.file_uploader(
        "Upload Failure Classification Excel File",
        type=["xlsx"]
    )

    if not uploaded_file:
        return

    df = load_data(uploaded_file)

    irregular_df = df[
        df["CATEGORY"] == "IRREGULAR_TEST_FAILURE"
    ]

    display_metrics(
        df,
        irregular_df
    )

    st.subheader("Failure Distribution")
    display_chart(df)

    st.subheader("Filtered Records Preview")
    st.dataframe(
        irregular_df,
        use_container_width=True
    )

    report_file, output_path, count = generate_report(
        uploaded_file
    )

    st.success(
        "Report Generated Successfully"
    )

    st.info(
        f"Total Irregular Failures Found: {count}"
    )

    st.info(
        f"Saved To: {output_path}"
    )

    st.download_button(
        label="📥 Download Report",
        data=report_file,
        file_name="Irregular_Test_Failures.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


if __name__ == "__main__":
    main()