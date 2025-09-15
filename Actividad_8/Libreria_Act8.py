import pandas as pd
import numpy as np

def cargar_a_df(ruta, tipo=None, **kwargs):
	if tipo is None:
		ext = ruta.split('.')[-1].lower()
		tipo = ext
	funciones = {
		'csv': pd.read_csv,
		'xlsx': pd.read_excel,
		'html': pd.read_html,
		'json': pd.read_json
	}
	if tipo not in funciones:
		raise ValueError('Tipo de archivo no soportado.')
	resultado = funciones[tipo](ruta, **kwargs)
	if tipo == 'html':
		return resultado[0] if isinstance(resultado, list) and len(resultado) == 1 else resultado
	return resultado


def nulos_ffill(df):
	return df.fillna(method='ffill')

def outliers(num, df):
    Q1 = num.quantile(0.25)
	Q3 = num.quantile(0.75)
	IQR = Q3 - Q1
 
	limite_superior_iqr = Q3 + 1.5 * IQR
	limite_inferior_iqr = Q1 - 1.5 * IQR
 
	return df.num[(num <= limite_superior_iqr) & (num >= limite_inferior_iqr)]
 
"""
num = df_limpio.select_dtypes(include=[np.number])

# Calcular Q1, Q3 e IQR
Q1 = num.quantile(0.25)
Q3 = num.quantile(0.75)
IQR = Q3 - Q1

limite_superior_iqr = Q3 + 1.5 * IQR
limite_inferior_iqr = Q1 - 1.5 * IQR

# Límites IQR
print('Límite superior permitido (IQR):')
print(limite_superior_iqr)
print('\nLímite inferior permitido (IQR):')
print(limite_inferior_iqr)

df_outliers_iqr = num[(num <= limite_superior_iqr) & (num >= limite_inferior_iqr)]

# Ver que cuántos valores nulos quedan
print('\nValores nulos tras eliminar outliers (IQR):')
print(df_outliers_iqr.isnull().sum())

plt.figure(figsize=(15, 8))
df_outliers_iqr.plot(kind='box', vert=False)
plt.title('Valores Atípicos eliminados por Rango Intercuartílico (IQR)')
plt.show()
"""


def nulos_bfill(df):
	return df.fillna(method='bfill')


def nulos_string(df, valor):
	df_copia = df.copy()
	cols_str = df_copia.select_dtypes(include=['object', 'string']).columns
	if len(cols_str) > 0:
		df_copia[cols_str] = df_copia[cols_str].where(~df_copia[cols_str].isnull(), valor)
	return df_copia


def nulos_promedio(df):
	df_copia = df.copy()
	num_cols = df_copia.select_dtypes(include=[np.number]).columns
	promedios = {col: df_copia[col].mean() for col in num_cols}
	df_copia[num_cols] = df_copia[num_cols].fillna(promedios)
	return df_copia


def nulos_mediana(df):
	df_copia = df.copy()
	num_cols = df_copia.select_dtypes(include=[np.number]).columns
	medianas = {col: df_copia[col].median() for col in num_cols}
	df_copia[num_cols] = df_copia[num_cols].fillna(medianas)
	return df_copia


def nulos_constante(df, valor):
	df_copia = df.copy()
	num_cols = df_copia.select_dtypes(include=[np.number]).columns
	df_copia[num_cols] = df_copia[num_cols].fillna(valor)
	return df_copia


def resumen_nulos(df):
	nulos_columna = df.isnull().sum()
	total_nulos = df.isnull().sum().sum()
	return pd.DataFrame({'nulos_por_columna': nulos_columna, 'total_nulos_en_df': total_nulos})