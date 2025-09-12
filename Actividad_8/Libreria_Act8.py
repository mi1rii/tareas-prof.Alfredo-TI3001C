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