from tkinter import*
import tkinter.messagebox
from tkinter import messagebox
import tkinter as tk
import sqlite3
import pandas as pd
import folium
from folium import plugins
import webbrowser
from random import randint
import distinctipy

Path_CSV_NAFOBoundary = './External_Import/AreaCalculated_Import/CSV_AreaProfile/DFO_NL_ASOP_NAFOAreaProfile.csv'
DB_SetCatch_Validation_Range = ("./BackEnd/Sqlite3_DB/QC_Check_RangeConsistency_DB/DFO_NL_ASOP_SetCatch_RangeValidation.db")
DB_SetCatch_Val_Calculation = ("./BackEnd/Sqlite3_DB/QC_Check_CalculationConsistency_DB/DFO_NL_ASOP_SetCatch_Calculation.db")
Path_CSV_NAFOBoundary_WithExZone = './External_Import/AreaCalculated_Import/CSV_AreaProfile/DFO_NL_ASOP_NAFOAreaProfile_WithExZone.csv'
Path_html_PlotOut = './TempData/NAFOAreaPlot.html'

def Plot_NAFOArea_QCFailList():
    
    def fetchData_NAFO_AreaProfile():
        sqliteConnection = sqlite3.connect(DB_SetCatch_Val_Calculation)
        cursor = sqliteConnection.cursor()
        NAFO_AreaCSV_DF = pd.read_sql_query("SELECT * FROM SetCatch_NAFO_AreaProfileImported;", sqliteConnection)
        cursor.close()
        sqliteConnection.close()
        return NAFO_AreaCSV_DF

    def StoredHexColorListCode():
        constant_hex_color_codes = [
    "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF",
    "#00FFFF", "#FFA500", "#A52A2A", "#800080", "#008000",
    "#000080", "#808080", "#C0C0C0", "#800000", "#008080",
    "#FFD700", "#00FFD4", "#B22222", "#7CFC00", "#8B008B",
    "#B8860B", "#2E8B57", "#4B0082", "#FF6347", "#40E0D0",
    "#FF4500", "#DA70D6", "#00CED1", "#FF8C00", "#9932CC",
    "#8FBC8F", "#483D8B", "#2F4F4F", "#00FA9A", "#00BFFF",
    "#FF1493", "#228B22", "#DAA520", "#8A2BE2", "#20B2AA",
    "#FF69B4", "#7B68EE", "#32CD32", "#6495ED", "#FF7F50",
    "#4169E1", "#1E90FF", "#FF4500", "#DC143C", "#00FFFF",
    "#7FFFD4", "#0000CD", "#000080", "#FFD700", "#8B4513",
    "#5F9EA0", "#D2691E", "#00CED1", "#00FF7F", "#B0E0E6",
    "#8A2BE2", "#6495ED", "#A0522D", "#2F4F4F", "#FF6347",
    "#8B0000", "#66CDAA", "#8B008B", "#5F9EA0", "#008B8B",
    "#B8860B", "#8B4513", "#32CD32", "#6495ED", "#FF4500",
    "#DC143C", "#00FFFF", "#7FFFD4", "#0000CD", "#000080",
    "#FFD700", "#8B4513", "#5F9EA0", "#D2691E", "#00CED1",
    "#00FF7F", "#B0E0E6", "#8A2BE2", "#6495ED", "#A0522D",
    "#2F4F4F", "#FF6347", "#8B0000", "#66CDAA", "#8B008B",
    "#5F9EA0", "#008B8B", "#B8860B", "#8B4513", "#32CD32",
    "#6495ED", "#FF4500", "#DC143C", "#00FFFF", "#7FFFD4",
    "#0000CD", "#000080", "#FFD700", "#8B4513", "#5F9EA0",
    "#D2691E", "#00CED1", "#00FF7F", "#B0E0E6", "#8A2BE2",
    "#6495ED", "#A0522D", "#2F4F4F", "#FF6347", "#8B0000",
    "#66CDAA", "#8B008B", "#5F9EA0", "#008B8B", "#B8860B",
    "#8B4513", "#32CD32", "#6495ED", "#FF4500", "#DC143C"
]
        return constant_hex_color_codes

    def ReadNAFOBoundaryCSV():
        try:
            df_CSV_NAFOBoundary = pd.read_csv(Path_CSV_NAFOBoundary_WithExZone, sep=',' , low_memory=False)
            df_CSV_NAFOBoundary = df_CSV_NAFOBoundary.reset_index(drop=True)
            df_CSV_NAFOBoundary = pd.DataFrame(df_CSV_NAFOBoundary)
            df_CSV_NAFOBoundary[['NAFO_ID', 'NAFO_PointOrder']] = df_CSV_NAFOBoundary[
                                                ['NAFO_ID','NAFO_PointOrder']].astype(int)
            df_CSV_NAFOBoundary[['NAFO_Latitude', 'NAFO_Longitude']] = df_CSV_NAFOBoundary[
                                                ['NAFO_Latitude', 'NAFO_Longitude']].astype(float)
            
            df_CSV_NAFOBoundary.sort_values(by=['NAFODivision', 'NAFOLabel','NAFO_PointOrder'], inplace=True)
            df_CSV_NAFOBoundary['NAFOPoints'] = list(zip(df_CSV_NAFOBoundary.NAFO_Latitude, df_CSV_NAFOBoundary.NAFO_Longitude))
            df_CSV_NAFOBoundary = df_CSV_NAFOBoundary.groupby('NAFOLabel').agg({'NAFOPoints': lambda x: list(x)})
            df_CSV_NAFOBoundary.reset_index(inplace=True)
            df_CSV_NAFOBoundary= df_CSV_NAFOBoundary.reset_index(drop=True)
            df_CSV_NAFOBoundary = df_CSV_NAFOBoundary.loc[:,['NAFOLabel', 'NAFOPoints']]
            df_CSV_NAFOBoundary.rename(columns={'NAFOLabel':'NAFODivision', 
            'NAFOPoints':'NAFOPoints'},inplace = True)
            NAFOBoundaryDF = pd.DataFrame(df_CSV_NAFOBoundary)
            return NAFOBoundaryDF
        except:
            messagebox.showerror('DFO-NL-ASOP NAFO Table Generation Error Message', 
                                "Void DFO-NL-ASOP NAFO Table In The Archived Folder, Name - DFO_NL_ASOP_NAFOAreaProfile_WithExZone.csv")
        
    def get_NAFO_AreaQC_dfDB():
        try:
            sqliteConnection = sqlite3.connect(DB_SetCatch_Val_Calculation)
            cursor = sqliteConnection.cursor()
            NAFO_AreaQC_df = pd.read_sql_query("SELECT * FROM SetCatch_NAFO_AreaQCAnalysis;", sqliteConnection)
            length_NAFO_AreaQC_df = len(NAFO_AreaQC_df)
            if length_NAFO_AreaQC_df > 0:
                NAFO_AreaQC_df = NAFO_AreaQC_df[
                ((NAFO_AreaQC_df.NAFOValidityCheck_StartPoints) == 'NAFO-QC Failed')]
                NAFO_AreaQC_df = NAFO_AreaQC_df.loc[:,
                ['DeploymentUID', 'StartPoints','EndPoints', 
                 'NAFODivision', 'GearType']]
                NAFO_AreaQC_df = NAFO_AreaQC_df.reset_index(drop=True)
                NAFO_AreaQC_dfDB = pd.DataFrame(NAFO_AreaQC_df)
                sqliteConnection.commit()
                return NAFO_AreaQC_dfDB, length_NAFO_AreaQC_df
            else:
                messagebox.showerror('Set & Catch Database Is Empty', "Please Import Set & Catch CSV File To View")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def BuildRec_1_QCFailPoints():
        get_NAFO_AreaQC_df = get_NAFO_AreaQC_dfDB()
        ObserverSetCatchDB = get_NAFO_AreaQC_df[0]
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB)
        
        keys_1 =('DeploymentUID', 'NAFODivision', 'StartPoints','EndPoints', 'GearType')
        records_1 = []
        dict_list_1 = ObserverSetCatchDB.to_dict('records')
        for row in dict_list_1:
            records_1.append({key: row[key] for key in keys_1})
        for record in records_1:
            StartLat, StartLon = record['StartPoints'].split("(")[-1].split(")")[0].split()
            StartLat = StartLat.replace(",", "",1)
            record['StartLatitude'] = float(StartLat)
            record['StartLongitude'] = float(StartLon)
            EndLat, EndLon = record['EndPoints'].split("(")[-1].split(")")[0].split()
            EndLat = EndLat.replace(",", "",1)
            record['EndLatitude'] = float(EndLat)
            record['EndLongitude'] = float(EndLon)
        return records_1
    
    def BuildRec_2_NAFOAreaProfile():
        get_NAFOBoundaryCSV = ReadNAFOBoundaryCSV()
        get_NAFOBoundaryCSV  = get_NAFOBoundaryCSV.reset_index(drop=True)
        NAFOBoundaryDF = pd.DataFrame(get_NAFOBoundaryCSV)
        lenRec2 = len(NAFOBoundaryDF)
        hex_color_codes = StoredHexColorListCode()
        colors =[]
        for Index_color in range(lenRec2):
            colors.append(hex_color_codes[Index_color])
        NAFOBoundaryDF['NAFO_Color'] = colors
        NAFOBoundaryDF  = NAFOBoundaryDF.reset_index(drop=True)
        NAFOBoundaryDF = pd.DataFrame(NAFOBoundaryDF)
        
        keys_2 =('NAFODivision', 'NAFOPoints', 'NAFO_Color')
        records_2 = []
        dict_list_2 = NAFOBoundaryDF.to_dict('records')
        for row in dict_list_2:
            records_2.append({key: row[key] for key in keys_2})
        return records_2
    
    records_1 = BuildRec_1_QCFailPoints()
    records_2 = BuildRec_2_NAFOAreaProfile()

    f = folium.Figure(width=1000, height=500)
    PointMap = folium.Map(location =[49.1783, -58.0322], zoom_start =5, 
                          crs='EPSG3857', max_bounds = True).add_to(f)

    for record in records_2:
        folium.Polygon(record['NAFOPoints'],
                       tooltip=record['NAFODivision'],
                       popup= 'NAFODiv : ' + record['NAFODivision'],
                       color =record['NAFO_Color'],
                       weight =1,
                       fill = True,
                       fill_color=record['NAFO_Color'],
                       fill_opacity =0.6).add_to(PointMap)
        
    for record in records_1:
        StartCords = (record['StartLatitude'], record['StartLongitude'])
        EndCords = (record['EndLatitude'], record['EndLongitude'])
        html = '''DeploymentUID :   ''' + (record['DeploymentUID']) + '''<br>'''\
               '''Assigned NAFO :   ''' + (record['NAFODivision'])  + '''<br>'''\
               '''Assigned GearType :  '''   + (str(record['GearType'])) + '''<br>'''\
               '''Start Point :  '''   + (str(StartCords))
        iframe = folium.IFrame(html,
                       width=500,
                       height=90)
        popup = folium.Popup(iframe,
                     max_width=250)
        
        folium.PolyLine([StartCords, EndCords],
                        tooltip=record['DeploymentUID'],
                        popup='Assigned NAFO : ' + record['NAFODivision'],
                        color ="blue",
                        weight =1,
                        fill = True,
                        fill_color="blue",
                        fill_opacity =0.6
                        ).add_to(PointMap)
        folium.CircleMarker(StartCords,
                      tooltip= record['DeploymentUID'],
                      popup= popup,
                      color ="red",
                      fill = True,
                      radius = 2,
                      weight =1
                      ).add_to(PointMap)
    
    PointMap.save('NAFOAreaPlotQC.html')
    webbrowser.open('NAFOAreaPlotQC.html')
    
