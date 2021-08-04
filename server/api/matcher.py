from server.api.extensions import db
#from server.api.models import Question_Set, Answer, Matching_Point
from server.api.models import Matching_Point, Big_Answer, Little_Answer
from server.api.constants import BIG_QUESTION_SET_ID, LITTLE_QUESTION_SET_ID
from difflib import SequenceMatcher

#-----this file contains functions that do the matches



def get_similarity_ratio(a ,b):
    #FIXME: maybe do this when they are stored?
    a = a.strip().lower()
    b = b.strip().lower()
    if a=="nan" or b == "nan":
        return 0
    return SequenceMatcher(None, a, b).ratio()

#MIN_SIMILARITY_RATIO = 0.4
MIN_SIMILARITY_RATIO = 0.6

#in case the board member put down slightly different answers
SAME_ANSWER_SIMILARITY = 0.95


#exptected to return: {'0':{'id':..., 'name':..., 'email':..., 'age':..., 'major_dept':.., 'major':... '}, '1':{}, ...}
def generate_suggestions_for(big_id, count=20):

    temp_suggestions = {}

    db_big_submission = Big_Answer.query.filter(Big_Answer.id == big_id).first()

    if not db_big_submission:
        return {}

    big_submission_json = db_big_submission.get_json()

    email_idx = '0'
    name_idx = '1'
    age_idx = '2'
    year_idx = '4'
    major_dept_idx = '5'
    major_idx = '6'
    county_idx = '7'
    dorm_commute_idx = '9'
    dorm_commute_from_idx = '10'
    pactive_idx = '11'

    big_gender_idx = '12'
    big_expect_gender_idx = '13'

    little_expect_gender_idx = '12'
    little_gender_idx = '13'

    top_music_idx = '14'
    second_music_idx = '15'

    top_movie_idx = '16'
    second_movie_idx = '17'

    drink_idx = '18'

    answer_key = 'answer'
    weight_key = 'weight_int'

    big_age = big_submission_json[age_idx][answer_key]
    big_year = big_submission_json[year_idx][answer_key]
    big_major_dept = big_submission_json[major_dept_idx][answer_key]
    #big_major = big_submission_json[major_idx]['answer']
    big_county = big_submission_json[county_idx][answer_key]
    big_dorm_commute = big_submission_json[dorm_commute_idx][answer_key]
    big_dorm_commute_from = big_submission_json[dorm_commute_from_idx][answer_key]
    big_pactive = big_submission_json[pactive_idx][answer_key]

    big_gender = big_submission_json[big_gender_idx][answer_key].lower()
    big_expect_gender = big_submission_json[big_expect_gender_idx][answer_key].lower().replace(" ","")

    big_top_music = big_submission_json[top_music_idx][answer_key]
    big_second_music = big_submission_json[second_music_idx][answer_key]
    big_top_movie = big_submission_json[top_movie_idx][answer_key]
    big_second_movie = big_submission_json[second_movie_idx][answer_key]
    big_drink = big_submission_json[drink_idx][answer_key].lower()


    db_littles = Little_Answer.query.all()

    for one_little in db_littles:
        if one_little.is_paired:
            continue

        total_pt = 0
        print("---one little: ", one_little.id)

        little_submission_json = one_little.get_json()

        #--1: age need to be within 2 years difference
        little_age = little_submission_json[age_idx][answer_key]
        try:
            if abs(int(big_age) - int(little_age)) <= 2:
                total_pt += int(little_submission_json[age_idx][weight_key])
                #print("---print age difference is within 2.., pt now: ", total_pt )
        except:
            pass


        #--2: year in school need to be within 2 years difference
        little_year = little_submission_json[year_idx][answer_key]
        try:
            if abs(_year_to_int(little_year) - _year_to_int(big_year)) <= 2:
                total_pt += int(little_submission_json[year_idx][weight_key])
                #print("---school year difference is within 2.., weight: ", int(little_submission_json[year_idx][weight_key]) )
        except:
            pass

        #--3: major department
        little_major_dept = little_submission_json[major_dept_idx][answer_key]
        if not (big_major_dept == "" or little_major_dept == ""):
            similarity_ratio = get_similarity_ratio(big_major_dept, little_major_dept)

            # in case the board member put down slightly different answers
            if similarity_ratio >= SAME_ANSWER_SIMILARITY:
                total_pt += int(little_submission_json[major_dept_idx][weight_key])
                #print("---major department match.., weight: ", int(little_submission_json[major_dept_idx][weight_key]) )


        #--4: county
        little_county = little_submission_json[county_idx][answer_key]
        if not (big_county == "" or little_county == ""):
            similarity_ratio = get_similarity_ratio(big_county, little_county)

            if similarity_ratio >= SAME_ANSWER_SIMILARITY:
                total_pt += int(little_submission_json[county_idx][weight_key])
                #print("---county match.., weight: ", int(little_submission_json[county_idx][weight_key]) )


        #--5: dorm / commute
        little_dorm_commute = little_submission_json[dorm_commute_idx][answer_key]
        if not (little_dorm_commute == "" or big_dorm_commute == ""):
            similarity_ratio = get_similarity_ratio(big_dorm_commute, little_dorm_commute)

            if similarity_ratio >= SAME_ANSWER_SIMILARITY:
                total_pt += int(little_submission_json[dorm_commute_idx][weight_key])
                #print("---dorm match.., weight: ", int(little_submission_json[dorm_commute_idx][weight_key]) )


        #--6: dorm_commute_from
        little_dorm_commute_from = little_submission_json[dorm_commute_from_idx][answer_key]
        if not (big_dorm_commute_from == "" or little_dorm_commute_from == ""):
            similarity_ratio = get_similarity_ratio(big_dorm_commute_from, little_dorm_commute_from)

            if similarity_ratio >= SAME_ANSWER_SIMILARITY:
                total_pt += int(little_submission_json[dorm_commute_from_idx][weight_key])
                #print("---dorm/commute from match.., weight: ", int(little_submission_json[dorm_commute_from_idx][weight_key]) )


        #--7: pactive
        little_pactive = little_submission_json[pactive_idx][answer_key]
        if not (big_pactive == "" or little_pactive == ""):
            similarity_ratio = get_similarity_ratio(big_pactive, little_pactive)

            if similarity_ratio >= SAME_ANSWER_SIMILARITY:
                total_pt += int(little_submission_json[pactive_idx][weight_key])
                #print("---pactive match.., weight: ", int(little_submission_json[pactive_idx][weight_key]) )


        #--8: little_expected_gender  <-->  big_gender
        little_expected_gender = little_submission_json[little_expect_gender_idx][answer_key].lower()
        if not (big_gender == "" or little_expected_gender == ""):
            similarity_ratio = get_similarity_ratio(big_gender, little_expected_gender)

            if similarity_ratio >= SAME_ANSWER_SIMILARITY:
                total_pt += int(little_submission_json[little_expect_gender_idx][weight_key])
                #print("---test 8 match.., weight: ", int(little_submission_json[little_expect_gender_idx][weight_key]) )


        #--9: little_gender  <--> big_expect_gender
        #little: little sister, little brother, other
        #big: all boys, all girls, one of each, surprise me
        little_gender = little_submission_json[little_gender_idx][answer_key].lower()


        denied_9 = False
        if "boys" in big_expect_gender:
            if "brother" in little_gender:
                total_pt += little_submission_json[little_gender_idx][weight_key]
            else:
                denied_9 = True

        elif not denied_9 and "girls" in big_expect_gender:
            if "sister" in little_gender:
                total_pt += little_submission_json[little_gender_idx][weight_key]
            else:
                denied_9 = True

        #other == other situation
        elif not denied_9 and get_similarity_ratio(big_expect_gender, "other") >= SAME_ANSWER_SIMILARITY:
            if get_similarity_ratio(little_gender, "other") >= SAME_ANSWER_SIMILARITY:
                total_pt += little_submission_json[little_gender_idx][weight_key]
            else:
                denied_9 = True

        #surprise me situation
        elif (not denied_9) and (not (big_expect_gender == "" or little_gender == "")):
            total_pt += little_submission_json[little_gender_idx][weight_key]



        #--10: music
        little_top_music = little_submission_json[top_music_idx][answer_key]
        little_second_music = little_submission_json[second_music_idx][answer_key]


        #one match
        if not little_top_music == "":
            if get_similarity_ratio(little_top_music, big_top_music ) >= SAME_ANSWER_SIMILARITY:
                total_pt += little_submission_json[top_music_idx][weight_key]
                #print("------------------------------------------ 10 c1")
            elif get_similarity_ratio(little_top_music, big_second_music) >= SAME_ANSWER_SIMILARITY:
                total_pt += little_submission_json[top_music_idx][weight_key]
                #print("------------------------------------------ 10 c2")

        #another match
        if not little_second_music == "":
            #make sure little don't put the same answer twice, looks like no need to take care of repeats in big
            if (not get_similarity_ratio(little_top_music, little_second_music) >= SAME_ANSWER_SIMILARITY):
                if get_similarity_ratio(little_second_music, big_top_music) >= SAME_ANSWER_SIMILARITY:
                    total_pt += little_submission_json[second_music_idx][weight_key]
                    #print("=========================================== 10 c3")
                elif get_similarity_ratio(little_second_music, big_second_music) >= SAME_ANSWER_SIMILARITY:
                    total_pt += little_submission_json[second_music_idx][weight_key]
                    #print("=========================================== 10 c4")

        #print("--10 after total pt: ", total_pt)

        #--11: movie
        little_top_movie = little_submission_json[top_movie_idx][answer_key]
        little_second_movie = little_submission_json[second_movie_idx][answer_key]

        #one match
        if not little_top_movie == "":
            if get_similarity_ratio(little_top_movie, big_top_movie) >= SAME_ANSWER_SIMILARITY:
                total_pt += little_submission_json[top_movie_idx][weight_key]
                #print("------------------------------------------ 11 c1")
            elif get_similarity_ratio(little_top_movie, big_second_movie) >= SAME_ANSWER_SIMILARITY:
                total_pt += little_submission_json[top_movie_idx][weight_key]
                #print("------------------------------------------ 11 c1")

        #second match
        if not little_second_movie == "":
            if (not get_similarity_ratio(little_top_movie, little_second_movie) >= SAME_ANSWER_SIMILARITY):
                if get_similarity_ratio(little_second_movie, big_top_movie) >= SAME_ANSWER_SIMILARITY:
                    total_pt += little_submission_json[second_movie_idx][weight_key]
                    #print("------------------------------------------ 11 c1")
                elif get_similarity_ratio(little_second_movie, big_second_movie) >= SAME_ANSWER_SIMILARITY:
                    total_pt += little_submission_json[second_movie_idx][weight_key]
                    #print("------------------------------------------ 11 c1")

        #print("--11 after total pt: ", total_pt)

        #--12: drink
        little_drink = little_submission_json[drink_idx][answer_key].lower()

        if not (big_drink == "" or little_drink == ""):
            #when they select the same answer
            if get_similarity_ratio(big_drink, little_drink) >= SAME_ANSWER_SIMILARITY:
                total_pt += little_submission_json[drink_idx][weight_key]
                #print("------------------ c1")

            #big: smoke,drink <-> little: both, corrupt
            elif ("smoke" in big_drink or "drink" in big_drink or "corrupt" in little_drink ) and ("both" in little_drink or "corrupt" in little_drink):
                total_pt += little_submission_json[drink_idx][weight_key]
                #print("------------------ c2")

            #bit: both,corrupt <-> little: smoke,drink
            elif ("both" in big_drink or "corrupt" in big_drink) and ("smoke" in little_drink or "drink" in little_drink or "corrupt" in little_drink):
                total_pt += little_submission_json[drink_idx][weight_key]
                #print("------------------ c3")

            #print("--total pt after: ", total_pt)

        cur_little_json = {
            'id': one_little.id,
            'name': little_submission_json[name_idx][answer_key],
            'age': little_submission_json[age_idx][answer_key],
            'emall': little_submission_json[email_idx][answer_key],
            'major_dept': little_submission_json[major_dept_idx][answer_key],
            'major': little_submission_json[major_idx][answer_key]

        }

        #{pt: [{}, {}, {}, ....], pt:[{}, {}, ...]}
        try:
            temp_suggestions[total_pt].append(cur_little_json)
        except:
            temp_suggestions[total_pt] = [cur_little_json]


    final_return_json = {}
    rank = 0
    #sort the dictionary by point
    for pt_key in sorted(temp_suggestions, reverse=True):
        # don't provide too many
        if rank >= count:
            break

        for one_little_json in temp_suggestions[pt_key]:
            # don't provide too many
            if rank >= count:
                break

            final_return_json[str(rank)] = one_little_json
            rank += 1

    print("----returning suggestions: ", final_return_json)

    return final_return_json















def _year_to_int(year_string):
    year = 5
    first_char = year_string[0]
    try:
        year = int(first_char)
    except:
        pass

    return year




def generate_suggestions_for_bigs(count=20):
    #get all big submissions
    all_big_submissions = Big_Answer.query.all()

    #get all little submission
    all_little_submissions = Little_Answer.query.all()
    little_json_list = [one_little_submission.get_json() for one_little_submission in all_little_submissions]

    #little_json_list_idx = 0
    len_little_json_list = len(little_json_list)

    #FIXME: did not loop over all little submission? what does this fixme mean?
    #loop over big submissions
    for one_big_submission in all_big_submissions:
        # {'0': {'point': the point, 'id': little id}, '1': {'point': the point, 'id': little id} }
        suggestions_json = {}
        big_answers_json = one_big_submission.get_json()

        #loop through one little submission at a time
        for little_json_list_idx in range(len_little_json_list):
            little_answer_json = little_json_list[little_json_list_idx]
            #little_json_list_idx += 1

            total_little_submission_point = 0

            #FIXME: i will loop over all questions, will only compare mc questions
            #compare one question at a time
            for one_q_key in big_answers_json:
                q_type = big_answers_json[one_q_key]['type']

                #skip current question if it's not multiple choice
                if q_type != 'mc':
                    continue

                big_question = big_answers_json[one_q_key]['question']
                big_answer = big_answers_json[one_q_key]['answer']
                big_question_id = big_answers_json[one_q_key]['id']
                big_weight = big_answers_json[one_q_key]['weight']

                #little typically has less questions
                try:
                    little_question = little_answer_json[one_q_key]['question']
                    little_answer = little_answer_json[one_q_key]['answer']
                    little_question_id = little_answer_json[one_q_key]['id']
                    little_weight = little_answer_json[one_q_key]['weight']

                    #FIXME: skip if weight point is 0
                    if big_weight == 0 and little_weight == 0:
                        continue

                    #FIXME: this part will need to be changed
                    similarity_ratio = get_similarity_ratio(big_answer, little_answer)

                    #FIXME: will change later
                    #FIXME: not store upone one question, should be upon on submission
                    #only store if ratio is large enough
                    if similarity_ratio >= MIN_SIMILARITY_RATIO:
                        #print("ratio: ", similarity_ratio, "___little answer: ", little_answer, " ==  Big answer: ", big_answer)
                        question_point = (little_weight + big_weight) * similarity_ratio
                        total_little_submission_point += question_point

                except:
                    break

            # final {'0': {'point': the point, 'id': little id}, '1': {'point': the point, 'id': little id} }
            # for now: use the point as key, so it's easier to order
            # FIXME: may need check, idx already add one top the top
            #FIXME: it is some how possible to get the same point
            #print("---little json_list idx: ", little_json_list_idx)
            if total_little_submission_point > 0:

                #FIXME: add more later
                suggestions_json[total_little_submission_point] = {
                    'point': total_little_submission_point,
                    'id': little_json_list_idx,
                    'name': little_answer_json['1']['answer'],
                    'email': little_answer_json['0']['answer'],
                    'age': little_answer_json['2']['answer'],
                    'major_dept': little_answer_json['6']['answer'],
                    'major': little_answer_json['7']['answer']

                }

            #store the suggestions back

        # final {'0': {'point': the point, 'id': little id}, '1': {'point': the point, 'id': little id} }
        idx = 0
        for key in sorted(suggestions_json, reverse=True):
            suggestions_json[str(idx)] = suggestions_json[key]
            del suggestions_json[key]
            idx += 1

        one_big_submission.suggested_littles_json = suggestions_json
        #db.session.commit()
        print("-----------stored in db: ", len(suggestions_json))
        print("---done..")

    db.session.commit()
    print("----all done")






#FIXME: backup
def generate_suggestions():
    all_big_submissions = Big_Answer.query.all()

    all_little_submissions = Little_Answer.query.all()
    little_json_list = [one_little_submission.get_json() for one_little_submission in all_little_submissions]

    #little_json_list_idx = 0
    len_little_json_list = len(little_json_list)
    #FIXME: did not loop over all little submission
    for one_big_submission in all_big_submissions:
        # {'0': {'point': the point, 'id': little id}, '1': {'point': the point, 'id': little id} }
        suggestions_json = {}
        big_answers_json = one_big_submission.get_json()

        #loop through one little submission at a time
        for little_json_list_idx in range(len_little_json_list):
            little_answer_json = little_json_list[little_json_list_idx]
            #little_json_list_idx += 1

            total_little_submission_point = 0

            #compare one question at a time
            for one_q_key in big_answers_json:
                big_question = big_answers_json[one_q_key]['question']
                big_answer = big_answers_json[one_q_key]['answer']
                big_question_id = big_answers_json[one_q_key]['id']
                big_weight = big_answers_json[one_q_key]['weight']

                #little typically has less questions
                try:
                    little_question = little_answer_json[one_q_key]['question']
                    little_answer = little_answer_json[one_q_key]['answer']
                    little_question_id = little_answer_json[one_q_key]['id']
                    little_weight = little_answer_json[one_q_key]['weight']

                    #FIXME: skip if weight point is 0
                    if big_weight == 0 and little_weight == 0:
                        continue

                    similarity_ratio = get_similarity_ratio(big_answer, little_answer)

                    #FIXME: not store upone one question, should be upon on submission
                    #only store if ratio is large enough
                    if similarity_ratio >= MIN_SIMILARITY_RATIO:
                        #print("ratio: ", similarity_ratio, "___little answer: ", little_answer, " ==  Big answer: ", big_answer)
                        question_point = (little_weight + big_weight) * similarity_ratio
                        total_little_submission_point += question_point

                except:
                    break

            # final {'0': {'point': the point, 'id': little id}, '1': {'point': the point, 'id': little id} }
            # for now: use the point as key, so it's easier to order
            # FIXME: may need check, idx already add one top the top
            #FIXME: it is some how possible to get the same point
            #print("---little json_list idx: ", little_json_list_idx)
            if total_little_submission_point > 0:
                suggestions_json[total_little_submission_point] = {
                    'point': total_little_submission_point,
                    'id': little_json_list_idx,
                    'name': little_answer_json['1']['answer'],
                    'email': little_answer_json['0']['answer']
                }

            #store the suggestions back

        # final {'0': {'point': the point, 'id': little id}, '1': {'point': the point, 'id': little id} }
        idx = 0
        for key in sorted(suggestions_json, reverse=True):
            suggestions_json[str(idx)] = suggestions_json[key]
            del suggestions_json[key]
            idx += 1

        one_big_submission.suggested_littles_json = suggestions_json
        #db.session.commit()
        print("-----------stored in db: ", len(suggestions_json))
        print("---done..")

    db.session.commit()
    print("----all done")

