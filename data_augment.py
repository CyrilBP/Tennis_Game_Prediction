# -*- coding: utf-8 -*-
"""
Created on Sat May 23 12:57:47 2020

@author: Cyril Bosse-Platiere
"""
import pandas as pd
import numpy as np
from datetime import datetime,timedelta

def Momentum(data, indices, days1, days2):
    
    exiting_columns = list(data.columns)
    
    data[["Player1", "Player2"]] = data.loc[:,["Winner", "Loser"]]
    data = pd.concat([data, pd.DataFrame( {'pc_win1':[0.5] * data.shape[0], 'pc_win2':[0.5] * data.shape[0], 
                   'Duel1':[0.5] * data.shape[0], 'Duel2':[0.5] * data.shape[0]})], axis = 1)
    
    data = data.loc[:,["Player1", "Player2","pc_win1", "pc_win2", "Duel1", "Duel2" ] +  exiting_columns]
    
    for i, match_index in enumerate(indices):
        if i%500 == 0:
            print(i)
        match = data.iloc[match_index,:]
        past_matches = data[(data.Date<match.Date)&(data.Date>=match.Date-timedelta(days=days1))]
        match_features_outcome_1=Player_Momentum(1,match,past_matches)
        match_features_outcome_2=Player_Momentum(2,match,past_matches)
        past_matches = data[(data.Date<match.Date)&(data.Date>=match.Date-timedelta(days=days2))]
        face_to_face_1 = FacetoFace(1, match, past_matches)
        
        data.loc[match_index,["pc_win1", "pc_win2", "Duel1", "Duel2"]] = [match_features_outcome_1,
                match_features_outcome_2, face_to_face_1, 1-face_to_face_1]
         
    return data
    

def Player_Momentum(k, match, past_matches):
    player = match.Winner if k==1 else match.Loser
    ##### Last matches
    wins=past_matches[past_matches.Winner==player]    
    losses=past_matches[past_matches.Loser==player]
    
    denom = wins.shape[0] + losses.shape[0]
    pc_win = wins.shape[0] / denom if denom > 0 else 0.5
    
    return pc_win

def FacetoFace(outcome, match, past_matches):
    player1=match.Winner if outcome==1 else match.Loser
    player2=match.Loser if outcome==1 else match.Winner
    
    duel1 = [(past_matches.Winner==player1) & (past_matches.Loser==player2)]
    duel2 = [(past_matches.Winner==player2) & (past_matches.Loser==player1)]
    
    denom = np.sum(duel1) + np.sum(duel2)
    duel = np.sum(duel1) / denom if denom >0 else 0.5 
    
    return duel
