import pandas as pd
import numpy as np
import pickle
'''Lineup Optimization'''
import pulp
import cplex
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


def optimize_dk_lineup(day_df):
    df_today = day_df.copy()
    df_today.reset_index(drop = True, inplace = True)

    #requirements
    salary_cap = 50000
    num_players = len(df_today.index)
    positions = {'PG':[], 'SG':[], 'SF':[], 'PF':[], 'C':[]}

    '''add players into positions (STEP DEPENDENT ON df_today)'''
    ''' Note: players with multiple positions might appear more than once - may need a constraint for that'''
    for pos in df_today.loc[:, 'Pos']:
        for key in positions:
            positions[key].append(1 if key in pos else 0)

    #define the pulp object problem
    prob = pulp.LpProblem('NBA',pulp.LpMaximize)

    #define the players variable
    players_lineup = [pulp.LpVariable("player_{}".format(i+1), cat='Binary') for i in range(num_players)]

    #positional constraints
    prob += (1 <= pulp.lpSum(positions['PG'][i]*players_lineup[i] for i in range(num_players)) <=3)
    prob += (1 <= pulp.lpSum(positions['SG'][i]*players_lineup[i] for i in range(num_players)) <=3)
    prob += (1 <= pulp.lpSum(positions['SF'][i]*players_lineup[i] for i in range(num_players)) <=3)
    prob += (1 <= pulp.lpSum(positions['PF'][i]*players_lineup[i] for i in range(num_players)) <=3)
    prob += (1 <= pulp.lpSum(positions['C'][i]*players_lineup[i] for i in range(num_players)) <=2)

    #max players constraint
    prob += (pulp.lpSum(players_lineup[i] for i in range(num_players)) == 8)

    #add salary constraint
    prob += ((pulp.lpSum(df_today.loc[i, 'Salary']*players_lineup[i] for i in range(num_players))) <= salary_cap)

    #add constraint to avoid selecting more than one player
    #prob += (pulp.lpSum( == 1)

    #add the objective
    prob += pulp.lpSum(pulp.lpSum(df_today.loc[i, 'FPTS']*players_lineup[i] for i in range(num_players)))

    #solve the problem
    solver = pulp.CPLEX_PY(msg=0)
    status = prob.solve(solver)

    # Puts the output of one lineup into a format that will be used later
    lineup_copy = []
    for i in range(num_players):
        if players_lineup[i].varValue >= 0.9 and players_lineup[i].varValue <= 1.1:
            lineup_copy.append(1)
        else:
            lineup_copy.append(0)

    filled_lineups = []
    for lineup in [lineup_copy]:
        a_lineup = ["", "", "", "", "", "", "", ""]

        # players_lineup = lineup_copy[num_players]
        total_proj = 0
        # if actuals:
        #     total_actual = 0
        for num, player in enumerate(lineup_copy):
            if player > 0.9 and player < 1.1:
                if positions['PG'][num] == 1:
                    if a_lineup[0] == "":
                        a_lineup[0] = df_today.loc[num, 'Name']
                    elif a_lineup[5] == "":
                        a_lineup[5] = df_today.loc[num, 'Name']
                    elif a_lineup[7] == "":
                        a_lineup[7] = df_today.loc[num, 'Name']
                elif positions['SG'][num] == 1:
                    if a_lineup[1] == "":
                        a_lineup[1] = df_today.loc[num, 'Name']
                    elif a_lineup[5] == "":
                        a_lineup[5] = df_today.loc[num, 'Name']
                    elif a_lineup[7] == "":
                        a_lineup[7] = df_today.loc[num, 'Name']
                elif positions['SF'][num] == 1:
                    if a_lineup[2] == "":
                        a_lineup[2] = df_today.loc[num, 'Name']
                    elif a_lineup[6] == "":
                        a_lineup[6] = df_today.loc[num, 'Name']
                    elif a_lineup[7] == "":
                        a_lineup[7] = df_today.loc[num, 'Name']
                elif positions['PF'][num] == 1:
                    if a_lineup[3] == "":
                        a_lineup[3] = df_today.loc[num, 'Name']
                    elif a_lineup[6] == "":
                        a_lineup[6] = df_today.loc[num, 'Name']
                    elif a_lineup[7] == "":
                        a_lineup[7] = df_today.loc[num, 'Name']
                elif positions['C'][num] == 1:
                    if a_lineup[4] == "":
                        a_lineup[4] = df_today.loc[num, 'Name']
                    elif a_lineup[7] == "":
                        a_lineup[7] = df_today.loc[num, 'Name']
                total_proj += df_today.loc[num, 'FPTS']
                # if actuals:
                #     total_actual += skaters_df.loc[num, 'actual']
        a_lineup.append(round(total_proj, 2))
        # if actuals:
        #     a_lineup.append(round(total_actual, 2))
        filled_lineups.append(a_lineup)

        return filled_lineups

