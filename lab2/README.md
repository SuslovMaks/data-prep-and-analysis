# Проєкт обробки та аналізу даних

Цей проєкт містить Python-скрипти для завантаження, очищення та аналізу даних з екології та енергоспоживання.

1. **Індекс здоров’я рослин (VHI)** для українських областей.
2. **Дані по споживанню електроенергії у будинках** для детального аналізу.

---

## 📁 Структура даних

- `data/` - папка з завантаженими датасетами:
  - `vhi_province_<id>_1981_2026_Mean_<timestamp>.csv` - дані VHI для кожної області (завантажуються динамічно).
  - `household_power_consumption.txt` - дані споживання електроенергії.
- `vhi_notebook.ipynb` - скрипт для роботи з індексом здоров’я рослин.
- `power_notebook.ipynb` - скрипт для роботи з даними по споживаню електроенергії.
---

## 🛠 Залежності

- Python 3.8+
- Бібліотеки:
  ```bash
  pandas
  numpy
  scipy
  urllib
  glob
  re
  time
  timeit

## 🌱 Обробка даних VHI

- `Функції аналізу:`
  - `filter_province_year(province_id, year)` — виводить VHI для конкретної області та року.
  - `filter_provinces_years(provinces_ids, years)` — виводить дані для декількох областей і років.
  - `filter_stats_provinces_years(provinces_ids, years)` — виводить мінімум, максимум, середнє та медіану VHI для обраних областей.
 
## ⚡ Обробка даних споживання електроенергії

- `Функції аналізу:`
  - `Фільтри:`
    - `filter_power_over_5kw(df)` — відбирає рядки з активною потужністю >5 кВт.
    - `filter_between_19_20(df)` — відбирає рядки з інтенсивністю між 19–20 і сумою субметрингів 1 & 2 > субметринг 3.
    - `filter_random_mean(df)` — обчислює середнє значення для 500 000 випадкових рядків.
    - `filter_evening(df)` — фільтрує вечірні дані з високим споживанням і умовами по субметрингах.
  - `Нормалізація та стандартизація:`
    - `normalization(df)` — масштабування значень у [0,1].
    - `standardization(df)` — стандартизація (z-score).
  - `Кореляційний аналіз:`
    - `pearson_correlation(df)` — коефіцієнт Пірсона між активною потужністю та інтенсивністю.
    - `spearman_correlation(df)` — коефіцієнт Спірмена між активною потужністю та інтенсивністю.
  - `One-Hot кодування:`
    - `one_hot_encoding(df)` — кодує періоди доби (`night`, `morning`, `day`, `evening`) як one-hot змінні.
      
### Субметринги (Sub_metering)

У датасеті `household_power_consumption.txt` три субметринги показують споживання електроенергії окремими групами приладів:
- `Sub_metering_1` — кухонні прилади, наприклад: бойлер, холодильник, духовка.
- `Sub_metering_2` — великі побутові прилади: пральна машина, посудомийка та інші подібні.
- `Sub_metering_3` — освітлення та кондиціонування, або інші специфічні прилади будинку.

## 🧑‍💻 Приклад використання
```
# Завантаження VHI
download_file()

# Конвертація CSV у DataFrame
csv_to_df()
change_indexes()
merge_dfs()

# Фільтрування та аналіз
filter_province_year(province_id, year)
province_filtred_ids = [1,2,3]
years_filtered = [1984,1985]
filter_provinces_years(province_filtred_ids, years_filtered)
filter_stats_provinces_years(province_filtred_ids, years_filtered)

# Завантаження та аналіз електропостачання
df = txt_to_df("data/household_power_consumption.txt")
normalized_df = normalization(df)
standardized_df = standardization(df)
pearson = pearson_correlation(df)
encoded_df = one_hot_encoding(df)
```
