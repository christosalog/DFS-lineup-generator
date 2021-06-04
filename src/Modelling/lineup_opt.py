import pandas as pd
import numpy as np
import pickle
'''Lineup Optimization'''
import pulp
import cplex
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


def fill_position(pos, player_pos_list):
    if pos == 'PG':
        pg = [pp for pp in player_pos_list if pp[1]=='PG']
        pgsg = [pp for pp in player_pos_list if 'PG' in pp[1]]
        if len(pg) > 0:
            player = pg[0][0]
            player_pos_list.remove(pg[0])
            return player, player_pos_list
        elif len(pgsg) > 0:
            player = pgsg[0][0]
            player_pos_list.remove(pgsg[0])
            return player, player_pos_list
    elif pos == 'SG':
        sg = [pp for pp in player_pos_list if pp[1]=='SG']
        pgsg = [pp for pp in player_pos_list if 'SG' in pp[1]]
        if len(sg) > 0:
            player = sg[0][0]
            player_pos_list.remove(sg[0])
            return player, player_pos_list
        elif len(pgsg) > 0:
            player = pgsg[0][0]
            player_pos_list.remove(pgsg[0])
            return player, player_pos_list
    elif pos == 'SF':
        sf = [pp for pp in player_pos_list if pp[1]=='SF']
        sfpf = [pp for pp in player_pos_list if 'SF' in pp[1]]
        if len(sf) > 0:
            player = sf[0][0]
            player_pos_list.remove(sf[0])
            return player, player_pos_list
        elif len(sfpf) > 0:
            player = sfpf[0][0]
            player_pos_list.remove(sfpf[0])
            return player, player_pos_list
    elif pos == 'PF':
        pf = [pp for pp in player_pos_list if pp[1]=='PF']
        sfpf = [pp for pp in player_pos_list if 'PF' in pp[1]]
        if len(pf) > 0:
            player = pf[0][0]
            player_pos_list.remove(pf[0])
            return player, player_pos_list
        elif len(sfpf) > 0:
            player = sfpf[0][0]
            player_pos_list.remove(sfpf[0])
            return player, player_pos_list
    elif pos == 'C':
        center = [pp for pp in player_pos_list if pp[1]=='C']
        pfc = [pp for pp in player_pos_list if 'C' in pp[1]]
        if len(center) > 0:
            player = center[0][0]
            player_pos_list.remove(center[0])
            return player, player_pos_list
        elif len(pfc) > 0:
            player = pfc[0][0]
            player_pos_list.remove(pfc[0])
            return player, player_pos_list
    elif pos == 'G':
        guard = [pp for pp in player_pos_list if 'G' in pp[1]]
        player = guard[0][0]
        player_pos_list.remove(guard[0])
        return player, player_pos_list
    elif pos == 'F':
        forward = [pp for pp in player_pos_list if 'F' in pp[1]]
        player = forward[0][0]
        player_pos_list.remove(forward[0])
        return player, player_pos_list
    elif pos == 'UTIL':
        player = player_pos_list[0][0]
        player_pos_list.pop()
        return player, player_pos_list

def optimize_dk_lineup(day_df):
    df_today = day_df.copy()
    df_today.reset_index(drop = True, inplace = True)

    #requirements
    salary_cap = 50000
    num_players = len(df_today.index)
    positions = {'PG': [], 'SG': [], 'SF': [], 'PF': [], 'C': []}

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

    ind_list = []
    for x, y in enumerate(lineup_copy):
        if y == 1:
            ind_list.append(x)

    players = [df_today.loc[i, 'Name'] for i in ind_list]
    positions = [df_today.loc[i, 'Pos'] for i in ind_list]
    fpts = [df_today.loc[i, 'FPTS'] for i in ind_list]
    total_predicted_fpts = sum(fpts)

    player_positions_list = [(player, pos) for player, pos in zip(players, positions)]

    lineup_dict = {'PG': '',
                   'SG': '',
                   'SF': '',
                   'PF': '',
                   'C': '',
                   'G': '',
                   'F': '',
                   'UTIL': ''
                   }
    lineup_slots = ['PG', 'SG', 'SF', 'PF', 'C', 'G', 'F', 'UTIL']
    player_pos = player_positions_list.copy()
    for position in lineup_slots:
        player, player_pos = fill_position(position, player_pos)
        lineup_dict[position] = player

    return lineup_dict, total_predicted_fpts

