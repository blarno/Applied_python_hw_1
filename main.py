import streamlit as st
import pandas as pd
import plotly.express as px


data = pd.read_csv('prepared_data.csv', index_col = [0])

st.title("Разведочный анализ данных")

genders = st.sidebar.multiselect('Выберите пол', data['GENDER'].unique())
AGE = st.sidebar.slider("Выберите возраст", 20, 68, (20, 68))
data = data[data['GENDER'].isin(genders)]
data = data[data["AGE"].between(AGE[0], AGE[1])]

st.subheader('Посмотрим на числовые характеристики столбцов')
st.write(data.describe())
st.write('После очистки от Nan, осталось 15223 строки')
st.write('что интересно - минимальное значение дохода 24 у.е., при максимальном 250к :)')

corr = px.imshow(
  data.drop('FAMILY_INCOME', axis = 1).corr(),
  color_continuous_scale="Inferno_r",
)
# Show plot
st.plotly_chart(corr)

st.write('Наибольшие корреляции между признаками AGREEMENT_RK и ID_CLIENT, которые оба являются id и в целом корреляцию иметь не должны')

st.write('Также большая корреляция между количеством взятых кредитов и количеством закрытых')

st.subheader('Посмотрим на распределение дохода семьи на скрипичном графике')

violin = px.violin(data, x="FAMILY_INCOME", y="AGE")

st.plotly_chart(violin)

st.write('В возрасте около 55 лет очень много людей с доходом ниже 5000')
st.write('В возрасте около 30 лет же, наоборот, с большим оходом семьи - больше 50т рублей')

scatter_age_income = px.scatter(data, x='AGE',
                y='PERSONAL_INCOME',
                color='TARGET',
                size='PERSONAL_INCOME',
                hover_data=['GENDER'])
st.plotly_chart(scatter_age_income)

st.write('Визуально target по возрасту распределен более менее равномерно, однако после ~50 лет наблюдений с 1 все меньше')

st.subheader('Посмотрим на scatter самых закоррелированных признаков')

scatter_id_agreement = px.scatter(data, x='AGREEMENT_RK',
                y='ID_CLIENT')
st.plotly_chart(scatter_id_agreement)

st.write('да, корреляция действительно есть :)')

scatter_loans = px.scatter(data, x='LOAN_NUM_TOTAL',
                y='LOAN_NUM_CLOSED')
st.plotly_chart(scatter_loans)

st.write('А здесь достаточно мало разнообразия в данных, однако корреляция тоже видна')

st.subheader('А теперь посмотрим на самые закореллированные с целевой переменной признаки (Корреляции очень маленькие, поэтому увидим мало)')

scattter_TARGET_income = px.scatter(data, x='TARGET',
                y='PERSONAL_INCOME')
st.plotly_chart(scattter_TARGET_income)

st.write('Тк задача классификации, такой график нам мало чего дает')


