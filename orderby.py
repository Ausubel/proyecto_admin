import pandas as pd
DF_CARRERAS = pd.read_excel('vaca.xlsx', names=['CARRERA_PROFESIONAL', 'VACANTES'])
CARRERAS = DF_CARRERAS['CARRERA_PROFESIONAL'].to_list()
VACANTES = DF_CARRERAS['VACANTES'].to_list()
for i, carrera in enumerate(CARRERAS):
    df = pd.read_csv(f'sdf/{carrera}.csv')
    df = df.sort_values('puntaje', ascending=False)
    df['Merito'] = df.index + 1
    if len(df) > VACANTES[i]:
        last_admitted_score = df.iloc[VACANTES[i]-1]['puntaje']
        df['Condicion'] = df.apply(lambda row: 'INGRESO' if row['puntaje'] >= last_admitted_score else 'NO INGRESO', axis=1)
    else:
        df['Condicion'] = 'INGRESO'
    df = df.rename(columns={'APELLIDO PATERNO': 'APELLIDO_PATERNO', 'APELLIDO MATERNO': 'APELLIDO_MATERNO', 'NOMBRES': 'NOMBRES_COMPLETOS', 'puntaje': 'PUNTAJE', 'Merito': 'MERITO','Condicion': 'CONDICION','codigo':'CODIGO'})
    df = df[['CODIGO','APELLIDO_PATERNO', 'APELLIDO_MATERNO', 'NOMBRES_COMPLETOS', 'PUNTAJE','MERITO', 'CONDICION']]
    df.to_csv(f'REPORTES/REPORTE_{carrera}.csv', index=False)