import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import os
import re
import time
import glob
from urllib.request import urlopen


def file_already_exists(province_id):
    pattern = os.path.join("data", f"vhi_province_{province_id}_1981_2026_Mean_*.csv")
    files = glob.glob(pattern)
    return len(files) > 0


def download_file():
    parsed_url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={province_id}&year1=1981&year2=2026&type=Mean"
    os.makedirs("data", exist_ok=True)
    province_ids = list(range(1, 28))

    for province_id in province_ids:
        if file_already_exists(province_id):
            continue

        url = parsed_url.format(province_id=province_id)

        current_time = time.strftime("%d-%m-%Y_%H-%M-%S")
        destination = os.path.join(
            "data",
            f"vhi_province_{province_id}_1981_2026_Mean_{current_time}.csv"
        )

        response = urlopen(url)
        text = response.read().decode("utf-8")

        clean_text = re.sub(r"<.*?>", "", text)

        with open(destination, "w", encoding="utf-8") as f:
            f.write(clean_text)


def csv_to_df():
    files = glob.glob("data/*.csv")

    province_names = {
        1: "Cherkasy",
        2: "Chernihiv",
        3: "Chernivtsi",
        4: "Crimea",
        5: "Dnipropetrovs'k",
        6: "Donets'k",
        7: "Ivano-Frankivs'k",
        8: "Kharkiv",
        9: "Kherson",
        10: "Khmel'nyts'kyy",
        11: "Kiev",
        12: "Kiev City",
        13: "Kirovohrad",
        14: "Luhans'k",
        15: "L'viv",
        16: "Mykolayiv",
        17: "Odessa",
        18: "Poltava",
        19: "Rivne",
        20: "Sevastopol'",
        21: "Sumy",
        22: "Ternopil'",
        23: "Transcarpathia",
        24: "Vinnytsya",
        25: "Volyn",
        26: "Zaporizhzhya",
        27: "Zhytomyr"
    }

    dfs = []

    for file in files:
        df = pd.read_csv(
            file,
            skiprows=2,
            header=None,
            names=["year", "week", "SMN", "SMT", "VCI", "TCI", "VHI"],
            usecols=[0, 1, 2, 3, 4, 5, 6],
            skipinitialspace=True
        )

        df.drop(columns=["SMN", "SMT"], inplace=True)

        df.replace(-1, np.nan, inplace=True)
        df.dropna(inplace=True)

        province_id = int(re.search(r"vhi_province_(\d+)", file).group(1))

        df["province_id"] = province_id
        df["province_name"] = province_names[province_id]

        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


download_file()
vhi_df = csv_to_df()

st.set_page_config(page_title="VHI App", layout="wide")

st.title("Аналіз часових рядів VCI, TCI, VHI")

province_options = sorted(vhi_df["province_name"].unique())

week_min = int(vhi_df["week"].min())
week_max = int(vhi_df["week"].max())
year_min = int(vhi_df["year"].min())
year_max = int(vhi_df["year"].max())


def set_default():
    st.session_state.index_dd = "VCI"
    st.session_state.state_dd = province_options[0]
    st.session_state.week_slider = (week_min, week_max)
    st.session_state.year_slider = (year_min, year_max)
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False

def apply_dark_chart_style(fig, ax):
    fig.patch.set_facecolor("#1e1e1e")
    ax.set_facecolor("#1e1e1e")

    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")

    for spine in ax.spines.values():
        spine.set_color("white")

filters_col, output_col = st.columns([1, 3])

with filters_col:
    st.header("Фільтри")

    index_dd = st.selectbox(
        label="Оберіть індекс",
        options=["VCI", "TCI", "VHI"],
        index=0,
        key="index_dd"
    )

    state_dd = st.selectbox(
        label="Оберіть область",
        options=province_options,
        key="state_dd"
    )

    week_slider_start, week_slider_end = st.select_slider(
        label="Оберіть інтервал тижнів",
        options=list(range(week_min, week_max + 1)),
        value=(week_min, week_max),
        key="week_slider"
    )

    year_slider_start, year_slider_end = st.select_slider(
        label="Оберіть інтервал років",
        options=list(range(year_min, year_max + 1)),
        value=(year_min, year_max),
        key="year_slider"
    )

    sort_asc = st.checkbox(
        "Сортувати за зростанням",
        key="sort_asc"
    )

    sort_desc = st.checkbox(
        "Сортувати за спаданням",
        key="sort_desc"
    )

    reset_btn = st.button(
        "Скинути фільтри",
        on_click=set_default
    )

with output_col:
    st.header("Результати")

    filtered_df = vhi_df[
        (vhi_df["province_name"] == state_dd) &
        (vhi_df["week"].between(week_slider_start, week_slider_end)) &
        (vhi_df["year"].between(year_slider_start, year_slider_end))
    ].copy()

    if sort_asc and sort_desc:
        st.warning("Увімкнено обидва типи сортування. Оберіть тільки один.")
        filtered_df = filtered_df.sort_values(by=["year", "week"])
    elif sort_asc:
        filtered_df = filtered_df.sort_values(by=index_dd, ascending=True)
    elif sort_desc:
        filtered_df = filtered_df.sort_values(by=index_dd, ascending=False)
    else:
        filtered_df = filtered_df.sort_values(by=["year", "week"])

    tab_table, tab_graph, tab_compare = st.tabs([
        "Таблиця",
        "Графік часового ряду",
        "Порівняння областей"
    ])

    with tab_table:
        st.write("Обраний індекс:", index_dd)
        st.write("Обрана область:", state_dd)

        if filtered_df.empty:
            st.warning("Немає даних за вибраними фільтрами.")
        else:
            st.dataframe(
                filtered_df[["year", "week", "province_name", index_dd]],
                use_container_width=True
            )

    with tab_graph:
        if filtered_df.empty:
            st.warning("Немає даних для побудови графіка.")
        else:
            filtered_df = filtered_df.sort_values(by=["year", "week"])
            filtered_df["time"] = (
                filtered_df["year"].astype(str)
                + "-W"
                + filtered_df["week"].astype(str)
            )

            fig, ax = plt.subplots(figsize=(12, 5))
            apply_dark_chart_style(fig, ax)

            ax.plot(
                filtered_df["time"],
                filtered_df[index_dd],
                marker="o"
            )

            ax.set_title(f"{index_dd} для області {state_dd}")
            ax.set_xlabel("Рік-тиждень")
            ax.set_ylabel(index_dd)
            ax.tick_params(axis="x", rotation=90)

            # щоб не було занадто багато підписів на осі X
            step = max(1, len(filtered_df) // 15)
            ax.set_xticks(filtered_df["time"][::step])

            st.pyplot(fig)

    with tab_compare:
        comparison_df = vhi_df[
            (vhi_df["week"].between(week_slider_start, week_slider_end)) &
            (vhi_df["year"].between(year_slider_start, year_slider_end))
        ].copy()

        if comparison_df.empty:
            st.warning("Немає даних для порівняння областей.")
        else:
            comparison_grouped = (
                comparison_df
                .groupby("province_name", as_index=False)[index_dd]
                .mean()
                .sort_values(by=index_dd, ascending=False)
            )

            fig, ax = plt.subplots(figsize=(12, 6))
            apply_dark_chart_style(fig, ax)

            colors = [
                "#ff6b6b" if province == state_dd else "#4dabf7"
                for province in comparison_grouped["province_name"]
            ]

            ax.bar(
                comparison_grouped["province_name"],
                comparison_grouped[index_dd],
                color=colors
            )

            ax.set_title(
                f"Середнє значення {index_dd} по областях "
                f"за {year_slider_start}-{year_slider_end} роки"
            )
            ax.set_xlabel("Область")
            ax.set_ylabel(f"Середнє {index_dd}")
            ax.tick_params(axis="x", rotation=90)

            st.pyplot(fig)