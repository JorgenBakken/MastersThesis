#!/usr/bin/python

from .src.dataparse import parse_asf, parse_amc
from .db.select_from_db import get_animation, get_subject, get_animation_id_set
from .db.similarity_db import check_animation_id, insert_similarity, insert_signature_distance

def fetch_animations(max, animation_id = None, file_name = None, description = None, 
        subject_file_name = None, subject_fkey = None):
    """
    Fetches animations from the database and returns a list of tuples of the form
    (skeleton, animation, description)
    """
    animations = get_animation(animation_id, file_name , description,
            subject_file_name , subject_fkey)
    #if fetchone
    if animation_id or file_name:
            a = parse_amc(animations[1])
            a.move_root_to_origin()
            s = parse_asf(get_subject(animation_file_name = animations[0])[1])
            s.precompute_local_matrices()
            description = animations[2]
            return (s, a, description)


    arr = []
    for i in range(min(len(animations), max)):
        try:
            a = parse_amc(animations[i][1])
            a.move_root_to_origin()
            s = parse_asf(get_subject(animation_file_name = animations[i][0])[1])
            s.precompute_local_matrices()
            description = animations[i][2]
            arr.append((s, a, description))
        except:
            print("Error caught in animation_manager, anim: %d" % i)
    return arr

def unpack(element):
    """
    Unpacks a tuple of size 3 into 3 variables
    """
    return element[0], element[1], element[2]

def fetch_animation_id_set(description = None, subject_fkey = None, count = None):
    """
    Fetches a set of animation ids from the database
    """
    id_set = get_animation_id_set(description, subject_fkey, count)
    return [id[0] for id in id_set]

def check_already_calculated(animation_id1, animation_id2):
    """
    Checks if the similarity between two animations has already been calculated
    """
    return check_animation_id(animation_id1, animation_id2)

def save_similarity(animation_id1, animation_id2, distance, dp_distance, size1, size2):
    """
    Saves the similarity between two animations in the database
    """
    number_calculated = 0
    total = None
    if not check_already_calculated(animation_id1, animation_id2):
        total = insert_similarity(animation_id1, animation_id2, distance, dp_distance, size1, size2)
        number_calculated += 1

    if not check_already_calculated(animation_id2, animation_id1):
        total = insert_similarity(animation_id2, animation_id1, distance, dp_distance, size1, size2)
        number_calculated += 1
    return total, number_calculated 

def save_signature_distance(animation_id1, animation_id2, signature_distance):
    """
    Saves the signature distance between two animations in the database
    Performs the same operation twice, since the signature distance is symmetric
    """
    insert_signature_distance(animation_id1, animation_id2, signature_distance)
    insert_signature_distance(animation_id2, animation_id1, signature_distance)


