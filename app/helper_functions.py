from flask import request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, RioUser

def calculate_era(runs_allowed, outs_pitched):
    if outs_pitched == 0 and runs_allowed > 0:
        return -abs(runs_allowed)
    elif outs_pitched > 0:
        return runs_allowed/(outs_pitched/3)
    else:
        return 0

def format_tuple_for_SQL(in_tuple):
    sql_tuple = "(" + ",".join(repr(v) for v in in_tuple) + ")"
    
    return (sql_tuple, (len(in_tuple) == 0))

def format_list_for_SQL(in_list):
    return format_tuple_for_SQL(tuple(in_list))


def sanatize_ints(str):
  not_statement = True if str[0] == '!' else False

  arr = []
  if not_statement:
    str = str[1:]

  if '!' in str:
    abort(400, 'Cannot have ! after param[0]')

  arr = str.split('_')
  final_arr = list()
  for val in arr:
    if '-' in val:
      temp_arr = val.split('-')
      for num in list(range(int(temp_arr[0]), int(temp_arr[1]) + 1)):
        final_arr.append(num)
    else:
      final_arr.append(int(val))

  return final_arr

@jwt_required(optional=True)
def get_user(dict):
  try:
    if dict.jwt:
      username = get_jwt_identity()
      user = RioUser.query.filter_by(username=username).first()
    if dict.rio_key:
      user = RioUser.query.filter_by(rio_key=dict.rio_key).first()
    if dict.username:
      username_lowercase = dict.username.lower()
      user = RioUser.query.filter_by(username_lowercase=username_lowercase).first()
    return user if user else False
  except:
    return False