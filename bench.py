#coding=utf-8
from  __future__ import print_function
from random import choices
from matplotlib import pyplot as plt
# import rados, sys

class BaseBench():
	def __init__(self, obj_num=10000, access_max=-1, pending_max=100):
		self.total_access = 0
		self.hit_access = 0
		self.pending_access = 0
		self.obj_num = obj_num
		self.access_max = access_max
		self.pending_max = pending_max

	def __str__(self):
		return ("total access: {0}, hit access: {1}, pending access: {2}, object num: {3}, " +\
			"access max: {4}, pending max: {5} ").format(self.total_access, self.hit_access,
			self.pending_access, self.obj_num, self.access_max, self.pending_max
			)

	def __repr__(self):
		return str(self)

	def generate(self):
		weights = [1] * self.obj_num
		return choices(range(self.obj_num), weights=weights, k=self.access_max)

class RWBench(BaseBench):
	def __init__(self, obj_num=10000, access_max=-1, pending_max=100, write_ratio=1.0):
		super().__init__(obj_num, access_max, pending_max)
		self.write_ratio_expect = write_ratio
		self.write_counter = 0

	def __str__(self):
		return super().__str__() + "write ratio expect: {0}, write counter: {1}".format(
			self.write_ratio_expect, self.write_counter)

	def __repr__(self):
		return str(self)

	def generate(self):
		base = super().generate()
		rw = choices([True, False], weights=[self.write_ratio_expect, 1-self.write_ratio_expect], k=self.access_max)
		access_rw = zip(base, rw)
		# Turn read to write if object not exists
		writed = []
		for index, p in enumerate(access_rw):
			if not p[1] and p[0] not in writed:
				writed.append(p[0])
				yield (p[0], True)
			else:
				yield p

class UnbanlanceBench(BaseBench):
	def __init__(self, obj_num=10000, access_max=-1, pending_max=100, slop=0.8, groups=10):
		super().__init__(obj_num, access_max, pending_max)
		self.slop = slop
		self.groups = groups

	def generate(self):
		ival = (self.access_max/self.groups) * (1-self.slop) / (1-self.slop**self.groups)
		weights = []
		for i in range(self.groups):
			weights.extend([ival]*(self.obj_num // self.groups))
			ival *= self.slop
		base = choices(range(self.obj_num), weights=weights, k=self.access_max)
		return base


def show_dist(nums):
	plt.hist(nums)
	plt.show()

def calc_avg(num_ratio, access_ratio, obj_num, access_num):
	number = obj_num * num_ratio
	avg_access = access_num * access_ratio / number
	rest_avg_access = access_num * (1-access_ratio) / (obj_num-number)

	return (avg_access, rest_avg_access)


def main():
	a  = UnbanlanceBench(1000, 100000)
	b = a.generate()
	# h = list(zip(*b))[1]
	show_dist(b)
	# print(list(b))

if __name__ == '__main__':
	main()