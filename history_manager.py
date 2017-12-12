import json
import os
import util


class History(object):
	def __init__(self, history_file):
		self.filename = history_file
		self.wines = util.read_json(history_file)

	def length(self):
		return len(self.wines)

	def add_wine(self, true_index, cluster_scores, feedback):
		new_wine = {}
		new_wine['true_index'] = true_index
		new_wine['cluster_scores'] = cluster_scores
		new_wine['user_feedback'] = feedback
		self.wines.append(new_wine)
		print(new_wine)

	def save_state(self):
		with open(self.filename, 'w+') as f:
			json.dump(self.wines, f, indent=4)

	def get_history(self):
		return self.wines