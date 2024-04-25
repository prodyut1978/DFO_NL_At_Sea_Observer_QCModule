from tkinter import*
from tkinter import messagebox
import sqlite3
import pandas as pd
import numpy as np

### Database Connection
DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_SetCatch_Validation_Logical = ("./BackEnd/Sqlite3_DB/QC_Check_LogicalConsistency_DB/DFO_NL_ASOP_SetCatch_LogicalValidation.db")

def RunSetCatch_LogicalValidation_BackEnd():
    
    def RunLogicalFailed_CatchVariables():
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                                                        'CodendMeshSize','MeshSizeMG','NumberPotReleasedCrab',
                                                                        'DirectedSpecies','EstimatedWeightReleasedCrab','KeptWeight',
                                                                        'DiscardWeight']]
                    SetCatchProfileDB_DF  = SetCatchProfileDB_DF.reset_index(drop=True)
                    SetCatchProfileDB_DF  = pd.DataFrame(SetCatchProfileDB_DF)
                    return SetCatchProfileDB_DF
                else:
                    messagebox.showerror('DFO-NL-ASOP Set & Catch DB Message', "Void DFO-NL-ASOP Set & Catch DB...Please Import DFO-NL-ASOP Set & Catch CSV Files")
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()

        def Submit_LogicalCatch_DB(
                CodendMeshSize_FailLogical, DirectedSpecies_FailLogical,
                NumberPotReleasedCrab_FailLogical, KeptWeight_DiscardWeight_FailLogical):
            try:
                CodendMeshSize_FailLogical = pd.DataFrame(CodendMeshSize_FailLogical)
                DirectedSpecies_FailLogical = pd.DataFrame(DirectedSpecies_FailLogical)
                NumberPotReleasedCrab_FailLogical = pd.DataFrame(NumberPotReleasedCrab_FailLogical)
                KeptWeight_DiscardWeight_FailLogical = pd.DataFrame(KeptWeight_DiscardWeight_FailLogical)
                
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Logical)
                cursor = sqliteConnection.cursor()
                CodendMeshSize_FailLogical.to_sql('SetCatch_QCFailedLogical_CatchVariable_CodendMeshSize',
                                            sqliteConnection, if_exists="replace", index =False)
                DirectedSpecies_FailLogical.to_sql('SetCatch_QCFailedLogical_CatchVariable_DirectedSpecies',
                                            sqliteConnection, if_exists="replace", index =False)
                NumberPotReleasedCrab_FailLogical.to_sql('SetCatch_QCFailedLogical_CatchVariable_NumberPotReleasedCrab',
                                            sqliteConnection, if_exists="replace", index =False)
                KeptWeight_DiscardWeight_FailLogical.to_sql('SetCatch_QCFailedLogical_CatchVariable_KeptWeight_DiscardWeight',
                                            sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        SetCatchProfileDB_DF = GetSetCatchProfileDB()
    
        ## QC On CodendMeshSize
        CodendMeshSize_FailLogical= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'CodendMeshSize','MeshSizeMG','RecordType']]).replace(['','None'], 99999999)
        
        CodendMeshSize_FailLogical[['DataBase_ID','RecordIdentifier','CodendMeshSize',
                            'MeshSizeMG','RecordType']] = CodendMeshSize_FailLogical[
                            ['DataBase_ID','RecordIdentifier','CodendMeshSize',
                            'MeshSizeMG','RecordType']
                            ].astype(int)
        CodendMeshSize_FailLogical = CodendMeshSize_FailLogical[
                                        (CodendMeshSize_FailLogical.CodendMeshSize !=99999999) &\
                                        (CodendMeshSize_FailLogical.MeshSizeMG !=99999999)
                                    ]
        CodendMeshSize_FailLogical = CodendMeshSize_FailLogical[
                                (CodendMeshSize_FailLogical.CodendMeshSize > CodendMeshSize_FailLogical.MeshSizeMG) 
                                    ]
        CodendMeshSize_FailLogical= (CodendMeshSize_FailLogical.loc[:,[
                                    'DataBase_ID','RecordIdentifier', 'DeploymentUID',
                                    'CodendMeshSize','MeshSizeMG','RecordType']]).replace([99999999], '')
        CodendMeshSize_FailLogical['QCCodendMeshSize'] ="CodendMeshSize =< MeshSize_MG"
        CodendMeshSize_FailLogical['QC_CaseType'] ="Case: CodendMeshSize - MeshSizeMG"
        CodendMeshSize_FailLogical  = CodendMeshSize_FailLogical.reset_index(drop=True)
        CodendMeshSize_FailLogical  = pd.DataFrame(CodendMeshSize_FailLogical)
        
        
        ## QC On DirectedSpecies
        DirectedSpecies_FailLogical= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier', 'DeploymentUID',
                            'NumberPotReleasedCrab','DirectedSpecies','RecordType']]).replace(['','None'], 99999999)
        
        DirectedSpecies_FailLogical[['DataBase_ID','RecordIdentifier','NumberPotReleasedCrab',
                            'DirectedSpecies','RecordType']] = DirectedSpecies_FailLogical[
                            ['DataBase_ID','RecordIdentifier','NumberPotReleasedCrab',
                            'DirectedSpecies','RecordType']
                            ].astype(int)
        DirectedSpecies_FailLogical = DirectedSpecies_FailLogical[
                                        (DirectedSpecies_FailLogical.NumberPotReleasedCrab !=99999999) &\
                                        (DirectedSpecies_FailLogical.DirectedSpecies !=8213)
                                    ]
        DirectedSpecies_FailLogical= (DirectedSpecies_FailLogical.loc[:,[
                                    'DataBase_ID','RecordIdentifier','DeploymentUID',
                                    'NumberPotReleasedCrab','DirectedSpecies','RecordType']]).replace([99999999], '')
        DirectedSpecies_FailLogical['QCDirectedSpecies'] ="If NPRC Non-Blank Then DS Must Be 8213"
        DirectedSpecies_FailLogical['QC_CaseType'] ="Case: NumberPotReleasedCrab (NPRC) - DirectedSpecies (DS)"
        DirectedSpecies_FailLogical  = DirectedSpecies_FailLogical.reset_index(drop=True)
        DirectedSpecies_FailLogical  = pd.DataFrame(DirectedSpecies_FailLogical)
    
        ## QC On NumberPotReleasedCrab
        NumberPotReleasedCrab_FailLogical= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'EstimatedWeightReleasedCrab','NumberPotReleasedCrab','RecordType']]).replace(['','None'], 99999999)
        
        NumberPotReleasedCrab_FailLogical[['DataBase_ID','RecordIdentifier','EstimatedWeightReleasedCrab',
                            'NumberPotReleasedCrab','RecordType']] = NumberPotReleasedCrab_FailLogical[
                            ['DataBase_ID','RecordIdentifier','EstimatedWeightReleasedCrab',
                            'NumberPotReleasedCrab','RecordType']
                            ].astype(int)
        NumberPotReleasedCrab_FailLogical = NumberPotReleasedCrab_FailLogical[
                                        (NumberPotReleasedCrab_FailLogical.EstimatedWeightReleasedCrab !=99999999) &\
                                        ((NumberPotReleasedCrab_FailLogical.NumberPotReleasedCrab <=0)|
                                        (NumberPotReleasedCrab_FailLogical.NumberPotReleasedCrab ==99999999))
                                    ]
        NumberPotReleasedCrab_FailLogical= (NumberPotReleasedCrab_FailLogical.loc[:,[
                                    'DataBase_ID','RecordIdentifier','DeploymentUID',
                                    'EstimatedWeightReleasedCrab','NumberPotReleasedCrab','RecordType']]).replace([99999999], '')
        NumberPotReleasedCrab_FailLogical['QCNumberPotReleasedCrab'] ="If EWRC == Non-Blank Then NPRC > 0 or Non-Blank"
        NumberPotReleasedCrab_FailLogical['QC_CaseType'] ="Case: EstimatedWeightReleasedCrab (EWRC) - NumberPotReleasedCrab (NPRC)"
        NumberPotReleasedCrab_FailLogical  = NumberPotReleasedCrab_FailLogical.reset_index(drop=True)
        NumberPotReleasedCrab_FailLogical  = pd.DataFrame(NumberPotReleasedCrab_FailLogical)

        ## QC On KeptWeight_DiscardWeight
        KeptWeight_DiscardWeight_FailLogical= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier', 'DeploymentUID',
                            'KeptWeight','DiscardWeight','RecordType']]).replace(['','None'], 99999999)
        
        KeptWeight_DiscardWeight_FailLogical[['DataBase_ID','RecordIdentifier','KeptWeight',
                            'DiscardWeight','RecordType']] = KeptWeight_DiscardWeight_FailLogical[
                            ['DataBase_ID','RecordIdentifier', 'KeptWeight',
                            'DiscardWeight','RecordType']
                            ].astype(int)
        KeptWeight_DiscardWeight_FailLogical = KeptWeight_DiscardWeight_FailLogical[
                                (KeptWeight_DiscardWeight_FailLogical.RecordType == 2)]
        KeptWeight_DiscardWeight_FailLogical = KeptWeight_DiscardWeight_FailLogical[
                                        ((KeptWeight_DiscardWeight_FailLogical.KeptWeight !=99999999) &\
                                        (KeptWeight_DiscardWeight_FailLogical.KeptWeight <1))|
                                        ((KeptWeight_DiscardWeight_FailLogical.DiscardWeight !=99999999)&\
                                        (KeptWeight_DiscardWeight_FailLogical.DiscardWeight <1))
                                    ]
        
        KeptWeight_DiscardWeight_FailLogical= (KeptWeight_DiscardWeight_FailLogical.loc[:,[
                                    'DataBase_ID','RecordIdentifier', 'DeploymentUID',
                                    'KeptWeight','DiscardWeight','RecordType']]).replace([99999999], np.nan)
        KeptWeight_DiscardWeight_FailLogical['Sum'] = KeptWeight_DiscardWeight_FailLogical['KeptWeight'].fillna(0)+\
                                                    KeptWeight_DiscardWeight_FailLogical['DiscardWeight'].fillna(0)
        KeptWeight_DiscardWeight_FailLogical = KeptWeight_DiscardWeight_FailLogical[
                                            (KeptWeight_DiscardWeight_FailLogical.Sum <1)
                                                ]
        KeptWeight_DiscardWeight_FailLogical = KeptWeight_DiscardWeight_FailLogical.loc[:,
                                                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                'KeptWeight','DiscardWeight','RecordType']]
        KeptWeight_DiscardWeight_FailLogical= (KeptWeight_DiscardWeight_FailLogical.loc[:,
                            ['DataBase_ID','RecordIdentifier', 'DeploymentUID',
                            'KeptWeight','DiscardWeight','RecordType']]).replace([np.nan], 99999999)
        KeptWeight_DiscardWeight_FailLogical[['DataBase_ID','RecordIdentifier', 'KeptWeight',
                            'DiscardWeight','RecordType']] = KeptWeight_DiscardWeight_FailLogical[
                            ['DataBase_ID','RecordIdentifier', 'KeptWeight',
                            'DiscardWeight','RecordType']
                            ].astype(int)
        KeptWeight_DiscardWeight_FailLogical= (KeptWeight_DiscardWeight_FailLogical.loc[:,[
                            'DataBase_ID','RecordIdentifier', 'DeploymentUID',
                            'KeptWeight','DiscardWeight','RecordType']]).replace([99999999], '')
        
        KeptWeight_DiscardWeight_FailLogical['QCKeptWeight_DiscardWeight'] ="KeptWeight + DiscardWeight => 1"
        KeptWeight_DiscardWeight_FailLogical['QC_CaseType'] ="Case: KeptWeight - DiscardWeight"
        KeptWeight_DiscardWeight_FailLogical  = KeptWeight_DiscardWeight_FailLogical.reset_index(drop=True)
        KeptWeight_DiscardWeight_FailLogical  = pd.DataFrame(KeptWeight_DiscardWeight_FailLogical)
        
        ## Submit To Logical Catch DB Storage
        Submit_LogicalCatch_DB(
                CodendMeshSize_FailLogical, DirectedSpecies_FailLogical,
                NumberPotReleasedCrab_FailLogical, KeptWeight_DiscardWeight_FailLogical)
        Length_FailedLogicalCatchlDF = (len(CodendMeshSize_FailLogical)+\
                                len(DirectedSpecies_FailLogical) +\
                                len(NumberPotReleasedCrab_FailLogical)+\
                                len(KeptWeight_DiscardWeight_FailLogical))
        return Length_FailedLogicalCatchlDF
    
    def RunLogicalFailed_RecordType_SetNumber():
        
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                                                        'DeploymentNumber','SetNumber']]
                    SetCatchProfileDB_DF  = SetCatchProfileDB_DF.reset_index(drop=True)
                    SetCatchProfileDB_DF  = pd.DataFrame(SetCatchProfileDB_DF)
                    return SetCatchProfileDB_DF
                else:
                    messagebox.showerror('DFO-NL-ASOP Set & Catch DB Message', "Void DFO-NL-ASOP Set & Catch DB...Please Import DFO-NL-ASOP Set & Catch CSV Files")
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()

        def Submit_RecordType_SetNumber_DB(
                Ref_FailedQC_InSetcatchDB, QC_FailLogical_RSSummary):
            try:
                Ref_FailedQC_InSetcatchDB = pd.DataFrame(Ref_FailedQC_InSetcatchDB)
                QC_FailLogical_RSSummary = pd.DataFrame(QC_FailLogical_RSSummary)
                
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Logical)
                cursor = sqliteConnection.cursor()
                Ref_FailedQC_InSetcatchDB.to_sql('SetCatch_QCFailedLogical_RecordType_SetNumber',
                                            sqliteConnection, if_exists="replace", index =False)
                QC_FailLogical_RSSummary.to_sql('Logical_RecordType_SetNumber_FailSummary',
                                            sqliteConnection, if_exists="replace", index =False)
            
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()
    
        ## Get Set& Catch DB profile
        SetCatchProfileDB_DF = GetSetCatchProfileDB()
    
        ## QC On RecordType_SetNumber
        RecordType_SetNumber_FailLogical= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'DeploymentNumber','SetNumber','RecordType']]).replace(['','None'], 99999999)
        
        RecordType_SetNumber_FailLogical[['DataBase_ID','RecordIdentifier',
                            'DeploymentNumber','SetNumber', 'RecordType']] = RecordType_SetNumber_FailLogical[
                            ['DataBase_ID','RecordIdentifier',
                            'DeploymentNumber','SetNumber', 'RecordType']
                            ].astype(int)
        RecordType_SetNumber_FailLogical[['DeploymentUID']] = RecordType_SetNumber_FailLogical[['DeploymentUID']].astype(str)

        ## Building QC_FailLogical_RSSummary_1
        QC_FailLogical_RSSummary1   = RecordType_SetNumber_FailLogical.groupby(
            ['DeploymentUID', 'DeploymentNumber', 'SetNumber', 'RecordType'], as_index=False).DataBase_ID.count()
        QC_FailLogical_RSSummary1   = pd.DataFrame(QC_FailLogical_RSSummary1)
        QC_FailLogical_RSSummary1.rename(columns={'DeploymentUID':'DeploymentUID',
                                                 'DeploymentNumber':'DeploymentNumber',
                                                 'SetNumber':'SetNumber',
                                                 'RecordType': 'RecordType', 
                                                 'DataBase_ID':'CountRecType1PresencePerSet'},inplace = True)
        QC_FailLogical_RSSummary1 = QC_FailLogical_RSSummary1[(QC_FailLogical_RSSummary1.RecordType == 1)&
                                            (QC_FailLogical_RSSummary1.CountRecType1PresencePerSet > 1)]
        
        QC_FailLogical_RSSummary1[
            ['DeploymentNumber','SetNumber', 'RecordType']] = QC_FailLogical_RSSummary1[
            ['DeploymentNumber','SetNumber', 'RecordType']].replace([99999999], '')
        QC_FailLogical_RSSummary1  = QC_FailLogical_RSSummary1.reset_index(drop=True)
        QC_FailLogical_RSSummary1  = pd.DataFrame(QC_FailLogical_RSSummary1)
        
        ## Building QC_FailLogical_RSSummary_2
        QC_FailLogical_RSSummary2   = RecordType_SetNumber_FailLogical.groupby(
            ['DeploymentUID', 'DeploymentNumber','SetNumber'], as_index=False)['RecordType'].apply(lambda x: sum((x==1)))
        QC_FailLogical_RSSummary2.rename(columns={'DeploymentUID':'DeploymentUID',
                                                  'DeploymentNumber':'DeploymentNumber',
                                                  'SetNumber':'SetNumber',
                                                  'RecordType': 'CountRecType1PresencePerSet'
                                                },inplace = True)
        QC_FailLogical_RSSummary2 = QC_FailLogical_RSSummary2[(QC_FailLogical_RSSummary2.CountRecType1PresencePerSet == 0)]
        QC_FailLogical_RSSummary2['RecordType'] =1
        QC_FailLogical_RSSummary2 = QC_FailLogical_RSSummary2.loc[:,['DeploymentUID', 'DeploymentNumber','SetNumber',
                                                                    'RecordType','CountRecType1PresencePerSet']]
        QC_FailLogical_RSSummary2[
            ['DeploymentNumber','SetNumber', 'RecordType']] = QC_FailLogical_RSSummary2[
            ['DeploymentNumber','SetNumber', 'RecordType']].replace([99999999], '')
        QC_FailLogical_RSSummary2  = QC_FailLogical_RSSummary2.reset_index(drop=True)
        QC_FailLogical_RSSummary2  = pd.DataFrame(QC_FailLogical_RSSummary2)

         ## Combining QC_FailLogical_RSSummary1 & QC_FailLogical_RSSummary2
        QC_FailLogical_RSSummary = pd.concat([QC_FailLogical_RSSummary1, QC_FailLogical_RSSummary2])
        QC_FailLogical_RSSummary = QC_FailLogical_RSSummary.drop_duplicates(subset='DeploymentUID', keep="first")
        QC_FailLogical_RSSummary.sort_values(by=['DeploymentUID','DeploymentNumber','SetNumber','RecordType'], inplace=True)
        QC_FailLogical_RSSummary  = QC_FailLogical_RSSummary.reset_index(drop=True)
        QC_FailLogical_RSSummary  = pd.DataFrame(QC_FailLogical_RSSummary)
        
        ## Building Ref_FailedQC_InSetcatchDB_1
        ForMergeOnlyRSSummary1 = QC_FailLogical_RSSummary1.loc[:,['DeploymentUID']]
        ForMergeOnlyRSSummary1 = ForMergeOnlyRSSummary1.drop_duplicates(subset='DeploymentUID', keep="first")
        Ref_FailedQC_InSetcatchDB1 = RecordType_SetNumber_FailLogical.merge(
                                ForMergeOnlyRSSummary1, on = ["DeploymentUID"], indicator=True, 
                                how='outer').query('_merge == "both"')
        Ref_FailedQC_InSetcatchDB1 = Ref_FailedQC_InSetcatchDB1.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                                    'RecordType','DeploymentNumber','SetNumber']]
        Ref_FailedQC_InSetcatchDB1[['RecordType','DeploymentNumber','SetNumber']] = Ref_FailedQC_InSetcatchDB1[['RecordType',
                                                                                'DeploymentNumber','SetNumber']].replace([99999999], '')
        Ref_FailedQC_InSetcatchDB1['QCRecordType_SetNumber'] = 'Only One RecordType1 Allowed Per SetNumber'
        RecType_1_QCMessage = 'Only One RecordType1 Allowed Per SetNumber'
        RecType_2_QCMessage ='Only One RecordType1 Allowed Per SetNumber'
        Ref_FailedQC_InSetcatchDB1['QCRecordType_SetNumber'] = np.where(Ref_FailedQC_InSetcatchDB1['RecordType']== 1, 
                            RecType_1_QCMessage, RecType_2_QCMessage)
        Ref_FailedQC_InSetcatchDB1['QC_CaseType'] ="Case-A: Multi RecordType1 - SetNumber"
        Ref_FailedQC_InSetcatchDB1 = Ref_FailedQC_InSetcatchDB1.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                        'RecordType','DeploymentNumber','SetNumber', 
                        'QCRecordType_SetNumber', 'QC_CaseType']]
        Ref_FailedQC_InSetcatchDB1.sort_values(by=['DeploymentUID','DeploymentNumber','SetNumber','RecordType'], inplace=True)
        Ref_FailedQC_InSetcatchDB1  = Ref_FailedQC_InSetcatchDB1.reset_index(drop=True)
        Ref_FailedQC_InSetcatchDB1  = pd.DataFrame(Ref_FailedQC_InSetcatchDB1)

         ## Building Ref_FailedQC_InSetcatchDB_2
        ForMergeOnlyRSSummary2 = QC_FailLogical_RSSummary2.loc[:,['DeploymentUID']]
        ForMergeOnlyRSSummary2 = ForMergeOnlyRSSummary2.drop_duplicates(subset='DeploymentUID', keep="first")
        Ref_FailedQC_InSetcatchDB2 = RecordType_SetNumber_FailLogical.merge(
                                ForMergeOnlyRSSummary2, on = ["DeploymentUID"], indicator=True, 
                                how='outer').query('_merge == "both"')
        Ref_FailedQC_InSetcatchDB2 = Ref_FailedQC_InSetcatchDB2.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                                    'RecordType','DeploymentNumber','SetNumber']]
        Ref_FailedQC_InSetcatchDB2[['RecordType','DeploymentNumber','SetNumber']] = Ref_FailedQC_InSetcatchDB2[['RecordType',
                                                                                'DeploymentNumber','SetNumber']].replace([99999999], '')
        Ref_FailedQC_InSetcatchDB2['QCRecordType_SetNumber'] = 'Atleast One RecordType1 Must Present Per SetNumber'
        Ref_FailedQC_InSetcatchDB2['QC_CaseType'] ="Case-B: Null RecordType1 - SetNumber"
        
        Ref_FailedQC_InSetcatchDB2 = Ref_FailedQC_InSetcatchDB2.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                        'RecordType','DeploymentNumber','SetNumber', 
                        'QCRecordType_SetNumber', 'QC_CaseType']]
        Ref_FailedQC_InSetcatchDB2.sort_values(by=['DeploymentUID','DeploymentNumber','SetNumber','RecordType'], inplace=True)
        Ref_FailedQC_InSetcatchDB2  = Ref_FailedQC_InSetcatchDB2.reset_index(drop=True)
        Ref_FailedQC_InSetcatchDB2  = pd.DataFrame(Ref_FailedQC_InSetcatchDB2)

         ## Combining Ref_FailedQC_InSetcatchDB1 & Ref_FailedQC_InSetcatchDB2
        Ref_FailedQC_InSetcatchDB = pd.concat([Ref_FailedQC_InSetcatchDB1, Ref_FailedQC_InSetcatchDB2])
        Ref_FailedQC_InSetcatchDB.sort_values(by=['DeploymentUID','DeploymentNumber','SetNumber','RecordType'], inplace=True)
        Ref_FailedQC_InSetcatchDB  = Ref_FailedQC_InSetcatchDB.reset_index(drop=True)
        Ref_FailedQC_InSetcatchDB  = pd.DataFrame(Ref_FailedQC_InSetcatchDB)

        Submit_RecordType_SetNumber_DB(Ref_FailedQC_InSetcatchDB, QC_FailLogical_RSSummary)
        Length_RecordType_SetNumber_DF = (len(QC_FailLogical_RSSummary))
        return Length_RecordType_SetNumber_DF
        
    def RunLogicalFailed_RecordType_NumberSpecies():
        
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                                    'DeploymentNumber','SetNumber','RecordType',
                                                                    'NumberSpecies']]
                    SetCatchProfileDB_DF  = SetCatchProfileDB_DF.reset_index(drop=True)
                    SetCatchProfileDB_DF  = pd.DataFrame(SetCatchProfileDB_DF)
                    return SetCatchProfileDB_DF
                else:
                    messagebox.showerror('DFO-NL-ASOP Set & Catch DB Message', "Void DFO-NL-ASOP Set & Catch DB...Please Import DFO-NL-ASOP Set & Catch CSV Files")
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()
    
        def Submit_RecordType_NumberSpecies_DB(Ref_FailedQC_InSetcatchDB):
            try:
                Ref_FailedQC_InSetcatchDB = pd.DataFrame(Ref_FailedQC_InSetcatchDB)
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Logical)
                cursor = sqliteConnection.cursor()
                Ref_FailedQC_InSetcatchDB.to_sql('SetCatch_QCFailedLogical_RecordType_NumberSpecies',
                                            sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        def Submit_QC_FailLogical_RNSummary(QC_FailLogical_RNSummary):
            try:
                QC_FailLogical_RNSummary = pd.DataFrame(QC_FailLogical_RNSummary)
                
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Logical)
                cursor = sqliteConnection.cursor()
                QC_FailLogical_RNSummary.to_sql('Logical_RecordType_NumberSpecies_FailSummary',
                                            sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        ## Get Set& Catch DB profile
        SetCatchProfileDB_DF = GetSetCatchProfileDB()

        ## QC On RecordType_NumberSpecies
        RecordType_NumberSpecies_FailLogical= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'DeploymentNumber','SetNumber','RecordType',
                            'NumberSpecies']]).replace(['','None'], 99999999)
        
        RecordType_NumberSpecies_FailLogical[['DataBase_ID','RecordIdentifier',
                                        'DeploymentNumber','SetNumber','RecordType',
                                        'NumberSpecies']] = RecordType_NumberSpecies_FailLogical[
                                        ['DataBase_ID','RecordIdentifier',
                                        'DeploymentNumber','SetNumber','RecordType',
                                        'NumberSpecies']].astype(int)
        RecordType_NumberSpecies_FailLogical[['DeploymentUID']] = RecordType_NumberSpecies_FailLogical[['DeploymentUID']].astype(str)

        ## Separating RecType 1 and 2
        QC_FailLogical_RNSummary = RecordType_NumberSpecies_FailLogical.groupby(['DeploymentUID', 'SetNumber'], 
                                    as_index=False)['RecordType'].apply(lambda x: sum(np.unique(x)))
        QC_FailLogical_RNSummary.rename(columns={'DeploymentUID':'DeploymentUID',
                                                'SetNumber':'SetNumber',
                                                'RecordType': 'RecordTypeSUM'},inplace = True)
        
        ## Building QC_FailLogical_RNSummary1
        QC_FailLogical_RNSummary1 = QC_FailLogical_RNSummary[(QC_FailLogical_RNSummary.RecordTypeSUM < 2)]
        QC_FailLogical_RNSummary1 = QC_FailLogical_RNSummary1.reset_index(drop=True)
        QC_FailLogical_RNSummary1 = pd.DataFrame(QC_FailLogical_RNSummary1)
        
        ForMergeOnlyRNSummary1 = QC_FailLogical_RNSummary1.loc[:,['DeploymentUID']]
        Ref_FailedQC_InSetcatchDB1 = RecordType_NumberSpecies_FailLogical.merge(
                            ForMergeOnlyRNSummary1, on = ["DeploymentUID"], indicator=True, 
                            how='outer').query('_merge == "both"')
        Ref_FailedQC_InSetcatchDB1 = Ref_FailedQC_InSetcatchDB1.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                                    'DeploymentNumber','SetNumber', 'RecordType','NumberSpecies']]
        Ref_FailedQC_InSetcatchDB1 = Ref_FailedQC_InSetcatchDB1[(Ref_FailedQC_InSetcatchDB1.NumberSpecies != 99999999)]
        Ref_FailedQC_InSetcatchDB1 = Ref_FailedQC_InSetcatchDB1[(Ref_FailedQC_InSetcatchDB1.NumberSpecies != 0)]
        
        Ref_FailedQC_InSetcatchDB1[['DeploymentNumber','SetNumber', 
                                'RecordType','NumberSpecies']] = Ref_FailedQC_InSetcatchDB1[['DeploymentNumber',
                                                                'SetNumber', 'RecordType','NumberSpecies']].replace([99999999], '')
        Ref_FailedQC_InSetcatchDB1['QCRecordType_NumberSpecies'] ="Case-A: In A Set With Only RecType1, NumberSpecies Must 0 or Blank"
        Ref_FailedQC_InSetcatchDB1['QCCaseType'] ="Case - A"
        Ref_FailedQC_InSetcatchDB1  = Ref_FailedQC_InSetcatchDB1.reset_index(drop=True)
        Ref_FailedQC_InSetcatchDB1  = pd.DataFrame(Ref_FailedQC_InSetcatchDB1)
       
        ## Building QC_FailLogical_RNSummary2
        QC_FailLogical_RNSummary2 = QC_FailLogical_RNSummary[(QC_FailLogical_RNSummary.RecordTypeSUM == 3)]
        QC_FailLogical_RNSummary2 = QC_FailLogical_RNSummary2.reset_index(drop=True)
        QC_FailLogical_RNSummary2 = pd.DataFrame(QC_FailLogical_RNSummary2)
        
        ForMergeOnlyRNSummary2 = QC_FailLogical_RNSummary2.loc[:,['DeploymentUID']]
        Ref_FailedQC_InSetcatchDB2 = RecordType_NumberSpecies_FailLogical.merge(
                            ForMergeOnlyRNSummary2, on = ["DeploymentUID"], indicator=True, 
                            how='outer').query('_merge == "both"')
        Ref_FailedQC_InSetcatchDB2 = Ref_FailedQC_InSetcatchDB2.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                                    'DeploymentNumber','SetNumber', 'RecordType','NumberSpecies']]
        uniqueFinder= Ref_FailedQC_InSetcatchDB2.groupby(['DeploymentUID'],  
                        as_index=False)['NumberSpecies'].apply(lambda x: (np.count_nonzero(np.unique(x))))
        uniqueFinder = uniqueFinder[(uniqueFinder.NumberSpecies > 1)]
        uniqueFinder = uniqueFinder.reset_index(drop=True)
        QC_FailLogical_RNSummary2 = pd.DataFrame(uniqueFinder)
        ForMergeOnlyRNSummary2 = QC_FailLogical_RNSummary2.loc[:,['DeploymentUID']]
        Ref_FailedQC_InSetcatchDB2 = RecordType_NumberSpecies_FailLogical.merge(
                            ForMergeOnlyRNSummary2, on = ["DeploymentUID"], indicator=True, 
                            how='outer').query('_merge == "both"')
        Ref_FailedQC_InSetcatchDB2 = Ref_FailedQC_InSetcatchDB2.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                                    'DeploymentNumber','SetNumber', 'RecordType','NumberSpecies']]
        Ref_FailedQC_InSetcatchDB2[['DeploymentNumber','SetNumber', 
                                'RecordType','NumberSpecies']] = Ref_FailedQC_InSetcatchDB2[['DeploymentNumber',
                                                                'SetNumber', 'RecordType','NumberSpecies']].replace([99999999], '')
        Ref_FailedQC_InSetcatchDB2['QCRecordType_NumberSpecies'] ="Case-B: In A Set With RecType-1/2, NumberSpecies Must Same For Each RecType"
        Ref_FailedQC_InSetcatchDB2['QCCaseType'] ="Case - B"
        Ref_FailedQC_InSetcatchDB2  = Ref_FailedQC_InSetcatchDB2.reset_index(drop=True)
        Ref_FailedQC_InSetcatchDB2  = pd.DataFrame(Ref_FailedQC_InSetcatchDB2)
        
        ## Combine Ref_FailedQC_InSetcatchDB & Ref_FailedQC_InSetcatchDB2
        Ref_FailedQC_InSetcatchDB= []
        Ref_FailedQC_InSetcatchDB = pd.concat([Ref_FailedQC_InSetcatchDB1, Ref_FailedQC_InSetcatchDB2])
        Ref_FailedQC_InSetcatchDB.sort_values(by=['DeploymentNumber','SetNumber','RecordType'], inplace=True)
        Ref_FailedQC_InSetcatchDB  = Ref_FailedQC_InSetcatchDB.reset_index(drop=True)
        Ref_FailedQC_InSetcatchDB  = pd.DataFrame(Ref_FailedQC_InSetcatchDB)
        Submit_RecordType_NumberSpecies_DB(Ref_FailedQC_InSetcatchDB)

        if len(Ref_FailedQC_InSetcatchDB)>0:
            QC_FailLogical_RNSummary= Ref_FailedQC_InSetcatchDB.groupby(['QCCaseType', 'QCRecordType_NumberSpecies'],  
                            as_index=False)['DeploymentUID'].apply(lambda x: (np.count_nonzero(np.unique(x))))
            QC_FailLogical_RNSummary = QC_FailLogical_RNSummary.loc[:,
                                    ['QCCaseType', 'QCRecordType_NumberSpecies', 'DeploymentUID']]
            QC_FailLogical_RNSummary.rename(columns={'QCCaseType':'QCCaseType', 'QCRecordType_NumberSpecies':'QCRecordType_NumberSpecies',
                                                     'DeploymentUID': 'QCFailCount'},inplace = True)
            Submit_QC_FailLogical_RNSummary(QC_FailLogical_RNSummary)
            Length_FailedRN_DF = (sum(QC_FailLogical_RNSummary['QCFailCount']) )
        else:
            QC_FailLogical_RNSummary = pd.DataFrame(columns={'QCCaseType':[], 
                                                             'QCRecordType_NumberSpecies':[], 
                                                             'QCFailCount':[]})
            Submit_QC_FailLogical_RNSummary(QC_FailLogical_RNSummary)
            Length_FailedRN_DF = 0
        return Length_FailedRN_DF
    
    def RunLogicalFailed_RecType_SpecsCode_NumbSpecs():  
        
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                                    'DeploymentNumber','SetNumber','RecordType',
                                                                    'NumberSpecies', 'SpeciesCode']]
                    SetCatchProfileDB_DF  = SetCatchProfileDB_DF.reset_index(drop=True)
                    SetCatchProfileDB_DF  = pd.DataFrame(SetCatchProfileDB_DF)
                    return SetCatchProfileDB_DF
                else:
                    messagebox.showerror('DFO-NL-ASOP Set & Catch DB Message', "Void DFO-NL-ASOP Set & Catch DB...Please Import DFO-NL-ASOP Set & Catch CSV Files")
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()
  
        def Submit_RecType_SpecsCode_NumbSpecs_DB(RecTyp_SpCode_FailLogical, 
                                             Specscode_NumSpecs_FailLogical,
                                             QC_FailLogical_RT_SC_NS_Summary):
            try:
                RecTyp_SpCode_FailLogical = pd.DataFrame(RecTyp_SpCode_FailLogical)
                Specscode_NumSpecs_FailLogical = pd.DataFrame(Specscode_NumSpecs_FailLogical)
                QC_FailLogical_RT_SC_NS_Summary = pd.DataFrame(QC_FailLogical_RT_SC_NS_Summary)
                
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Logical)
                cursor = sqliteConnection.cursor()
                RecTyp_SpCode_FailLogical.to_sql('SetCatch_QCFailedLogical_RecordType_SpeciesCode',
                                            sqliteConnection, if_exists="replace", index =False)
                Specscode_NumSpecs_FailLogical.to_sql('SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode',
                                            sqliteConnection, if_exists="replace", index =False)
                QC_FailLogical_RT_SC_NS_Summary.to_sql('Logical_RecType_SpecsCode_NumbSpecs_FailSummary',
                                            sqliteConnection, if_exists="replace", index =False)
            
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()
        
        ## Get Set& Catch DB profile
        SetCatchProfileDB_DF = GetSetCatchProfileDB()

        ## QC On RecordType_SpeciesCode
        RecTyp_SpCode_FailLogical= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'DeploymentNumber','SetNumber','RecordType',
                            'NumberSpecies', 'SpeciesCode']]).replace(['','None'], 99999999)
        RecTyp_SpCode_FailLogical[['DataBase_ID','RecordIdentifier',
                                'DeploymentNumber','SetNumber','RecordType',
                                'NumberSpecies', 'SpeciesCode']] = RecTyp_SpCode_FailLogical[
                                ['DataBase_ID','RecordIdentifier',
                                'DeploymentNumber','SetNumber','RecordType',
                                'NumberSpecies', 'SpeciesCode']].astype(int)
        RecTyp_SpCode_FailLogical[['DeploymentUID']] = RecTyp_SpCode_FailLogical[['DeploymentUID']].astype(str)
        
        ## Case-A Filter 
        FilteredRecTyp_SpCode_FailLogical1 = RecTyp_SpCode_FailLogical[(RecTyp_SpCode_FailLogical.RecordType == 1)&
                                            (RecTyp_SpCode_FailLogical.SpeciesCode != 99999999)]
        FilteredRecTyp_SpCode_FailLogical1 = FilteredRecTyp_SpCode_FailLogical1.loc[:,
                                                ['DeploymentUID']]
        FilteredRecTyp_SpCode_FailLogical1['QCCaseType'] ="Case - A"
        FilteredRecTyp_SpCode_FailLogical1  = FilteredRecTyp_SpCode_FailLogical1.reset_index(drop=True)
        FilteredRecTyp_SpCode_FailLogical1  = pd.DataFrame(FilteredRecTyp_SpCode_FailLogical1)

        ## Case-B Filter 2 : Rectyp1
        FilSpecscode_NumSpecs_FailLogical2 = RecTyp_SpCode_FailLogical[
                    ((RecTyp_SpCode_FailLogical.RecordType == 1))|(
                    (RecTyp_SpCode_FailLogical.RecordType == 2)&
                    (RecTyp_SpCode_FailLogical.SpeciesCode != 99999999))] 
        FilSpecscode_NumSpecs_FailLogical2 = FilSpecscode_NumSpecs_FailLogical2.groupby([
                'DeploymentUID', 'RecordType','NumberSpecies'], 
                as_index=False)['SpeciesCode'].apply(lambda x: (np.count_nonzero((x))))
        FilSpecscode_NumSpecs_FailLogical2.rename(columns={'DeploymentUID':'DeploymentUID',
                                                        'RecordType':'RecordType',
                                                        'NumberSpecies':'NumberSpecies',
                                                        'SpeciesCode': 'CountSumSpeciesCode'
                                                        },inplace = True)
        ## Building Rec1_FilSpecscode_NumSpecs_FailLogical2
        Rec1_FilSpecscode_NumSpecs_FailLogical2 = FilSpecscode_NumSpecs_FailLogical2[
                        (FilSpecscode_NumSpecs_FailLogical2.RecordType == 1)]
        Rec1_FilSpecscode_NumSpecs_FailLogical2  = Rec1_FilSpecscode_NumSpecs_FailLogical2.reset_index(drop=True)
        Rec1_FilSpecscode_NumSpecs_FailLogical2  = pd.DataFrame(Rec1_FilSpecscode_NumSpecs_FailLogical2)
        
         ## Building Rec2_FilSpecscode_NumSpecs_FailLogical2
        Rec2_FilSpecscode_NumSpecs_FailLogical2 = FilSpecscode_NumSpecs_FailLogical2[
                        (FilSpecscode_NumSpecs_FailLogical2.RecordType == 2)]
        Rec2_FilSpecscode_NumSpecs_FailLogical2 = Rec2_FilSpecscode_NumSpecs_FailLogical2.groupby([
                'DeploymentUID', 'RecordType'], 
                as_index=False)['CountSumSpeciesCode'].apply(lambda x: (np.sum((x))))
        Rec2_FilSpecscode_NumSpecs_FailLogical2  = Rec2_FilSpecscode_NumSpecs_FailLogical2.reset_index(drop=True)
        Rec2_FilSpecscode_NumSpecs_FailLogical2  = pd.DataFrame(Rec2_FilSpecscode_NumSpecs_FailLogical2)
        
            ## Combining Rec1_FilSpecscode_NumSpecs_FailLogical2 With Rec2_FilSpecscode_NumSpecs_FailLogical2
        Combine_Rec_1_2 = Rec1_FilSpecscode_NumSpecs_FailLogical2.merge(
                        Rec2_FilSpecscode_NumSpecs_FailLogical2, 
                        on = ["DeploymentUID"], indicator=True, 
                        how='outer').query('_merge == "both"')
        Combine_Rec_1_2 = Combine_Rec_1_2.loc[:,
                                            ['DeploymentUID','RecordType_x', 'NumberSpecies',
                                            'CountSumSpeciesCode_y']]
        Combine_Rec_1_2 = Combine_Rec_1_2[
                (Combine_Rec_1_2.NumberSpecies != Combine_Rec_1_2.CountSumSpeciesCode_y)]
        Combine_Rec_1_2 = Combine_Rec_1_2.loc[:,
                                            ['DeploymentUID']]
        Combine_Rec_1_2 = Combine_Rec_1_2.drop_duplicates(subset='DeploymentUID', keep="first")
        Combine_Rec_1_2  = Combine_Rec_1_2.reset_index(drop=True)
        FilteredRecTyp_SpCode_FailLogical2  = pd.DataFrame(Combine_Rec_1_2)
        FilteredRecTyp_SpCode_FailLogical2['QCCaseType'] ="Case - B"
        FilteredRecTyp_SpCode_FailLogical2  = FilteredRecTyp_SpCode_FailLogical2.reset_index(drop=True)
        FilteredRecTyp_SpCode_FailLogical2  = pd.DataFrame(FilteredRecTyp_SpCode_FailLogical2)

        ## Merging RecTyp_SpCode_FailLogical With FilteredRecTyp_SpCode_FailLogical
        FilteredRecTyp_SpCode_FailLogical1  = FilteredRecTyp_SpCode_FailLogical1.reset_index(drop=True)
        FilteredRecTyp_SpCode_FailLogical  = pd.DataFrame(FilteredRecTyp_SpCode_FailLogical1)
        RecTyp_SpCode_FailLogical = RecTyp_SpCode_FailLogical.merge(
                                    FilteredRecTyp_SpCode_FailLogical, on = ["DeploymentUID"], indicator=True, 
                                    how='outer').query('_merge == "both"')
        RecTyp_SpCode_FailLogical = RecTyp_SpCode_FailLogical.loc[:,
                                    ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                    'DeploymentNumber','SetNumber','RecordType',
                                    'NumberSpecies', 'SpeciesCode', 'QCCaseType']]
        RecTyp_SpCode_FailLogical[['DataBase_ID','RecordIdentifier','DeploymentUID',
                                    'DeploymentNumber','SetNumber','RecordType',
                                    'NumberSpecies', 'SpeciesCode']] = \
        RecTyp_SpCode_FailLogical[['DataBase_ID','RecordIdentifier','DeploymentUID',
                                    'DeploymentNumber','SetNumber','RecordType',
                                    'NumberSpecies', 'SpeciesCode']].replace([99999999, '99999999'], '')
        RecTyp_SpCode_FailLogical  = RecTyp_SpCode_FailLogical.reset_index(drop=True)
        RecTyp_SpCode_FailLogical  = pd.DataFrame(RecTyp_SpCode_FailLogical)

        ## QC On CountSumSpeciesCode_NumberSpecies
        Specscode_NumSpecs_FailLogical= (SetCatchProfileDB_DF.loc[:,
                                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                        'DeploymentNumber','SetNumber','RecordType',
                                        'NumberSpecies', 'SpeciesCode']]).replace(['','None'], 99999999)
        
        Specscode_NumSpecs_FailLogical[['DataBase_ID','RecordIdentifier',
                                        'DeploymentNumber','SetNumber','RecordType',
                                        'NumberSpecies', 'SpeciesCode']] = Specscode_NumSpecs_FailLogical[
                                        ['DataBase_ID','RecordIdentifier',
                                        'DeploymentNumber','SetNumber','RecordType',
                                        'NumberSpecies', 'SpeciesCode']].astype(int)
        Specscode_NumSpecs_FailLogical[['DeploymentUID']] \
                                = Specscode_NumSpecs_FailLogical[['DeploymentUID']].astype(str)
        FilSpecscode_NumSpecs_FailLogical = Specscode_NumSpecs_FailLogical[
                                            (Specscode_NumSpecs_FailLogical.RecordType == 2)&
                                            (Specscode_NumSpecs_FailLogical.SpeciesCode != 99999999)]
        
        FilSpecscode_NumSpecs_FailLogical   = FilSpecscode_NumSpecs_FailLogical.groupby(['DeploymentUID', 'NumberSpecies'], 
                                        as_index=False)['SpeciesCode'].apply(lambda x: (np.count_nonzero((x))))
        FilSpecscode_NumSpecs_FailLogical.rename(columns={'DeploymentUID':'DeploymentUID',
                                                    'NumberSpecies':'NumberSpecies',
                                                    'SpeciesCode': 'CountSumSpeciesCode'
                                                    },inplace = True)
        FilSpecscode_NumSpecs_FailLogical = FilSpecscode_NumSpecs_FailLogical[
                (FilSpecscode_NumSpecs_FailLogical.NumberSpecies != FilSpecscode_NumSpecs_FailLogical.CountSumSpeciesCode)]
        FilSpecscode_NumSpecs_FailLogical = FilSpecscode_NumSpecs_FailLogical.loc[:,
                                            ['DeploymentUID']]
        FilSpecscode_NumSpecs_FailLogical = FilSpecscode_NumSpecs_FailLogical.drop_duplicates(subset='DeploymentUID', keep="first")
        FilSpecscode_NumSpecs_FailLogical['QCCaseType'] ="Case - B"
        FilSpecscode_NumSpecs_FailLogical  = FilSpecscode_NumSpecs_FailLogical.reset_index(drop=True)
        FilSpecscode_NumSpecs_FailLogical  = pd.DataFrame(FilSpecscode_NumSpecs_FailLogical)

        FilSpecscode_NumSpecs_FailLogical = pd.concat([FilSpecscode_NumSpecs_FailLogical, FilteredRecTyp_SpCode_FailLogical2])
        FilSpecscode_NumSpecs_FailLogical = FilSpecscode_NumSpecs_FailLogical.drop_duplicates(subset='DeploymentUID', keep="first")
        FilSpecscode_NumSpecs_FailLogical  = FilSpecscode_NumSpecs_FailLogical.reset_index(drop=True)
        FilSpecscode_NumSpecs_FailLogical  = pd.DataFrame(FilSpecscode_NumSpecs_FailLogical)
        
        Specscode_NumSpecs_FailLogical = Specscode_NumSpecs_FailLogical.merge(
                                        FilSpecscode_NumSpecs_FailLogical, 
                                        on = ["DeploymentUID"], indicator=True, 
                                        how='outer').query('_merge == "both"')
        Specscode_NumSpecs_FailLogical = Specscode_NumSpecs_FailLogical.loc[:,
                                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                        'DeploymentNumber','SetNumber','RecordType',
                                        'NumberSpecies', 'SpeciesCode', 'QCCaseType']]
        Specscode_NumSpecs_FailLogical[['DataBase_ID','RecordIdentifier','DeploymentUID',
                                        'DeploymentNumber','SetNumber','RecordType',
                                        'NumberSpecies', 'SpeciesCode']] = \
        Specscode_NumSpecs_FailLogical[['DataBase_ID','RecordIdentifier','DeploymentUID',
                                        'DeploymentNumber','SetNumber','RecordType',
                                        'NumberSpecies', 'SpeciesCode']].replace([99999999, 
                                        '99999999'], '')
        Specscode_NumSpecs_FailLogical  = Specscode_NumSpecs_FailLogical.reset_index(drop=True)
        Specscode_NumSpecs_FailLogical  = pd.DataFrame(Specscode_NumSpecs_FailLogical)
        
        ## Combine RecTyp_SpCode_FailLogical & Specscode_NumSpecs_FailLogical
        Ref_FailedQC_InSetcatchDB= []
        Ref_FailedQC_InSetcatchDB = pd.concat([RecTyp_SpCode_FailLogical, Specscode_NumSpecs_FailLogical])
        if len(Ref_FailedQC_InSetcatchDB)>0:
            QC_FailLogical_RT_SC_NS_Summary= Ref_FailedQC_InSetcatchDB.groupby(['QCCaseType'],  
                            as_index=False)['DeploymentUID'].apply(lambda x: (np.count_nonzero(np.unique(x))))
            QC_FailLogical_RT_SC_NS_Summary = QC_FailLogical_RT_SC_NS_Summary.loc[:,
                                            ['QCCaseType', 'DeploymentUID']]
            QC_FailLogical_RT_SC_NS_Summary.rename(columns={'QCCaseType':'QCCaseType',
                                                            'DeploymentUID': 'QCFailCount'
                                                            },inplace = True)
            QC_FailLogical_RT_SC_NS_Summary  = QC_FailLogical_RT_SC_NS_Summary.reset_index(drop=True)
            QC_FailLogical_RT_SC_NS_Summary  = pd.DataFrame(QC_FailLogical_RT_SC_NS_Summary)
            Submit_RecType_SpecsCode_NumbSpecs_DB(RecTyp_SpCode_FailLogical, 
                                              Specscode_NumSpecs_FailLogical,
                                              QC_FailLogical_RT_SC_NS_Summary)
            Length_RT_SC_NS_Summary  = (sum(QC_FailLogical_RT_SC_NS_Summary['QCFailCount']))
        else:
            QC_FailLogical_RT_SC_NS_Summary = pd.DataFrame(columns={'QCCaseType':[], 
                                                             'QCFailCount':[]})
            Submit_RecType_SpecsCode_NumbSpecs_DB(RecTyp_SpCode_FailLogical, 
                                              Specscode_NumSpecs_FailLogical,
                                              QC_FailLogical_RT_SC_NS_Summary)
            Length_RT_SC_NS_Summary = 0
        
        return Length_RT_SC_NS_Summary

    def RunLogicalFailed_RecType1_DKWeight_NumIndv():  
        
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                                    'DeploymentNumber','SetNumber','RecordType',
                                                                    'NumberSpecies', 'SpeciesCode','KeptWeight',
                                                                    'DiscardWeight','NumberIndividuals']]
                    SetCatchProfileDB_DF  = SetCatchProfileDB_DF.reset_index(drop=True)
                    SetCatchProfileDB_DF  = pd.DataFrame(SetCatchProfileDB_DF)
                    return SetCatchProfileDB_DF
                else:
                    messagebox.showerror('DFO-NL-ASOP Set & Catch DB Message', "Void DFO-NL-ASOP Set & Catch DB...Please Import DFO-NL-ASOP Set & Catch CSV Files")
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()
  
        def Submit_RecType1_DKWeight_NumIndv_DB(RecType1_DKWeight_NumIndv_FailLogical):
            try:
                RecType1_DKWeight_NumIndv_FailLogical = pd.DataFrame(RecType1_DKWeight_NumIndv_FailLogical)

                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Logical)
                cursor = sqliteConnection.cursor()
                RecType1_DKWeight_NumIndv_FailLogical.to_sql('SetCatch_QCFailedLogical_RecType_KW_DW_NI',
                                            sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()
        
        ## Get Set& Catch DB profile
        SetCatchProfileDB_DF = GetSetCatchProfileDB()

        ## QC On RecordType_SpeciesCode
        RecType1_DKWeight_NumIndv_FailLogical= (SetCatchProfileDB_DF.loc[:,
                    ['DataBase_ID','RecordIdentifier','DeploymentUID',
                    'DeploymentNumber','SetNumber','RecordType',
                    'NumberSpecies', 'SpeciesCode', 'KeptWeight',
                    'DiscardWeight','NumberIndividuals']]).replace(['','None'], 99999999)
        RecType1_DKWeight_NumIndv_FailLogical[['DataBase_ID','RecordIdentifier',
                    'DeploymentNumber','SetNumber','RecordType',
                    'NumberSpecies', 'SpeciesCode',
                    'KeptWeight','DiscardWeight','NumberIndividuals']] = RecType1_DKWeight_NumIndv_FailLogical[
                    ['DataBase_ID','RecordIdentifier',
                    'DeploymentNumber','SetNumber','RecordType',
                    'NumberSpecies', 'SpeciesCode',
                    'KeptWeight','DiscardWeight','NumberIndividuals']].astype(int)
        RecType1_DKWeight_NumIndv_FailLogical[['DeploymentUID']] = RecType1_DKWeight_NumIndv_FailLogical[
                    ['DeploymentUID']].astype(str)
        RecType1_DKWeight_NumIndv_FailLogical = RecType1_DKWeight_NumIndv_FailLogical[
            (RecType1_DKWeight_NumIndv_FailLogical.RecordType == 1)]
        RecType1_DKWeight_NumIndv_FailLogical  = RecType1_DKWeight_NumIndv_FailLogical.reset_index(drop=True)
        RecType1_DKWeight_NumIndv_FailLogical  = pd.DataFrame(RecType1_DKWeight_NumIndv_FailLogical)
         
         ## Filter For ReccordType 1 KeptWeight, DiscardWeight,  NumberIndividuals Must be Blank
        FilterRecType1_DKWeight_NumIndv_FailLogical1 = RecType1_DKWeight_NumIndv_FailLogical[
            (RecType1_DKWeight_NumIndv_FailLogical.KeptWeight != 99999999)|
            (RecType1_DKWeight_NumIndv_FailLogical.DiscardWeight != 99999999)|
            (RecType1_DKWeight_NumIndv_FailLogical.NumberIndividuals != 99999999)
            ]
        FilterRecType1_DKWeight_NumIndv_FailLogical1 = FilterRecType1_DKWeight_NumIndv_FailLogical1.loc[
            :,['DeploymentUID']]
        FilterRecType1_DKWeight_NumIndv_FailLogical1['QCMessage'] ="For ReccordType 1 KeptWeight, DiscardWeight,  NumberIndividuals Must be Blank"
        FilterRecType1_DKWeight_NumIndv_FailLogical1  = FilterRecType1_DKWeight_NumIndv_FailLogical1.reset_index(drop=True)
        FilterRecType1_DKWeight_NumIndv_FailLogical1  = pd.DataFrame(FilterRecType1_DKWeight_NumIndv_FailLogical1)

        ## Merging
        RecType1_DKWeight_NumIndv_FailLogical = RecType1_DKWeight_NumIndv_FailLogical.merge(
                                    FilterRecType1_DKWeight_NumIndv_FailLogical1, on = ["DeploymentUID"], indicator=True, 
                                    how='outer').query('_merge == "both"')
        RecType1_DKWeight_NumIndv_FailLogical = RecType1_DKWeight_NumIndv_FailLogical.loc[:,
                    ['DataBase_ID','RecordIdentifier','DeploymentUID',
                    'DeploymentNumber','SetNumber','RecordType',
                    'NumberSpecies', 'SpeciesCode','KeptWeight',
                    'DiscardWeight','NumberIndividuals', 'QCMessage']]
        RecType1_DKWeight_NumIndv_FailLogical[['DataBase_ID','RecordIdentifier',
                    'DeploymentNumber','SetNumber','RecordType',
                    'NumberSpecies', 'SpeciesCode',
                    'KeptWeight','DiscardWeight','NumberIndividuals']] = \
        RecType1_DKWeight_NumIndv_FailLogical[['DataBase_ID','RecordIdentifier',
                    'DeploymentNumber','SetNumber','RecordType',
                    'NumberSpecies', 'SpeciesCode',
                    'KeptWeight','DiscardWeight','NumberIndividuals']].replace([99999999, '99999999'], '')
        RecType1_DKWeight_NumIndv_FailLogical  = RecType1_DKWeight_NumIndv_FailLogical.reset_index(drop=True)
        RecType1_DKWeight_NumIndv_FailLogical  = pd.DataFrame(RecType1_DKWeight_NumIndv_FailLogical)
        Submit_RecType1_DKWeight_NumIndv_DB(RecType1_DKWeight_NumIndv_FailLogical)
        Length_QC_Fail  = len(RecType1_DKWeight_NumIndv_FailLogical)
        return Length_QC_Fail
    
    ### Run Logical QC Type 1. RunLogicalFailed_CatchVariables
    RunLogicalFailed_Catch = RunLogicalFailed_CatchVariables()
    ### Run Logical QC Type 2. RunLogicalFailed_RecordType_SetNumber
    RunLogicalFailed_RS = RunLogicalFailed_RecordType_SetNumber()
    ### Run Logical QC Type 3. RunLogicalFailed_RecordType_NumberSpecies
    RunLogicalFailed_RN = RunLogicalFailed_RecordType_NumberSpecies()
    ### Run Logical QC Type 4. RunLogicalFailed_RecType_SpecsCode_NumbSpecs
    RunLogicalFailed_RT_NS_SpCode = RunLogicalFailed_RecType_SpecsCode_NumbSpecs()
    ### Run Logical QC Type 5. RunLogicalFailed_RecType1_DKWeight_NumIndv
    RunLogicalFailed_RT_DKW_NI = RunLogicalFailed_RecType1_DKWeight_NumIndv()
    
    TotalFailedQC_LogicalValidation = (int(RunLogicalFailed_Catch)+\
                                       int(RunLogicalFailed_RS) +\
                                       int(RunLogicalFailed_RN) +\
                                       int(RunLogicalFailed_RT_NS_SpCode)+\
                                       int(RunLogicalFailed_RT_DKW_NI)
                                       )
    return TotalFailedQC_LogicalValidation
