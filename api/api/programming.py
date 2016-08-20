from flask import current_app as app, Blueprint, request, session

from decorators import api_wrapper, login_required, team_required, WebException
from models import db, Problems, ProgrammingSubmissions, Solves, Activity

import imp
import json
import os
import requests
import shutil
import subprocess
import time

import autogen
import cache
import problem
import team
import user
import utils

blueprint = Blueprint("programming", __name__)

JUDGE_URL = os.getenv("JUDGE_URL", None)
JUDGE_APIKEY = os.getenv("JUDGE_APIKEY", None)

@blueprint.route("/submissions/delete", methods=["POST"])
@api_wrapper
@login_required
@team_required
def delete_submission():
	params = utils.flat_multi(request.form)
	psid = params.get("psid")
	tid = session.get("tid")
	result = ProgrammingSubmissions.query.filter_by(psid=psid, tid=tid)

	if result.first() is None:
		raise WebException("Submission does not exist.")

	with app.app_context():
		result.delete()
		db.session.commit()
		db.session.close()

	return { "success": 1, "message": "Success!" }

@blueprint.route("/submissions", methods=["GET"])
@api_wrapper
@login_required
@team_required
def get_submissions():
	submissions_return = []
	tid = session.get("tid")
	submissions = ProgrammingSubmissions.query.filter_by(tid=tid).order_by(ProgrammingSubmissions.psid.desc()).all()
	for submission in submissions:
		pass
	return { "success": 1, "submissions": submissions_return }

@blueprint.route("/problems", methods=["GET"])
@api_wrapper
@login_required
def get_problems():
	if session.get("admin"):
		pass
	elif session.get("tid") <= 0:
		raise WebException("You need a team.")
	elif team.get_team(tid=session.get("tid")).first().finalized != True:
		raise WebException("Your team is not finalized.")

	data = []
	problems = Problems.query.filter_by(category="Programming").all()
	if problems is not None:
		for _problem in problems:
			data.append({
				"title": _problem.title,
				"pid": _problem.pid,
				"value": _problem.value
			})
	return { "success": 1, "problems": data }

@blueprint.route("/submit", methods=["POST"])
@api_wrapper
@login_required
@team_required
def submit_program():
	if JUDGE_URL is None or JUDGE_APIKEY is None:
		raise WebException("Judge API key missing.")
	params = utils.flat_multi(request.form)

	pid = params.get("pid")
	_user = user.get_user().first()
	language = params.get("language")
	submission_contents = params.get("submission")

	r = requests.post(JUDGE_URL + "/jobs", data={
		"problem_id": 1337,
		"language": language,
		"code": submission_contents
	}, headers = { "api_key": JUDGE_APIKEY })
	if r.status_code != 201:
		raise WebException("Invalid response from judge. %s" % r.raw)

	data = json.loads(r.text)
	jid = data["id"]

	submission = ProgrammingSubmissions(pid, _user.uid, _user.tid, jid, language)
	with app.app_context():
		db.session.add(submission)
		db.session.commit()
		db.session.close()

	return { "success": 1, "message": "Submitted!" }

def get_submission(jid):
	submission = ProgrammingSubmissions.query.filter_by(jid=jid)
	if submission is None:
		return None
	obj = {
		"jid": submission.jid,
		"pid": submission.pid,
	}
	if submission.verdict == "waiting":
		# send post request
		r = requests.post(JUDGE_URL + "/api/", data={
			
		}, headers = { "api_key": JUDGE_APIKEY })
	else:
		obj["verdict"] = submission.verdict
		if obj["verdict"] == "accepted":
			random = autogen.get_random(submission.pid, submission.tid)
			obj["token"] = utils.generate_string()
		obj["language"] = submission.language
		obj["started"] = submission.creation_time
		obj["execution_time"] = submission.execution_time

	return obj

def judge(submission_path, language, pid):
	if not os.path.exists(submission_path):
		raise WebException("Program is missing.")

	_problem = problem.get_problem(pid=pid).first()
	if _problem is None:
		raise WebException("Problem does not exist.")

	submission_root = os.path.dirname(submission_path)
	os.chdir(submission_root)
	log = ""
	message = ""

	log += "Compiling...\n"
	start_time = time.time()
	try:
		if language == "python2":
			subprocess.check_output("python -m py_compile %s" % submission_path, shell=True)
		elif language == "python3":
			subprocess.check_output("python3 -m py_compile %s" % submission_path, shell=True)
		elif language == "java":
			subprocess.check_output("javac %s" % submission_path, shell=True)
		else:
			message = "Not implemented."
			return message, log, time.time() - start_time
	except subprocess.CalledProcessError as e:
		# TODO: Extract useful error messages from exceptions and add timeout
		#log += "There was a problem with compiling.\n%s\n" % str(e)
		message = "There was a problem with compiling."

		return message, log, time.time() - start_time

	log += "Compiled.\n"

	try:
		judge = imp.load_source("judge", _problem.grader)
	except Exception, e:
		message = "An error occured. Please notify an admin immediately."
		log += "Could not load judge.\n"
		return message, log, time.time() - start_time

	for i in range(1, judge.TEST_COUNT + 1):
		log += "Running test #%s\n" % i

		try:
			_input, correct = judge.generate()
		except Exception, e:
			message = "An error occured. Please notify an admin immediately."
			log += "Could not generate input for test #%s.\n" % i
			return message, log, time.time() - start_time

		try:
			command = ""
			if language == "python2":
				command = "python %s <<< \"%s\"" % (submission_path, _input)
			elif language == "python3":
				command = "python3 %s <<< \"%s\"" % (submission_path, _input)
			elif language == "java":
				command = "java program <<< \"%s\"" % _input
			output = subprocess.check_output(command, shell=True, executable="/bin/bash").strip()
		except subprocess.CalledProcessError as e:
			#log += "Program threw an exception:\n%s\n" % str(e)
			message = "Program crashed."
			return message, log, time.time() - start_time

		if correct != output:
			message = "Incorrect."
			log += "Test #%s failed.\n\n" % i
			log += "Input:\n%s\n\n" % _input
			log += "Output:\n%s\n\n" % output
			log += "Expected:\n%s\n\n" % correct
			return message, log, time.time() - start_time
		else:
			log += "Test #%s passed!\n" % i

	message = "Correct!"
	log += "All tests passed."

	return message, log, time.time() - start_time

def validate_judge(judge_contents):
	return
	tmp_judge = "/tmp/judge.py"

	open(tmp_judge, "w").write(judge_contents)

	try:
		judge = imp.load_source("judge", tmp_judge)
	except Exception, e:
		raise WebException("There is a syntax error in the judge: %s" % e)

	try:
		assert hasattr(judge, "TEST_COUNT"), "Judge missing TEST_COUNT."

		assert type(judge.TEST_COUNT) == int, "TEST_COUNT must be an integer."

		_input, correct = judge.generate()

		assert _input is not None, "Judge did not generate valid input."
		assert correct is not None, "Judge did not generate a valid response."
	except AssertionError, e:
		raise WebException(e)
	except Exception, e:
		raise WebException(e)
