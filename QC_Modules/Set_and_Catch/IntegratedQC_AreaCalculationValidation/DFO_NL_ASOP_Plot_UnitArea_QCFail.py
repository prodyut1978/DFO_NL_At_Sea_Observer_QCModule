from tkinter import*
import tkinter.messagebox
from tkinter import messagebox
import tkinter as tk
import sqlite3
import pandas as pd
from shapely.geometry import Point, Polygon, MultiPolygon, MultiPoint
from shapely import geometry
import folium
from folium import plugins
import webbrowser
from random import randint

Path_CSV_unitAreaBoundary = './External_Import/AreaCalculated_Import/CSV_AreaProfile/DFO_NL_ASOP_UnitAreaProfile.csv'
DB_SetCatch_Validation_Range = ("./BackEnd/Sqlite3_DB/QC_Check_RangeConsistency_DB/DFO_NL_ASOP_SetCatch_RangeValidation.db")
DB_SetCatch_Val_Calculation = ("./BackEnd/Sqlite3_DB/QC_Check_CalculationConsistency_DB/DFO_NL_ASOP_SetCatch_Calculation.db")
Path_html_PlotOut = './TempData/UnitAreaPlot.html'

def Plot_UnitArea_QCFailList():

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
        "#8B4513", "#32CD32", "#6495ED", "#FF4500", "#DC143C"]
        return constant_hex_color_codes

    def ReadUnitAreaBoundaryCSV():
        try:
            df_CSV_UnitAreaBoundary = pd.read_csv(Path_CSV_unitAreaBoundary, sep=',' , low_memory=False)
            df_CSV_UnitAreaBoundary = df_CSV_UnitAreaBoundary.reset_index(drop=True)
            df_CSV_UnitAreaBoundary = pd.DataFrame(df_CSV_UnitAreaBoundary)
            df_CSV_UnitAreaBoundary[['UnitArea_ID', 'PointOrder']] = df_CSV_UnitAreaBoundary[
                                                ['UnitArea_ID','PointOrder']].astype(int)
            df_CSV_UnitAreaBoundary[['UnitArea_Latitude', 'UnitArea_Longitude']] = df_CSV_UnitAreaBoundary[
                                    ['UnitArea_Latitude', 'UnitArea_Longitude']].astype(float)
            
            df_CSV_UnitAreaBoundary.sort_values(by=['NAFODivision', 'UnitArea','PointOrder'], inplace=True)
            df_CSV_UnitAreaBoundary['UnitAreaPoints'] = list(zip(df_CSV_UnitAreaBoundary.UnitArea_Latitude, df_CSV_UnitAreaBoundary.UnitArea_Longitude))
            df_CSV_UnitAreaBoundary = df_CSV_UnitAreaBoundary.groupby('UnitArea').agg({'UnitAreaPoints': lambda x: list(x),
                                                                                       'NAFODivision': lambda x: list(set(x)),
                                                                                       'UnitAreaLabel': lambda x: list(set(x))})
            df_CSV_UnitAreaBoundary.reset_index(inplace=True)
            df_CSV_UnitAreaBoundary= df_CSV_UnitAreaBoundary.reset_index(drop=True)
            df_CSV_UnitAreaBoundary = df_CSV_UnitAreaBoundary.loc[:,['NAFODivision','UnitArea', 
                                                                     'UnitAreaPoints', 'UnitAreaLabel']]
            UnitAreaBoundaryDF = pd.DataFrame(df_CSV_UnitAreaBoundary)
            return UnitAreaBoundaryDF
        except:
            messagebox.showerror('DFO-NL-ASOP UnitArea Table Generation Error Message', 
                                "Void DFO-NL-ASOP UnitArea Table In The Archived Folder, Name - DFO_NL_ASOP_UnitAreaAreaProfile.csv")
        
    def BuildRec_2_UnitAreaProfile():
        get_UnitAreaBoundaryCSV = ReadUnitAreaBoundaryCSV()
        get_UnitAreaBoundaryCSV  = get_UnitAreaBoundaryCSV.reset_index(drop=True)
        UnitAreaBoundaryDF = pd.DataFrame(get_UnitAreaBoundaryCSV)
        lenRec2 = len(UnitAreaBoundaryDF)
        hex_color_codes = StoredHexColorListCode()
        colors =[]
        for Index_color in range(lenRec2):
            colors.append(hex_color_codes[Index_color])
        UnitAreaBoundaryDF['UnitArea_Color'] = colors
        UnitAreaBoundaryDF  = UnitAreaBoundaryDF.reset_index(drop=True)
        UnitAreaBoundaryDF = pd.DataFrame(UnitAreaBoundaryDF)
        
        keys_2 =('NAFODivision','UnitArea', 'UnitAreaPoints', 'UnitAreaLabel', 'UnitArea_Color')
        records_2 = []
        dict_list_2 = UnitAreaBoundaryDF.to_dict('records')
        for row in dict_list_2:
            records_2.append({key: row[key] for key in keys_2})
        return records_2
    
    def get_Unit_AreaQC_dfDB():
        try:
            sqliteConnection = sqlite3.connect(DB_SetCatch_Val_Calculation)
            cursor = sqliteConnection.cursor()
            UnitArea_AreaQC_df = pd.read_sql_query("SELECT * FROM SetCatch_UnitAreaQCAnalysis;", sqliteConnection)
            length_UnitArea_AreaQC_df = len(UnitArea_AreaQC_df)
            if length_UnitArea_AreaQC_df > 0:
                UnitArea_AreaQC_df = UnitArea_AreaQC_df[
                ((UnitArea_AreaQC_df.UAValidityCheck_StartPoints) == 'UnitArea-QC Failed')]
                UnitArea_AreaQC_df = UnitArea_AreaQC_df.loc[:,
                ['DeploymentUID', 'StartPoints','EndPoints', 
                 'NAFODivision', 'UnitArea', 'GearType']]
                UnitArea_AreaQC_df = UnitArea_AreaQC_df.reset_index(drop=True)
                UnitArea_AreaQC_dfDB = pd.DataFrame(UnitArea_AreaQC_df)
                sqliteConnection.commit()
                return UnitArea_AreaQC_dfDB, length_UnitArea_AreaQC_df
            else:
                messagebox.showerror('Set & Catch Database Is Empty', "Please Import Set & Catch CSV File To View")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def BuildRec_1_QCFailPoints():
        get_NAFO_AreaQC_df = get_Unit_AreaQC_dfDB()
        ObserverSetCatchDB = get_NAFO_AreaQC_df[0]
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB)
        keys_1 =('DeploymentUID', 'NAFODivision', 
                 'UnitArea', 'GearType', 'StartPoints','EndPoints')
        records_1 = []
        dict_list_1 = ObserverSetCatchDB.to_dict('records')
        for row in dict_list_1:
            records_1.append({key: row[key] for key in keys_1})
        for record in records_1:
            StartLat, StartLon = record['StartPoints'].split("(")[-1].split(")")[0].split()
            StartLat = StartLat.replace(",", "", 1)
            record['StartLatitude'] = float(StartLat)
            record['StartLongitude'] = float(StartLon)
            EndLat, EndLon = record['EndPoints'].split("(")[-1].split(")")[0].split()
            EndLat = EndLat.replace(",", "",1)
            record['EndLatitude'] = float(EndLat)
            record['EndLongitude'] = float(EndLon)
        return records_1

    records_1 = BuildRec_1_QCFailPoints()
    records_2 = BuildRec_2_UnitAreaProfile()
    f = folium.Figure(width=1000, height=500)
    PointMap = folium.Map(location =[49.1783, -58.0322], zoom_start =5, crs='EPSG3857', max_bounds = True).add_to(f)

    for record in records_2:
        folium.Polygon(record['UnitAreaPoints'],
                       tooltip= str(record['UnitArea']),
                       popup= 'NAFODivCode  : ' + str (record['NAFODivision']) + '   >>>>> AND <<<<<  ' + \
                              'UnitAreaCode  : ' + str (record['UnitAreaLabel']),
                       color =record['UnitArea_Color'],
                       weight =1,
                       fill = True,
                       fill_color=record['UnitArea_Color'],
                       fill_opacity =0.6).add_to(PointMap)

    for record in records_1:
        StartCords = (record['StartLatitude'], record['StartLongitude'])
        EndCords = (record['EndLatitude'], record['EndLongitude'])
        folium.CircleMarker(StartCords,
                      tooltip=record['DeploymentUID'],
                      popup= 'AssignedUnitArea : ' + str(record['UnitArea']) +' & ' + 'GearType : ' + str(record['GearType']),
                      color ="red",
                      fill = True,
                      radius = 2,
                      weight =1
                      ).add_to(PointMap)    
    
    PointMap.save('UnitAreaPlotQC.html')
    webbrowser.open("UnitAreaPlotQC.html")
    
