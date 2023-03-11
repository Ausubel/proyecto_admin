import pandas as pd
DF_CARRERAS = pd.read_excel('vaca.xlsx', names=['CARRERA_PROFESIONAL', 'VACANTES'])
CARRERAS = DF_CARRERAS['CARRERA_PROFESIONAL'].to_list()
VACANTES = DF_CARRERAS['VACANTES'].to_list()
for i, carrera in enumerate(CARRERAS):
    df = pd.read_csv(f'sdf/{carrera}.csv')
    df = df.sort_values('puntaje', ascending=False)
    df['N° Ord'] = df.index + 1
    df['MERITO'] = df.index + 1
    if len(df) > VACANTES[i]:
        last_admitted_score = df.iloc[VACANTES[i]-1]['puntaje']
        df['CONDICION'] = df.apply(lambda row: 'INGRESO' if row['puntaje'] >= last_admitted_score else 'NO INGRESO', axis=1)
    else:
        df['CONDICION'] = 'INGRESO'
    df['APELLIDOS Y NOMBRES'] = df['APELLIDO PATERNO'].str.cat(df['APELLIDO MATERNO'], sep=' ')
    df['APELLIDOS Y NOMBRES'] = df['APELLIDOS Y NOMBRES'].str.cat(df['NOMBRES'], sep=' ')
    df = df.rename(columns={'puntaje': 'PUNTAJE','codigo':'CODIGO'})
    df = df[['N° Ord','CODIGO','APELLIDOS Y NOMBRES', 'PUNTAJE','MERITO', 'CONDICION']]
    df.to_csv(f'REPORTES/REPORTE_{carrera}.csv', index=False)