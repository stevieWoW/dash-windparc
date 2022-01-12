import logging
import datetime


class DashPerformance:
	# Declare some global Variables
	PERF_DATA = DATA = WINDMILL = PREP_DATA = AGGR = None

	def __init__(self,perf_data,windmill):
		'''
			#
		'''
		self.PERF_DATA = perf_data
		self.WINDMILL = windmill


	
	def check_box_year_month(self,year:list,month:list,windmill=False,aggr='MONTH'):
		'''
			#
		'''
		data = self.PERF_DATA.loc[(self.PERF_DATA['YEAR'] >= year[0]) & (self.PERF_DATA['YEAR'] <= year[1])]
		data = data.loc[(data['MONTH'] >= month[0]) & (data['MONTH'] <= month[1])]
		self.DATA = data
		self.AGGR = aggr
		self.prepare_data(windmill)


	def check_box_year(self,year:list,month:list,windmill=False,aggr='MONTH'):
		'''
			#
		'''
		data = self.PERF_DATA.loc[(self.PERF_DATA['YEAR'] >= year[0]) & (self.PERF_DATA['YEAR'] <= year[1])]
		self.DATA = data
		self.AGGR = aggr
		self.prepare_data(windmill)


	def check_box_month(self,year:list,month:list,windmill=False,aggr='MONTH'):
		'''
			#
		'''
		data = self.PERF_DATA.loc[(self.PERF_DATA['MONTH'] >= month[0]) & (self.PERF_DATA['MONTH'] <= month[1])]
		self.DATA = data
		self.AGGR = aggr
		self.prepare_data(windmill)


	def prepare_data(self,windmill):
		'''
			#
		'''
		if windmill:
			data = self.DATA[self.DATA['WINDMILL_ID'].isin(windmill)]
			self.DATA = data

		data = self.DATA.groupby([self.AGGR], as_index=False).sum()
		if self.AGGR == 'WINDMILL_ID':
			data = data[[self.AGGR,'ISPERFORMANCE','PLANPERFORMANCE']]
		elif self.AGGR != 'WINDMILL_ID':
			data = data[[self.AGGR,'ISPERFORMANCE','PLANPERFORMANCE','WINDMILL_ID']]

		self.PREP_DATA = data
	
	@property
	def pie_chart(self):
		'''
			get numbers for PIE Chart
		'''
		
		data = self.DATA.merge(self.WINDMILL.set_index('WINDMILL_ID'), on='WINDMILL_ID')
		data = data[['WINDMILL_ID','TYPE']].drop_duplicates(subset=['WINDMILL_ID'])

		data = data.groupby(['TYPE'], as_index=True)['WINDMILL_ID'].count()
		
		return data.reset_index(level=0)

	@property
	def perf_bar(self):
		'''
			get numbers for Performance Bar
		'''
		data = self.PREP_DATA[['ISPERFORMANCE','PLANPERFORMANCE', self.AGGR]]
		return data 
		

	@property
	def perf_gauge(self):
		'''
			get numbers for Performance Gauge
		'''

		data_gauge = self.DATA[['ISPERFORMANCE','PLANPERFORMANCE']].loc[self.DATA['ISPERFORMANCE'] != 0 ].sum()
		
		return (data_gauge.ISPERFORMANCE / data_gauge.PLANPERFORMANCE) * 100

	@property
	def perf_median(self):
		'''
			get numbers for Median
		'''

		#print(self.DATA)
		#1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 17 17 18 19 20 21 22 23 24
		data = self.DATA.groupby([self.AGGR], as_index=False).mean()
		#print(data)
		#print(data.describe()[['ISPERFORMANCE','PLANPERFORMANCE']])
		return data

	@property
	def perf_prediction(self):
		pred_range = self.DATA.groupby(['MONTH','YEAR'], as_index=False).sum()
		pred_range = pred_range.loc[pred_range['ISPERFORMANCE'] == 0 ]['YEAR']
		pred_range = pred_range.drop_duplicates()
		pred_range = pred_range.to_list()
		print(pred_range)

		#print(self.PERF_DATA)
		data = self.PERF_DATA[~self.PERF_DATA['YEAR'].isin(pred_range)]
		data = data.groupby([self.AGGR], as_index=False)[[self.AGGR,'ISPERFORMANCE']].mean()
		print(self.PREP_DATA)
		data['PRED'] = self.PREP_DATA['ISPERFORMANCE'] + data['ISPERFORMANCE']
		print(data)
		return data
