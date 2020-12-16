import ssl
import string
from nltk.corpus import stopwords
import google_search
import wikipedia_search
import word_eliminator
import datamuse

SOLUTION = {
    "date": "Thursday, November 5, 2020", 
    "grid": [   [1, 1, 0, 0, 0], 
                [0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0], 
                [0, 0, 0, 1, 1] ], 
    "grid_numbers": [   [0, 0, "1", "2", "3"], 
                        ["4", "5", 0, 0, 0], 
                        ["6", 0, 0, 0, 0], 
                        ["7", 0, 0, 0, 0], 
                        ["8", 0, 0, 0, 0]  ], 
    "answer": [ [" ", " ", "T", "A", "B"], 
                ["S", "M", "I", "L", "E"], 
                ["K", "A", "P", "P", "A"], 
                ["I", "T", "S", "O", "N"], 
                ["S", "H", "Y", " ", " "]], 
    "across": [ ["1", "Running total at a bar"], 
                ["4", "Photographer's request"],
                ["6", "Greek \"K\""], 
                ["7", "\"Oh, you wanna go? Let's go!\""], 
                ["8", "Bashful"]], 
    "down": [   ["1", "A little drunk"], 
                ["2", "Purina dog food brand"], 
                ["3", "Word after jelly or coffee"], 
                ["4", "Sports equipment with which you can do a \"pizza stop\""], 
                ["5", "Class that has its pluses and minuses"]]
}

def solve(  grid, across, down, grid_numbers):
    answer = [
                [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ', ' '], 
    ]
    across_clue_lengths = get_clue_lengths(grid, grid_numbers, across, "across")
    down_clue_lengths = get_clue_lengths(grid, grid_numbers, down, "down")
    # across_candidate_lists = find_candidate_lists(across, across_clue_lengths)
    # down_candidate_lists = find_candidate_lists(down, down_clue_lengths)


    across_candidates_list = [
            (1, ['SAY', 'FAR', 'OLD', 'VIZ', 'JIT', 'GOD', 'WHO', 'HAD', 'ALE', 'MAR', 'NOT', 'NOV', 'ILL', 'USE', 'PUT', 'PER', 'ONE', 'JAN', 'HIS', 'TEA', 'BUT', 'TIE', 'ALL', 'AND', 'WAS', 'TEE', 'DET', 'POT', 'JUN', 'MAN', 'DAM', 'DAX', 'NOW', 'OCT', 'TAB', 'ROW', 'TOP', 'OUR', 'MAY', 'HOW', 'CAN', 'ITS', 'ARE', 'THE', 'YOU', 'ADD', 'HIT', 'DUE', 'FEW', 'NUT', 'SEE', 'BAR', 'NEW', 'SUM', 'FEB', 'FOR', 'WAY', 'SET']),
            (4, ['SMILE', 'CLARK', 'ASKED', 'OFTEN', 'MUSIC', 'SHOWN', 'ABOUT', 'HELIX', 'STORE', 'BSIDE', 'ORGAN', 'MONTH', 'GLARE', 'BONUS', 'PRINT', 'FACES', 'QUITE', 'STYLE', 'SPLIT', 'COURT', 'RADIO', 'DRUMS', 'PHOTO', 'PATHS', 'AFTER', 'ALBUM', 'LOWER', 'MATTO', 'YEARS', 'UNDER', 'JIMMY', 'VOICE', 'VINCI', 'ISSUE', 'BEGAN', 'ROOTS', 'IMAGE', 'STUFF', 'ALONG', 'DRIED', 'VISIT', 'BEING', 'STEVE', 'THEME', 'EVENT', 'FIFTH', 'TERMS', 'KINGS', 'STONE', 'THEIR', 'SHOWS', 'BLUES', 'PUNKY', 'GIRLS', 'LIKES', 'TAKES', 'LIFES', 'SUPER', 'EARTH', 'SOUTH', 'SHMCD', 'MIXED', 'OUTDO', 'TASTE', 'STAND', 'APPLE', 'FLASH', 'THERE', 'THINK', 'DECCA', 'EVANS', 'THREE', 'WYMAN', 'WHICH', 'NEVER', 'BATES', 'FLUTE', 'COULD', 'GÜIRO', 'ABKCO', 'MACRO', 'FRANK', 'TOUCH', 'BUILD', 'WORLD', 'LINKS', 'JONES']),
            (6, ['OFTEN', 'MUSIC', 'ABOUT', 'GIVEN', 'HUELL', 'ATTIC', 'PRIME', 'STYLE', 'CHECK', 'FAULT', 'AFTER', 'SIGMA', 'KÁPPA', 'DELTA', 'YOUNG', 'BEGIN', 'BEING', 'EVENT', 'ISAAC', 'ELENI', 'DOORS', 'THICK', 'GIRLS', 'ΚΆΠΠΑ', 'ELLAS', 'STEEL', 'AGORA', 'GAMMA', 'LATIN', 'SNBSP', 'LACKS', 'VIEWS', 'WHICH', 'FLUID', 'TENTH', 'CLICK', 'ANBSP', 'ENJOY', 'WHERE', 'POWER', 'GRAVE', 'GROUP', 'ROMAN', 'ACUTE', 'CRETE', 'OMEGA', 'ˈKÆPƏ', 'THESE', 'VALUE', 'NAMED', 'AULIS', 'CURVE', 'KRINO', 'KFLAY', 'SOUND', 'SALAD', 'RATIO', 'KOINE', 'AMMON', 'UPPER', 'USING', 'GRECO', 'AGENT', 'AROSE', 'GRAPH', 'THÊTA', 'GREEK', 'ELIAS', 'FIRST', 'CASES', 'LEARN', 'SHARE', 'ΚΟΙΝΗ', 'VOWEL', 'CHAOS', 'ALPHA', 'ΨNBSP', 'KAPPA', 'EARLY', 'ARYAN', 'OTHER', 'DORIC', 'NAMES']),
            (7, ['ITSON', 'KOREA', 'VALOR', 'ABOUT', 'MONTH', 'MACAU', 'HOENN', 'READY', 'NOTES', 'LEVEL', 'THOSE', 'WHOLE', 'FULLY', 'SMALL', 'BEING', 'BEGIN', 'GUIDO', 'EVENT', 'RISKS', 'SWAPS', 'EXIST', 'THEIR', 'GAMES', 'BRUSH', 'SHALL', 'APPLE', 'TOTAL', 'VIEWS', 'BALLS', 'FRANK', 'AIMED', 'INAPP', 'LIGHT', 'HOPED', 'ANNIE', 'VALID', 'AWARD', 'WHITE', 'GREEN', 'STILL', 'SALES', 'TRUCK', 'WANNA', 'CHINA', 'APRIL', 'SEOUL', 'CLANS', 'GOTTA', 'NAMED', 'TREND', 'TEAMS', 'JULIA', 'USAGE', 'VERSE', 'SHOOT', 'DRIVE', 'TOUGH', 'CAIRO', 'FIRST', 'CRUSH', 'GRANT', 'SPOTS', 'URBAN', 'LEARN', 'TASKS', 'MANIA', 'LARGE', 'COMIC', 'DUTCH', 'JOHTO', 'STEER', 'AHEAD', 'TRAIN', 'SEEMS', 'LEAVE', 'UNTIL', 'DAYUS', 'TRUMP', 'SHAPE', 'MOVES', 'MUSIC', 'AREAS', 'ITALY', 'STORE', 'BONUS', 'RANGE', 'GMAIL']),
            (8, ['SAY', 'FAR', 'SAN', 'STE', 'WHO', 'HAD', 'ETC', 'DEC', 'EYE', 'VIA', 'HAS', 'LAY', 'ADJ', 'NOT', 'APR', 'USE', 'BAD', 'TOO', 'ANY', 'GET', 'ONE', 'SHE', 'OWN', 'OUT', 'APP', 'BUT', 'AGE', 'OPT', 'FƏL', 'CUE', 'DAY', 'COY', 'SHY', 'LOW', 'ALL', 'AND', 'WAS', 'HER', 'DRD', 'WAY', 'BIT', 'HTT', 'NOW', 'HEY', 'TOP', 'OUR', 'MAY', 'HOW', 'ACT', 'CAN', 'ITS', 'YET', 'ARE', 'HWY', 'SHT', 'ASK', 'THE', 'YOU', 'III', 'TWO', 'WHY', 'HAT', 'SEE', 'RUN', 'NEW', 'NYC', 'FOR', 'ODD', 'JOE', 'SET', 'LRV'])
            ]
    down_candidates_list = [ 
        (4, ['HERE', 'GEAR', 'JUNE', 'LEFT', 'SUCH', 'SALE', 'GROW', 'SHIP', 'YEAR', 'PROM', 'MIND', 'WHEN', 'BEEN', 'SARA', 'LOGO', 'FATE', 'KNOW', 'FIVE', 'JOBS', 'FROM', 'HUNT', 'WELL', 'TYPE', 'CLUE', 'PART', 'FELT', 'LESS', 'KPMG', 'ONLY', 'GOAL', 'ONCE', 'BEAG', 'FIRM', 'TOWN', 'FALL', 'SOLD', 'ROAD', 'USED', 'BRAH', 'MANY', 'THUS', 'MOVE', 'LAID', 'TOSS', 'LINE', 'TEXT', 'SETS', 'BEST', 'TWIN', 'TOOK', 'AWAY', 'KIND', 'LAST', 'FLOW', 'OVER', 'FAIR', 'HAVE', 'BUTT', 'CITY', 'SAME', 'COST', 'HOLD', 'YOUR', 'NINE', 'WHAT', 'LOSS', 'VERY', 'TANS', 'JUDI', 'WERE', 'WITH', 'LIKE', 'CUTS', 'SELL', 'CASE', 'RAMS', 'SHOP', 'GIFT', 'MUST', 'SOME', 'WEEK', 'EACH', 'POOL', 'FUND', 'BAGS', 'SKIS', 'BIKE', 'JUST', 'ALSO', 'PAID', 'SAID', 'MORE', 'CCAA', 'DONT', 'THEM', 'SHOT', 'MUCH' ]),
        (1, ['MIGHT', 'HENRY', 'DRINK', 'THATS', 'TRACK', 'MUSIC', 'SOBER', 'BLIND', 'MOVIE', 'DRAWN', 'ENTRY', 'VELTZ', 'HELPS', 'LETHE', 'FIRST', 'PAUSE', 'QUITE', 'MERRY', 'TASTE', 'URBAN', 'THESE', 'SPEND', 'CHART', 'THERE', 'TOTAL', 'QUOTA', 'THREE', 'WRITE', 'VIEWS', 'MOORE', 'PLACE', 'ROUND', 'BEERY', 'YEARS', 'LABEL', 'MEANS', 'TIPSY', 'JIMMY', 'UNDER', 'TIGHT', 'SWILL', 'WORSE', 'STIFF', 'NIGHT', 'VIDEO', 'ENJOY', 'THING', 'POTTY', 'LOLHE', 'ABOMB', 'YOURE', 'JOLLY', 'BEING', 'TODDY', 'STORY', 'DRUNK', 'MEGAN', 'DAVID', 'DRAFT', 'SLEEP']),
        (2, ['HERE', 'SUED', 'SUCH', 'DOWN', 'YEAR', 'TONS', 'LOVE', 'MEET', 'WHEN', 'SWOT', 'BEEN', 'RUSK', 'FILL', 'MAIN', 'SLIM', 'SCAR', 'PART', 'LESS', 'ONLY', 'DIET', 'GOYA', 'STAY', 'SOLD', 'USED', 'MANY', 'DRUG', 'SEND', 'HEAR', 'LINE', 'BEST', 'SPOT', 'SOUL', 'HAVE', 'CITY', 'COST', 'NOTE', 'KILL', 'YOUR', 'READ', 'WHAT', 'LITE', 'WERE', 'WITH', 'LIKE', 'CUTS', 'CHOP', 'SNAP', 'RING', 'SOME', 'WEEK', 'SITE', 'POST', 'BIRD', 'NEXT', 'CARE', 'ALSO', 'SAID', 'MORE', 'BOWL', 'ROLL', 'CAFE', 'MARS', 'CHOW', 'FLEA', 'WORK', 'FIND', 'CLUB', 'THAT', 'WORM', 'WILD', 'TIME', 'SHOW', 'TRAY', 'PETS', 'THEY', 'GAME', 'WOLF', 'MADE', 'FREE', 'FULL', 'REAL', 'TIDY', 'FILM', 'BLUE', 'LOSE', 'HIGH', 'BURN', 'MCTS', 'NAME', 'INTO', 'GREW', 'DOGS', 'TICK', 'TIPS', 'ASIA', 'ALPO', 'MEOW' ]),
        (3, ['HERE', 'LORD', 'SFOG', 'AGAR', 'BASE', 'ONES', 'WHEN', 'BEEN', 'DAYS', 'ARAB', 'LASH', 'WELL', 'CLUE', 'ONLY', 'OTTO', 'SOLD', 'USED', 'MANY', 'AKIN', 'BEST', 'TOOK', 'EDEN', 'LAST', 'JEWS', 'ARTS', 'LAMB', 'OVER', 'HAVE', 'SAME', 'GERM', 'YOUR', 'READ', 'ROOT', 'WERE', 'WITH', 'TOED', 'SELL', 'EVER', 'ADAM', 'MUST', 'ELSE', 'EACH', 'SITE', 'BEAN', 'POST', 'STET', 'CALL', 'ALSO', 'MORE', 'NONE', 'ROLL', 'TAIL', 'THEM', 'BUYS', 'ספוג', 'VIDE', 'LAWS', 'WORK', 'AMEN', 'IDOL', 'FIND', 'STIR', 'THAT', 'TIME', 'JELL', 'GAME', 'THEY', 'CLIP', 'PURL', 'MADE', 'FREE', 'TINY', 'FORM', 'EVEN', 'VISA', 'NAME', 'LARD', 'FIRE', 'MINI', 'USES', 'THAN', 'WORD', 'MAKE', 'HEAD', 'SIZE', 'THIS', 'GRAM', 'LATE', 'STEM', 'FOOD', 'ARAQ', 'NBSP', 'MOST', 'YORK', 'PEAS', 'FROM', 'THEN']),
        (5, ['HERE', 'BEEN', 'RACE', 'KNOW', 'PART', 'CLUE', 'ONLY', 'LESS', 'ONCE', 'USED', 'MANY', 'LINE', 'LAST', 'ACID', 'HAVE', 'SAME', 'TEND', 'YOUR', 'READ', 'NINE', 'ZONE', 'WITH', 'LIKE', 'CUTS', 'CASE', 'SHOP', 'VICE', 'SOME', 'SNOB', 'JUST', 'ALSO', 'JAIR', 'MORE', 'DONT', 'HAIR', 'HEIR', 'SIGN', 'FIND', 'CONS', 'GOES', 'THAT', 'FRAC', 'PLUS', 'THEY', 'OILS', 'NEAR', 'WANT', 'ZERO', 'FORM', 'EVEN', 'GOOD', 'REAL', 'ISIF', 'HIGH', 'TAKE', 'LIVE', 'SKIP', 'WILL', 'BARS', 'THAN', 'SIDE', 'CONE', 'JAVA', 'FLEX', 'HEAD', 'DOES', 'PLAN', 'MEAN', 'LIFE', 'BOOM', 'PROS', 'ERIC', 'MOST', 'BOTH', 'RULE', 'THIS', 'FROM', 'THEN'])
        ]

    test_across = [
            (1, ['SAY', 'TAB']),
            (4, ['SMILE']),
            (6, ['OFTEN', 'KAPPA']),
            (7, ['ITSON']),
            (8, ['SHY'])
            ]
    test_down = [ 
        (4, ['HERE', 'SKIS']),
        (1, ['TIPSY']),
        (2, ['HERE', 'ALPO']),
        (3, ['HERE', 'BEAN']),
        (5, ['MATH'])
        ]

    results = rec_insert(grid, grid_numbers, answer, test_across, test_down, True, 0)
    input("Finito")
    for result in results:
        for row in result:
            print(row)
        print("------")
    print(len(results))

    return answer

def find_candidate_lists(clues, clue_lengths):
    candidate_lists = []
    for clue in clues:
        print("Finding answers for clue", clue[1], "length", clue_lengths[str(clue[0])])
        candidate_list = find_candidates(clue[1], clue_lengths[str(clue[0])])
        candidate_lists.append( (clue[0], candidate_list) )
    return candidate_lists

def find_candidates(clue, length):
    candidates_list = []
    # search clue
    filtered_clue = word_eliminator.remove_escape_sequences(clue)
    google_results = google_search.search_google(filtered_clue, length)
    candidates_list.extend(google_results[:50])
    wikipedia_results = wikipedia_search.wikipedia_search(filtered_clue, length)
    candidates_list.extend(wikipedia_results[:50])
    datamuse_results = datamuse.get_words_with_similar_meaning(clue, length)
    candidates_list.extend(datamuse_results[:50])
    candidates_list = word_eliminator.eliminate_duplicates(candidates_list)
    return candidates_list

def empty_tile_number(grid, current_grid):
    empty_no = 0
    for x, row in enumerate(grid):
        for y, tile in enumerate(row):
            if tile == 0 and current_grid[x][y] == ' ':
                empty_no += 1
    return empty_no

def rec_insert(grid, grid_numbers, current_grid, acro_cand_list, down_cand_list, turn, skipped):
    print("Current puzzle grid")
    for row in current_grid:
        print(row)
    print("*****")
    across_count = len(acro_cand_list) 
    down_count = len(down_cand_list)
    add_across = False
    add_down = False
    if across_count <= 0 and down_count <= 0:
        print("No clues left.. Current grid:")
        for row in current_grid:
            print(row)
        print("*****")
        return [ [row[:] for row in current_grid] ]
    elif across_count > 0 and turn:
        add_across = True
    elif down_count > 0 and not turn:
        add_down = True
    elif across_count > 0:
        add_across = True
    elif down_count > 0:
        add_down = True

    possible_outcomes = []
    if add_across:
        next_across_tup = acro_cand_list[0]
        clue_no = next_across_tup[0]
        cand_list = next_across_tup[1]
        start, end = start_and_end(grid, grid_numbers, clue_no, "across")
        possible_branches = []
        for candidate in cand_list:
            print("trying to insert", candidate)
            inserted = insert_to_grid(current_grid, start, end, candidate)
            if inserted is not None:
                print("Insert succesful.. New grid is")
                for row in inserted:
                    print(row)
                print("*****")
                append_unique(possible_branches, inserted)
        
        if len(possible_branches) == 0 and skipped < 1:
            possible_branches = [ [row[:] for row in current_grid] ]
            skipped += 1

        for branch in possible_branches:
            outcomes = rec_insert(grid, grid_numbers, branch, acro_cand_list[1:], down_cand_list, not turn, skipped)
            for outcome in outcomes:
                append_unique(possible_outcomes, outcome)

    elif add_down:
        next_down_tup = down_cand_list[0]
        clue_no = next_down_tup[0]
        cand_list = next_down_tup[1]
        start, end = start_and_end(grid, grid_numbers, clue_no, "down")
        possible_branches = []
        for candidate in cand_list:
            inserted = insert_to_grid(current_grid, start, end, candidate)
            if inserted is not None:
                print("Insert succesful.. New grid is")
                for row in inserted:
                    print(row)
                print("*****")
                append_unique(possible_branches, inserted)
        
        if len(possible_branches) == 0 and skipped < 1:
            print("No insert can be made.. Returning the old grid:")
            for row in current_grid:
                print(row)
            print("*****")
            possible_branches = [ [row[:] for row in current_grid] ]
            skipped += 1
        for branch in possible_branches:
            outcomes = rec_insert(grid, grid_numbers, branch, acro_cand_list, down_cand_list[1:], not turn, skipped)
            for outcome in outcomes:
                append_unique(possible_outcomes, outcome)

    return possible_outcomes

# Turn true denotes adding across clue next
def insert_recursively(grid, grid_numbers, current_grid, across_candidates_list, down_candidates_list, inserted, turn=True):
    across_count = len(across_candidates_list) 
    down_count = len(down_candidates_list)
    add_across = False
    add_down = False
    if across_count <= 0 and down_count <= 0:
        return [ ([row[:] for row in current_grid], inserted) ]
    elif across_count > 0 and turn:
        add_across = True
    elif down_count > 0 and not turn:
        add_down = True
    elif across_count > 0:
        add_across = True
    elif down_count > 0:
        add_down = True
    skipped = 0
    new_branches = []
    if add_across:
        next_across = across_candidates_list[0]
        start_acc, end_acc = start_and_end(grid, grid_numbers, int(next_across[0]), "across")
        current_findings = []
        for candidate in next_across[1]:
            try_to_insert = insert_to_grid(current_grid, start_acc, end_acc, candidate)
            if try_to_insert is not None:
                print("Made an insertion..")
                for row in try_to_insert:
                    print(row)
                print("*****")
                input()
                append_unique(current_findings, (try_to_insert, inserted + 1))

        new_branches = []
        for finding in current_findings:
            print("Try to branch from this:")
            for row in finding[0]:
                print(row)
            print("*****")
            input()
            next_candidates = insert_recursively(grid, grid_numbers, finding[0], across_candidates_list[1:], down_candidates_list, finding[1], not turn)
            
            if next_candidates[0][0] == current_grid:
                skipped = 1
            new_branches.extend(next_candidates)

    elif add_down:
        next_down = down_candidates_list[0]
        start_down, end_down = start_and_end(grid, grid_numbers, int(next_down[0]), "down")
        current_findings = []
        for candidate in next_down[1]:
            try_to_insert = insert_to_grid(current_grid, start_down, end_down, candidate)
            if try_to_insert is not None:
                print("Made an insertion..")
                for row in try_to_insert:
                    print(row)
                print("*****")
                append_unique(current_findings, (try_to_insert, inserted + 1))

        new_branches = []
        for finding in current_findings:
            print("Try to branch from this:")
            for row in finding[0]:
                print(row)
            print("*****")
            input()
            next_candidates = insert_recursively(grid, grid_numbers, finding[0], across_candidates_list, down_candidates_list[1:], finding[1], not turn)
            if next_candidates[0][0] == current_grid:
                skipped = 1
            new_branches.extend(next_candidates)

    # max_filled = []
    # max_inserted = 0
    
    # for branch in new_branches:
    #     if branch[1] > max_inserted:
    #         max_inserted = branch[1]
    # for branch in new_branches:
    #     if branch[1] == max_inserted:
    #         max_filled.append(branch) 
    if len(new_branches) == 0 and skipped < 1:
        print("Could not find an option from", across_candidates_list[0] if add_across else down_candidates_list[0], "Returning skip = ", skipped + 1)
        for row in current_grid:
            print(row)
        print("*******")
        input()
        return [ ([row[:] for row in current_grid], inserted) ]
    elif len(new_branches) == 0 and skipped >= 1:
        print("Could not find an option from", across_candidates_list[0] if add_across else down_candidates_list[0], "No skip left")
        for row in current_grid:
            print(row)
        print("*******")
        input()
        return []
    return new_branches

def insert_clues(grid, grid_numbers, current_grid, across_candidates_list, down_candidates_list):
    across_count = len(across_candidates_list) - 1
    down_count = len(down_candidates_list) - 1
    possible_answers = [ [row[:] for row in current_grid] ]
    while across_count >= 0 and down_count >= 0:
        next_across = across_candidates_list[across_count]
        start_acc, end_acc = start_and_end(grid, grid_numbers, int(next_across[0]), "across")
        current_findings = []
        for possible_answer in possible_answers:
            append_unique(current_findings, possible_answer)
            for candidate in next_across[1]:
                try_to_insert = insert_to_grid(possible_answer, start_acc, end_acc, candidate)
                if try_to_insert is not None:
                    append_unique(current_findings, try_to_insert)
        across_count -= 1
        possible_answers = current_findings
        current_findings = []
        next_down = down_candidates_list[down_count]
        start_dwn, end_dwn = start_and_end(grid, grid_numbers, int(next_down[0]), "down")
        for possible_answer in possible_answers:
            append_unique(current_findings, possible_answer)
            for candidate in next_down[1]:
                try_to_insert = insert_to_grid(possible_answer, start_dwn, end_dwn, candidate)
                if try_to_insert is not None:
                    append_unique(current_findings, try_to_insert)
        down_count -= 1
        possible_answers = current_findings

    # If left
    while across_count >= 0:
        next_across = across_candidates_list[across_count]
        start_acc, end_acc = start_and_end(grid, grid_numbers, int(next_across[0]), "across")
        current_findings = []
        for possible_answer in possible_answers:
            append_unique(current_findings, possible_answer)
            for candidate in next_across[1]:
                try_to_insert = insert_to_grid(possible_answer, start_acc, end_acc, candidate)
                if try_to_insert is not None:
                    append_unique(current_findings, try_to_insert)
        across_count -= 1
        possible_answers = current_findings

    while down_count >= 0:
        next_across = across_candidates_list[across_count]
        start_acc, end_acc = start_and_end(grid, grid_numbers, int(next_across[0]), "across")
        current_findings = []
        for possible_answer in possible_answers:
            append_unique(current_findings, possible_answer)
            for candidate in next_across[1]:
                try_to_insert = insert_to_grid(possible_answer, start_acc, end_acc, candidate)
                if try_to_insert is not None:
                    append_unique(current_findings, try_to_insert)
        across_count -= 1
        possible_answers = current_findings
    
    return possible_answers

def insert_to_grid(current_grid, start, end, word):
    temp_grid = [row[:] for row in current_grid]
    x = start[0]
    y = start[1]
    while x <= end[0] and y <= end[1]:
        if start[0] == end[0]: # across
            if temp_grid[x][y] == " " or temp_grid[x][y] == word[y - start[1]]:
                temp_grid[x][y] = word[y - start[1]]
                y += 1
            else:
                return # Cannot insert
        elif start[1] == end[1]: # down
            if temp_grid[x][y] == " " or temp_grid[x][y] == word[x - start[0]]:
                temp_grid[x][y] = word[x - start[0]]
                x += 1
            else:
                return # Cannot insert
    return temp_grid

def get_clue_lengths(grid, grid_numbers, clues, direction):
    clue_lengths = {}
    for clue in clues:
        start, end = start_and_end(grid, grid_numbers, int(clue[0]), direction)
        length = 0
        if direction == "down":
            length = end[0] - start[0] + 1
        elif direction == "across":
            length = end[1] - start[1] + 1
        clue_lengths[clue[0]] = length
    return clue_lengths

def start_and_end(grid, grid_numbers, clue_no, direction):
    starting_pos = start_position(grid_numbers, clue_no)
    ending_pos = end_position(grid, starting_pos, direction) 
    return starting_pos, ending_pos

def start_position(grid_numbers, clue_no):
    for x in range(5):
        for y in range(5):
            if int(grid_numbers[x][y]) == clue_no:
                return (x, y)

def end_position(grid, start_position, direction):
    x = start_position[0]
    y = start_position[1]
    if direction == "across":
        while y < 4 and grid[x][y + 1] != 1:
            y += 1
    elif direction == "down":
        while x < 4 and grid[x + 1][y] != 1:
            x += 1
    return (x, y)    

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def remove_punctuation(inputString):
    return inputString.translate(str.maketrans('', '', string.punctuation))

def process_list(input_list):
    unique_words = set(input_list) # remove duplicates
    words_without_punc = [remove_punctuation(x) for x in unique_words]
    short_words = [x for x in words_without_punc if len(x) <= 5 and len(x) > 1] # find all words with less than or equal to 5 characters
    none_number_words = [x for x in short_words if not has_numbers(x)]
    none_stop_words = [x for x in none_number_words if x not in stopwords.words('english')] # remove stop-words
    result_words = [x.lower() for x in none_stop_words]
    return result_words

def append_unique(append_to, target):
    if target not in append_to:
        append_to.append(target)

solve(SOLUTION["grid"], SOLUTION["across"], SOLUTION["down"], SOLUTION["grid_numbers"])
