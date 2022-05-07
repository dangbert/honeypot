import os
import json
from flask import Blueprint, request, jsonify, redirect, abort
from datetime import datetime
import glob

from app import getConfigForEnv
from config import CTX

config = getConfigForEnv()()
SAVE_DIR = config.SAVE_DIR
REDIRECT_URL = config.REDIRECT_URL or 'https://google.eu'

# CTX.hash('example')
PW_HASH = '$argon2id$v=19$m=65536,t=25,p=4$E2KMsdaaMybEWAuhVEqpdQ$E+vv073GiiebPFMt8aYy5iUeSeclAY2WFJSSZCAClKQ'

# https://github.com/pallets/flask/issues/348
bp = Blueprint('tracker', __name__)

def ensureDir(dir):
  if not os.path.exists(dir):
    print(f"created directory: {os.path.abspath(SAVE_DIR)}")
    os.mkdir(dir)

def trackRequest(path, token):
  ### save tracked data
  nowUtc = datetime.utcnow() 
  fname = os.path.join(SAVE_DIR, f"{nowUtc}.json")
  data = {
    'ip': request.remote_addr,
    'userAgent': request.headers.get('User-Agent'),
    'dateStrUtc': str(nowUtc),
    'dateEpoch': nowUtc.timestamp(),
    'token': token,
    'path': path,
  }

  ensureDir(SAVE_DIR)
  with open(fname, 'w') as f:
      json.dump(data, f, indent=2) # write indented json to file
      print(f"Wrote: {fname}")


@bp.route("/", methods=["GET"])
def home():
  token = request.args.get('t')
  trackRequest('/', token)
  return redirect(REDIRECT_URL, 307)

@bp.route("/link", methods=["GET"])
def link():
  token = request.args.get('t')
  trackRequest('/link', token)
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


  # read all tracked data
  allData = []
  for fname in glob.glob(os.path.join(SAVE_DIR, '*.json')):
       with open(fname) as f:
            allData.append(json.load(f))

  print(f"\nread {len(allData)} total data entries")

  # optionally filter by a desired token
  token = request.args.get('t')
  if token:
    if token == 'null':
      token = None # allow ability to explicitly search for null tokens
    print(f"filtering by token {token}")
    allData = list(filter(lambda x: x['token'] == token, allData))

  # optionally filter by link
  path = request.args.get('path')
  if path:
    print(f"filtering by path {path}")
    allData = list(filter(lambda x: x['path'] == path, allData))

  # sort by date (showing most recent first)
  allData = sorted(allData, key=lambda x: -1 * x['dateEpoch'])
  print(f"returning {len(allData)} entries")
  return jsonify(allData), 200