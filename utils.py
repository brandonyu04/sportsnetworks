import numpy as np

team_list=['Arsenal', 'B\'mouth', 'Burnley', 'C. Palace', 'Chelsea', 'Everton', \
          'Hull City', 'Leicester', 'Liverpool', 'M\'brough', 'Man City', 'Man Utd', \
          'S\'hampton', 'Spurs', 'Stoke', 'Sunderland', 'Swansea', 'Watford', 'WBA', 'West Ham']
team_alias=['Arsenal', 'B-mouth', 'Burnley', 'Cpalace', 'Chelsea', 'Everton', \
          'Hull-City', 'Leicester', 'Liverpool', 'M-brough', 'Man-City', 'Man-Utd', \
          'S-Hampton', 'Spurs', 'Stoke', 'Sunderland', 'Swansea', 'Watford', 'Wba', 'West-Ham']
def import_data(folder_path, team_list):
	#the output is a list of tuples containing match stats
    file_list = os.listdir(folder_path)
    match_list = []
    return_list = []
    for team_name in team_list:
        matches = [matches for matches in file_list if matches.startswith('epl_'+team_name)]
        for match in matches:
            passer = list()
            with open(folder_path+match, 'r') as f:
                match_name = match.split('_')[2]
                match_date = match.split('_')[3]
                content = f.readlines()
                player_numbers = len(content)
                passing_pattern = np.zeros((player_numbers,), dtype=np.int)
                for line in content:
                    line_split = line.split(',')
                    player_name = line_split[0].replace('"', '')
                    passer.extend([player_name])
                    passing_data = np.array(line_split[1:player_numbers+1]).astype(np.int16)
                    passing_pattern = np.vstack((passing_pattern,passing_data))
                passing_pattern = np.delete(passing_pattern, 0, 0)
                match_tuple = {'team_name': team_name,\
                               'match_name': match_name,\
                               'match_date': match_date,\
                               'players': passer,\
                               'passing_pattern': passing_pattern
                              }
                match_list.append(match_tuple)
    return match_list
def comp_passing_strength(match_list, T=45):
	#commpute stats and add as items in the tuples
    player_list = []
    for i in range(len(match_list)):
        match = match_list[i]
        player_num = len(match['players'])
        match['total_pass'] = np.sum(np.sum(match['passing_pattern']))
        match['out_strength'] = np.sum(match['passing_pattern'],axis=1)
        match['in_strength'] = np.sum(match['passing_pattern'],axis=0)
        match['intensity'] = np.sum(match['out_strength']+match['in_strength']).astype(np.float)/(2*T)
        max_interaction = np.max(np.max(match['passing_pattern']))
        match['weight_centralization'] = np.sum(np.sum(max_interaction-match['passing_pattern']))/\
                                                        ((player_num**2-player_num-1)*match['intensity']*T)
        match['out_strength_centralization'] = np.sum(np.max(match['out_strength'])-\
                                                      match['out_strength']).astype(np.float)\
                                                        /((player_num-1)*np.sum(match['out_strength']+\
                                                        match['in_strength']).astype(np.float))
        match['in_strength_centralization'] = np.sum(np.max(match['in_strength'])-\
                                                      match['in_strength']).astype(np.float)\
                                                        /((player_num-1)*np.sum(match['out_strength']+\
                                                        match['in_strength']).astype(np.float))            
        
    return match_list