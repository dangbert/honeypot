import os
import json
from flask import Blueprint, request, jsonify, redirect, abort
from datetime import datetime
import glob

from app import getConfigForEnv
from config import CTX

config = getConfigForEnv()()
SAVE_DIR = config.SAVE_DIR
REDIRECT_URL = config.REDIRECT_URL

# CTX.hash('example')
PW_HASH = '$argon2id$v=19$m=65536,t=25,p=4$E2KMsdaaMybEWAuhVEqpdQ$E+vv073GiiebPFMt8aYy5iUeSeclAY2WFJSSZCAClKQ'

# https://github.com/pallets/flask/issues/348
bp = Blueprint('tracker', __name__)

def ensureDir(dir):
  if not os.path.exists(dir):
    print(f"created directory: {os.path.abspath(SAVE_DIR)}")
    os.mkdir(dir)

@bp.route("/", methods=["GET"])
def home():
  ensureDir(SAVE_DIR)

  ### save tracked data
  nowUtc = datetime.utcnow() 
  fname = os.path.join(SAVE_DIR, f"{nowUtc}.json")
  data = {
    'ip': request.remote_addr,
    'userAgent': request.headers.get('User-Agent'),
    'dateStrUtc': str(nowUtc),
    'dateEpoch': nowUtc.timestamp(),
  }

  with open(fname, 'w') as f:
      json.dump(data, f, indent=2) # write indented json to file
      print(f"Wrote: {fname}")

  #return jsonify({'hi': 'world'}), 200
  return redirect(REDIRECT_URL, 307)


@bp.route("/report", methods=["GET"])
def report():
  """read stored data"""
  # authentication:
  password = request.args.get('pass')
  if not password:
    abort(404)
  if not CTX.verify(password, PW_HASH):
    abort(404)

  # return all tracked data
  allData = []
  for fname in glob.glob(os.path.join(SAVE_DIR, '*.json')):
       with open(fname) as f:
            allData.append(json.load(f))
  return jsonify(allData), 200