'''
Copyright (C)
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)#fulltext. 

For license issues, please contact:

Dr. Bing Ye
Life Sciences Institute
University of Michigan
210 Washtenaw Avenue, Room 5403
Ann Arbor, MI 48109-2216
USA

Email: bingye@umich.edu
'''



import wx
import os
import matplotlib as mpl
from pathlib import Path
import pandas as pd
import torch
from .analyzebehaviors import AnalyzeAnimal
from .tools import plot_evnets
from collections import OrderedDict



the_absolute_current_path=str(Path(__file__).resolve().parent)



class ColorPicker(wx.Dialog):

	def __init__(self,parent,title,name_and_color):

		super(ColorPicker,self).__init__(parent=None,title=title,size=(200,200))

		self.name_and_color=name_and_color
		name=self.name_and_color[0]
		hex_color=self.name_and_color[1][1].lstrip('#')
		color=tuple(int(hex_color[i:i+2],16) for i in (0,2,4))

		boxsizer=wx.BoxSizer(wx.VERTICAL)

		self.color_picker=wx.ColourPickerCtrl(self,colour=color)

		button=wx.Button(self,wx.ID_OK,label='Apply')

		boxsizer.Add(0,10,0)
		boxsizer.Add(self.color_picker,0,wx.ALL|wx.CENTER,10)
		boxsizer.Add(button,0,wx.ALL|wx.CENTER,10)
		boxsizer.Add(0,10,0)

		self.SetSizer(boxsizer)



class WindowLv1_AnalyzeBehaviors(wx.Frame):

	def __init__(self,title):

		super(WindowLv1_AnalyzeBehaviors,self).__init__(parent=None,title=title,size=(1000,530))
		self.use_detector=False
		self.detector_path=None
		self.path_to_detector=None
		self.detector_batch=1
		# if not None, will load background images from path
		self.background_path=None
		# the parent path of the Categorizers
		self.model_path=None
		self.path_to_categorizer=None
		self.path_to_videos=None
		self.result_path=None
		self.framewidth=None
		self.delta=10000
		self.decode_animalnumber=False
		self.animal_number=1
		self.relink=False
		self.autofind_t=False
		self.decode_t=False
		self.t=0
		self.duration=0
		self.decode_extraction=False
		self.ex_start=0
		self.ex_end=None
		self.behaviornames_and_colors=OrderedDict()
		self.dim_tconv=8
		self.dim_conv=8
		self.channel=1
		self.length=15
		# 0: animals birghter than the background; 1: animals darker than the background; 2: hard to tell
		self.animal_vs_bg=0
		self.stable_illumination=True
		self.animation_analyzer=True
		# behaviors for annotation and plots
		self.behavior_to_annotate=['all']
		self.parameter_to_analyze=[]
		self.include_bodyparts=False
		self.std=0
		self.uncertain=0
		self.show_legend=True
		self.background_free=True
		# whether to normalize the distance (in pixel) to the animal contour area
		self.normalize_distance=True

		self.dispaly_window()


	def dispaly_window(self):

		panel=wx.Panel(self)
		boxsizer=wx.BoxSizer(wx.VERTICAL)

		module_selectcategorizer=wx.BoxSizer(wx.HORIZONTAL)
		button_selectcategorizer=wx.Button(panel,label='Select a Categorizer for\nbehavior classification',size=(300,40))
		button_selectcategorizer.Bind(wx.EVT_BUTTON,self.select_categorizer)
		self.text_selectcategorizer=wx.StaticText(panel,label='The fps of the videos to analyze should match that of the selected Categorizer.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_selectcategorizer.Add(button_selectcategorizer,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_selectcategorizer.Add(self.text_selectcategorizer,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,10,0)
		boxsizer.Add(module_selectcategorizer,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_inputvideos=wx.BoxSizer(wx.HORIZONTAL)
		button_inputvideos=wx.Button(panel,label='Select the video(s)\nfor behavior analysis',size=(300,40))
		button_inputvideos.Bind(wx.EVT_BUTTON,self.select_videos)
		self.text_inputvideos=wx.StaticText(panel,label='Can select multiple videos for an analysis batch (one raster plot for one batch).',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_inputvideos.Add(button_inputvideos,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_inputvideos.Add(self.text_inputvideos,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_inputvideos,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_outputfolder=wx.BoxSizer(wx.HORIZONTAL)
		button_outputfolder=wx.Button(panel,label='Select a folder to store\nthe analysis results',size=(300,40))
		button_outputfolder.Bind(wx.EVT_BUTTON,self.select_outpath)
		self.text_outputfolder=wx.StaticText(panel,label='Will create a subfolder for each video under this folder.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_outputfolder.Add(button_outputfolder,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_outputfolder.Add(self.text_outputfolder,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_outputfolder,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_startanalyze=wx.BoxSizer(wx.HORIZONTAL)
		button_startanalyze=wx.Button(panel,label='Specify when the analysis\nshould begin (unit: second)',size=(300,40))
		button_startanalyze.Bind(wx.EVT_BUTTON,self.specify_timing)
		self.text_startanalyze=wx.StaticText(panel,label='Default: at the beginning of the video(s).',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_startanalyze.Add(button_startanalyze,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_startanalyze.Add(self.text_startanalyze,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_startanalyze,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_duration=wx.BoxSizer(wx.HORIZONTAL)
		button_duration=wx.Button(panel,label='Specify the analysis duration\n(unit: second)',size=(300,40))
		button_duration.Bind(wx.EVT_BUTTON,self.input_duration)
		self.text_duration=wx.StaticText(panel,label='Default: from the specified beginning time to the end of a video.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_duration.Add(button_duration,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_duration.Add(self.text_duration,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_duration,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_animalnumber=wx.BoxSizer(wx.HORIZONTAL)
		button_animalnumber=wx.Button(panel,label='Specify the number of animals\nin a video',size=(300,40))
		button_animalnumber.Bind(wx.EVT_BUTTON,self.specify_animalnumber)
		self.text_animalnumber=wx.StaticText(panel,label='Default: 1.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_animalnumber.Add(button_animalnumber,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_animalnumber.Add(self.text_animalnumber,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_animalnumber,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_detection=wx.BoxSizer(wx.HORIZONTAL)
		button_detection=wx.Button(panel,label='Specify the method to\ndetect animals or objects',size=(300,40))
		button_detection.Bind(wx.EVT_BUTTON,self.select_method)
		self.text_detection=wx.StaticText(panel,label='Background subtraction (default): faster but needs static background; Detectors: versatile but slow.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_detection.Add(button_detection,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_detection.Add(self.text_detection,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_detection,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_selectbehaviors=wx.BoxSizer(wx.HORIZONTAL)
		button_selectbehaviors=wx.Button(panel,label='Select the behaviors for\nannotations and plots',size=(300,40))
		button_selectbehaviors.Bind(wx.EVT_BUTTON,self.select_behaviors)
		self.text_selectbehaviors=wx.StaticText(panel,label='Default: all the behaviors listed in the selected Categorizer.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_selectbehaviors.Add(button_selectbehaviors,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_selectbehaviors.Add(self.text_selectbehaviors,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_selectbehaviors,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_selectparameters=wx.BoxSizer(wx.HORIZONTAL)
		button_selectparameters=wx.Button(panel,label='Select the quantitative measurements\nfor each behavior',size=(300,40))
		button_selectparameters.Bind(wx.EVT_BUTTON,self.select_parameters)
		self.text_selectparameters=wx.StaticText(panel,label='Default: none.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_selectparameters.Add(button_selectparameters,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_selectparameters.Add(self.text_selectparameters,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_selectparameters,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		button_analyze=wx.Button(panel,label='Start to analyze the behaviors',size=(300,40))
		button_analyze.Bind(wx.EVT_BUTTON,self.analyze_behaviors)
		boxsizer.Add(0,5,0)
		boxsizer.Add(button_analyze,0,wx.RIGHT|wx.ALIGN_RIGHT,90)
		boxsizer.Add(0,10,0)

		panel.SetSizer(boxsizer)

		self.Centre()
		self.Show(True)


	def select_categorizer(self,event):

		if self.model_path is None:
			self.model_path=os.path.join(the_absolute_current_path,'models')

		categorizers=[i for i in os.listdir(self.model_path) if os.path.isdir(os.path.join(self.model_path,i))]
		if '__pycache__' in categorizers:
			categorizers.remove('__pycache__')
		if '__init__' in categorizers:
			categorizers.remove('__init__')
		if '__init__.py' in categorizers:
			categorizers.remove('__init__.py')
		categorizers.sort()
		if 'No behavior classification, just track animals and quantify motion kinematics' not in categorizers:
			categorizers.append('No behavior classification, just track animals and quantify motion kinematics')
		if 'Choose a new directory of the Categorizer' not in categorizers:
			categorizers.append('Choose a new directory of the Categorizer')

		dialog=wx.SingleChoiceDialog(self,message='Select a Categorizer for behavior classification',caption='Select a Categorizer',choices=categorizers)

		if dialog.ShowModal()==wx.ID_OK:
			categorizer=dialog.GetStringSelection()
			if categorizer=='Choose a new directory of the Categorizer':
				dialog1=wx.DirDialog(self,'Select a directory','',style=wx.DD_DEFAULT_STYLE)
				if dialog1.ShowModal()==wx.ID_OK:
					self.path_to_categorizer=dialog1.GetPaths()
				dialog1.Destroy()
				dialog1=wx.NumberEntryDialog(self,"Enter the Categorizer's uncertainty level (0~100%)","If probability difference between\n1st- and 2nd-likely behaviors\nis less than uncertainty,\nclassfication outputs an 'NA'.",'Uncertainty level',0,0,100)
				if dialog1.ShowModal()==wx.ID_OK:
					uncertain=dialog1.GetValue()
					self.uncertain=uncertain/100
				dialog1.Destroy()
				self.text_selectcategorizer.SetLabel('The path to the Categorizer is: '+self.path_to_categorizer+' with uncertainty of '+str(uncertain)+'%.')
			elif categorizer=='No behavior classification, just track animals and quantify motion kinematics':
				self.path_to_categorizer=None
				dialog1=wx.NumberEntryDialog(self,'Specify a time window used for measuring\nmotion kinematics of tracked animals','Enter the number of\nframes (minimum=3):','Time window for calculating kinematics',15,1,100000000000000)
				if dialog1.ShowModal()==wx.ID_OK:
					self.length=int(dialog1.GetValue())
					if self.length<3:
						self.length=3
				dialog1.Destroy()
				self.text_selectcategorizer.SetLabel('No behavior classification; the time window to measure kinematics of tracked animals is: '+str(self.length)+' frames.')
				self.text_selectbehaviors.SetLabel('No behavior classification. Just track animals and quantify motion kinematics.')
			else:
				self.path_to_categorizer=os.path.join(self.model_path,categorizer)
				dialog1=wx.NumberEntryDialog(self,"Enter the Categorizer's uncertainty level (0~100%)","If probability difference between\n1st- and 2nd-likely behaviors\nis less than uncertainty,\nclassfication outputs an 'NA'.",'Uncertainty level',0,0,100)
				if dialog1.ShowModal()==wx.ID_OK:
					uncertain=dialog1.GetValue()
					self.uncertain=uncertain/100
					self.text_selectcategorizer.SetLabel('Categorizer: '+categorizer+' with uncertainty of '+str(uncertain)+'%.')	

			if self.path_to_categorizer is not None:

				parameters=pd.read_csv(os.path.join(self.path_to_categorizer,'model_parameters.txt'))
				complete_colors=list(mpl.colors.cnames.values())
				colors=[]
				for c in complete_colors:
					colors.append(['#ffffff',c])
				self.behaviornames_and_colors=OrderedDict()

				for behavior_name in list(parameters['classnames']):
					index=list(parameters['classnames']).index(behavior_name)
					if index<len(colors):
						self.behaviornames_and_colors[behavior_name]=colors[index]
					else:
						self.behaviornames_and_colors[behavior_name]=['#ffffff','#ffffff']

				if 'dim_conv' in list(parameters.keys()):
					self.dim_conv=int(parameters['dim_conv'][0])
				if 'dim_tconv' in list(parameters.keys()):
					self.dim_tconv=int(parameters['dim_tconv'][0])
				self.channel=int(parameters['channel'][0])
				self.length=int(parameters['time_step'][0])
				if self.length<3:
					self.length=3
				categorizer_type=int(parameters['network'][0])
				if categorizer_type==2:
					self.animation_analyzer=True
				else:
					self.animation_analyzer=False
				if int(parameters['inner_code'][0])==0:
					self.include_bodyparts=True
				else:
					self.include_bodyparts=False
				self.std=int(parameters['std'][0])
				if int(parameters['background_free'][0])==0:
					self.background_free=True
				else:
					self.background_free=False

		dialog.Destroy()


	def select_videos(self,event):

		wildcard='Video files(*.avi;*.mpg;*.mpeg;*.wmv;*.mp4;*.mkv;*.m4v;*.mov)|*.avi;*.mpg;*.mpeg;*.wmv;*.mp4;*.mkv;*.m4v;*.mov'
		dialog=wx.FileDialog(self,'Select video(s)','','',wildcard,style=wx.FD_MULTIPLE)

		if dialog.ShowModal()==wx.ID_OK:
			self.path_to_videos=dialog.GetPaths()
			self.path_to_videos.sort()
			path=os.path.dirname(self.path_to_videos[0])
			dialog2=wx.MessageDialog(self,'Proportional resize the video frames?\nSelect "No" if dont know what it is.','(Optional) resize the frames?',wx.YES_NO|wx.ICON_QUESTION)
			if dialog2.ShowModal()==wx.ID_YES:
				dialog3=wx.NumberEntryDialog(self,'Enter the desired frame width','The unit is pixel:','Desired frame width',1000,1,10000)
				if dialog3.ShowModal()==wx.ID_OK:
					self.framewidth=int(dialog3.GetValue())
					if self.framewidth<10:
						self.framewidth=10
					self.text_inputvideos.SetLabel('Selected '+str(len(self.path_to_videos))+' video(s) in: '+path+' (proportionally resize framewidth to '+str(self.framewidth)+').')
				else:
					self.framewidth=None
					self.text_inputvideos.SetLabel('Selected '+str(len(self.path_to_videos))+' video(s) in: '+path+' (original framesize).')
				dialog3.Destroy()
			else:
				self.framewidth=None
				self.text_inputvideos.SetLabel('Selected '+str(len(self.path_to_videos))+' video(s) in: '+path+' (original framesize).')
			dialog2.Destroy()

		dialog.Destroy()


	def select_outpath(self,event):

		dialog=wx.DirDialog(self,'Select a directory','',style=wx.DD_DEFAULT_STYLE)
		if dialog.ShowModal()==wx.ID_OK:
			self.result_path=dialog.GetPath()
			self.text_outputfolder.SetLabel('Results will be in: '+self.result_path+'.')
		dialog.Destroy()


	def specify_timing(self,event):

		dialog=wx.MessageDialog(self,'light on and off in videos?','Illumination shifts?',wx.YES_NO|wx.ICON_QUESTION)
		if dialog.ShowModal()==wx.ID_YES:
			self.delta=1.2
		else:
			self.delta=10000
		dialog.Destroy()

		if self.delta==1.2:
			methods=['Automatic (for light on and off)','Decode from filenames: "_bt_"','Enter a time point']
		else:
			methods=['Decode from filenames: "_bt_"','Enter a time point']

		dialog=wx.SingleChoiceDialog(self,message='Specify beginning time of analysis',caption='Beginning time of analysis',choices=methods)
		if dialog.ShowModal()==wx.ID_OK:
			method=dialog.GetStringSelection()
			if method=='Automatic (for light on and off)':
				self.autofind_t=True
				self.decode_t=False
				self.text_startanalyze.SetLabel('Automatically find the onset of the 1st time when light on / off as the beginning time.')
			elif method=='Decode from filenames: "_bt_"':
				self.autofind_t=False
				self.decode_t=True
				self.text_startanalyze.SetLabel('Decode the beginning time from the filenames: the "t" immediately after the letter "b"" in "_bt_".')
			else:
				self.autofind_t=False
				self.decode_t=False
				dialog2=wx.NumberEntryDialog(self,'Enter the beginning time of analysis','The unit is second:','Beginning time of analysis',0,0,100000000000000)
				if dialog2.ShowModal()==wx.ID_OK:
					self.t=float(dialog2.GetValue())
					if self.t<0:
						self.t=0
					self.text_startanalyze.SetLabel('Analysis will begin at the: '+str(self.t)+' second.')
				dialog2.Destroy()
		dialog.Destroy()


	def input_duration(self,event):

		dialog=wx.NumberEntryDialog(self,'Enter the duration of the analysis','The unit is second:','Analysis duration',0,0,100000000000000)
		if dialog.ShowModal()==wx.ID_OK:
			self.duration=int(dialog.GetValue())
			if self.duration!=0:
				self.text_duration.SetLabel('The analysis duration is '+str(self.duration)+' seconds.')
			else:
				self.text_duration.SetLabel('The analysis duration is from the specified beginning time to the end of a video.')
		dialog.Destroy()


	def specify_animalnumber(self,event):

		methods=['Decode from filenames: "_nn_"','Enter the number of animals']
		dialog=wx.SingleChoiceDialog(self,message='Enter the number of animals in a video',caption='The number of animals in a video',choices=methods)
		if dialog.ShowModal()==wx.ID_OK:
			method=dialog.GetStringSelection()
			if method=='Enter the number of animals':
				dialog2=wx.NumberEntryDialog(self,'','The number of animals:','Animal number',1,1,100)
				if dialog2.ShowModal()==wx.ID_OK:
					self.decode_animalnumber=False
					self.animal_number=int(dialog2.GetValue())
					self.text_animalnumber.SetLabel('The total number of animals in a video is '+str(self.animal_number)+'.')
				dialog2.Destroy()
			else:
				self.decode_animalnumber=True
				self.text_animalnumber.SetLabel('Decode from the filenames: the "n" immediately after the letter "n" in _"nn"_.')
		dialog.Destroy()

		if self.animal_number>1 or self.decode_animalnumber is True:
			dialog=wx.MessageDialog(self,'Allow to relink the reappeared animals\nto the IDs that are lost track?','Relink IDs?',wx.YES_NO|wx.ICON_QUESTION)
			if dialog.ShowModal()==wx.ID_YES:
				self.relink=True
				if self.decode_animalnumber is True:
					self.text_animalnumber.SetLabel('Decode from the filenames: the "n" immediately after the letter "n" in _"nn"_; allow relink IDs.')
				else:
					self.text_animalnumber.SetLabel('The total number of animals in a video is '+str(self.animal_number)+'; allow relink IDs.')
			else:
				self.relink=False
				if self.decode_animalnumber is True:
					self.text_animalnumber.SetLabel('Decode from the filenames: the "n" immediately after the letter "n" in _"nn"_; NOT allow relink IDs.')
				else:
					self.text_animalnumber.SetLabel('The total number of animals in a video is '+str(self.animal_number)+'; NOT allow relink IDs.')
			dialog.Destroy()


	def select_method(self,event):

		methods=['Subtract background (much faster but requires static background & stable illumination)','Use trained Detectors (versatile, good for social behaviors but much slower)']
		dialog=wx.SingleChoiceDialog(self,message='How to detect the animals?',caption='Detection methods',choices=methods)

		if dialog.ShowModal()==wx.ID_OK:
			method=dialog.GetStringSelection()

			if method=='Subtract background (much faster but requires static background & stable illumination)':

				self.use_detector=False

				contrasts=['Animal brighter than background','Animal darker than background','Hard to tell']
				dialog1=wx.SingleChoiceDialog(self,message='Select the scenario that fits your experiments best',caption='Which fits best?',choices=contrasts)

				if dialog1.ShowModal()==wx.ID_OK:
					contrast=dialog1.GetStringSelection()
					if contrast=='Animal brighter than background':
						self.animal_vs_bg=0
						self.text_detection.SetLabel('Background subtraction: animal brighter than background.')
					elif contrast=='Animal darker than background':
						self.animal_vs_bg=1
						self.text_detection.SetLabel('Background subtraction: animal darker than background.')
					else:
						self.animal_vs_bg=2
						self.text_detection.SetLabel('Background subtraction: animal partially brighter/darker than background.')
					dialog2=wx.MessageDialog(self,'Load an existing background from a folder?\nSelect "No" if dont know what it is.','(Optional) load existing background?',wx.YES_NO|wx.ICON_QUESTION)
					if dialog2.ShowModal()==wx.ID_YES:
						dialog3=wx.DirDialog(self,'Select a directory','',style=wx.DD_DEFAULT_STYLE)
						if dialog3.ShowModal()==wx.ID_OK:
							self.background_path=dialog3.GetPath()
						dialog3.Destroy()
					else:
						self.background_path=None
						if self.animal_vs_bg!=2:
							dialog3=wx.MessageDialog(self,'Unstable illumination in the video?\nSelect "Yes" if dont know what it is.','(Optional) unstable illumination?',wx.YES_NO|wx.ICON_QUESTION)
							if dialog3.ShowModal()==wx.ID_YES:
								self.stable_illumination=False
							else:
								self.stable_illumination=True
							dialog3.Destroy()
					dialog2.Destroy()

					if self.background_path is None:
						ex_methods=['Use the entire duration (default but NOT recommended)','Decode from filenames: "_xst_" and "_xet_"','Enter two time points']
						dialog2=wx.SingleChoiceDialog(self,message='Specify the time window for background extraction',caption='Time window for background extraction',choices=ex_methods)
						if dialog2.ShowModal()==wx.ID_OK:
							ex_method=dialog2.GetStringSelection()
							if ex_method=='Use the entire duration (default but NOT recommended)':
								self.decode_extraction=False
								if self.animal_vs_bg==0:
									self.text_detection.SetLabel('Background subtraction: animal brighter, using the entire duration.')
								elif self.animal_vs_bg==1:
									self.text_detection.SetLabel('Background subtraction: animal darker, using the entire duration.')
								else:
									self.text_detection.SetLabel('Background subtraction: animal partially brighter/darker, using the entire duration.')
							elif ex_method=='Decode from filenames: "_xst_" and "_xet_"':
								self.decode_extraction=True
								if self.animal_vs_bg==0:
									self.text_detection.SetLabel('Background subtraction: animal brighter, using time window decoded from filenames "_xst_" and "_xet_".')
								elif self.animal_vs_bg==1:
									self.text_detection.SetLabel('Background subtraction: animal darker, using time window decoded from filenames "_xst_" and "_xet_".')
								else:
									self.text_detection.SetLabel('Background subtraction: animal partially brighter/darker, using time window decoded from filenames "_xst_" and "_xet_".')
							else:
								self.decode_extraction=False
								dialog3=wx.NumberEntryDialog(self,'Enter the start time','The unit is second:','Start time for background extraction',0,0,100000000000000)
								if dialog3.ShowModal()==wx.ID_OK:
									self.ex_start=int(dialog3.GetValue())
								dialog3.Destroy()
								dialog3=wx.NumberEntryDialog(self,'Enter the end time','The unit is second:','End time for background extraction',0,0,100000000000000)
								if dialog3.ShowModal()==wx.ID_OK:
									self.ex_end=int(dialog3.GetValue())
									if self.ex_end==0:
										self.ex_end=None
								dialog3.Destroy()
								if self.animal_vs_bg==0:
									if self.ex_end is None:
										self.text_detection.SetLabel('Background subtraction: animal brighter, using time window (in seconds) from '+str(self.ex_start)+' to the end.')
									else:
										self.text_detection.SetLabel('Background subtraction: animal brighter, using time window (in seconds) from '+str(self.ex_start)+' to '+str(self.ex_end)+'.')
								elif self.animal_vs_bg==1:
									if self.ex_end is None:
										self.text_detection.SetLabel('Background subtraction: animal darker, using time window (in seconds) from '+str(self.ex_start)+' to the end.')
									else:
										self.text_detection.SetLabel('Background subtraction: animal darker, using time window (in seconds) from '+str(self.ex_start)+' to '+str(self.ex_end)+'.')
								else:
									if self.ex_end is None:
										self.text_detection.SetLabel('Background subtraction: animal partially brighter/darker, using time window (in seconds) from '+str(self.ex_start)+' to the end.')
									else:
										self.text_detection.SetLabel('Background subtraction: animal partially brighter/darker, using time window (in seconds) from '+str(self.ex_start)+' to '+str(self.ex_end)+'.')
						dialog2.Destroy()

				dialog1.Destroy()

			else:

				self.use_detector=True

				if self.detector_path is None:
					self.detector_path=os.path.join(the_absolute_current_path,'detectors')

				detectors=[i for i in os.listdir(self.detector_path) if os.path.isdir(os.path.join(self.detector_path,i))]
				if '__pycache__' in detectors:
					detectors.remove('__pycache__')
				if '__init__' in detectors:
					detectors.remove('__init__')
				if '__init__.py' in detectors:
					detectors.remove('__init__.py')
				detectors.sort()
				if 'Choose a new directory of the Detector' not in detectors:
					detectors.append('Choose a new directory of the Detector')

				dialog1=wx.SingleChoiceDialog(self,message='Select a Detector for animal detection',caption='Select a Detector',choices=detectors)

				if dialog1.ShowModal()==wx.ID_OK:
					detector=dialog1.GetStringSelection()
					if detector=='Choose a new directory of the Detector':
						dialog2=wx.DirDialog(self,'Select a directory','',style=wx.DD_DEFAULT_STYLE)
						if dialog2.ShowModal()==wx.ID_OK:
							self.path_to_detector=dialog2.GetPaths()
						dialog2.Destroy()
						self.text_detection.SetLabel('The path to the Detector is: '+self.path_to_detector+'.')
					else:
						self.path_to_detector=os.path.join(self.detector_path,detector)
						self.text_detection.SetLabel('Detector: '+detector+'.')
				dialog1.Destroy()
				if torch.cuda.is_available():
					dialog1=wx.NumberEntryDialog(self,"Enter the batch size for faster processing","GPU is available in this device to enable batch processing.\nYou may use batch processing for faster speed.",'Batch size',0,0,100)
					if dialog1.ShowModal()==wx.ID_OK:
						self.detector_batch=dialog1.GetValue()
					dialog1.Destroy()

		dialog.Destroy()


	def select_behaviors(self,event):

		if self.path_to_categorizer is None:

			wx.MessageBox('No Categorizer selected! The behavior names are listed in the Categorizer.','Error',wx.OK|wx.ICON_ERROR)

		else:

			behaviors=list(self.behaviornames_and_colors.keys())
			dialog=wx.MultiChoiceDialog(self,message='Select behaviors',caption='Behaviors to annotate',choices=behaviors)
			if dialog.ShowModal()==wx.ID_OK:
				self.behavior_to_annotate=[behaviors[i] for i in dialog.GetSelections()]
			else:
				self.behavior_to_annotate=behaviors
			dialog.Destroy()

			if len(self.behavior_to_annotate)==0:
				self.behavior_to_annotate=behaviors
			if self.behavior_to_annotate[0]=='all':
				self.behavior_to_annotate=behaviors

			complete_colors=list(mpl.colors.cnames.values())
			colors=[]
			for c in complete_colors:
				colors.append(['#ffffff',c])
			
			dialog=wx.MessageDialog(self,'Specify the color to represent\nthe behaviors in annotations and plots?','Specify colors for behaviors?',wx.YES_NO|wx.ICON_QUESTION)
			if dialog.ShowModal()==wx.ID_YES:
				names_colors={}
				n=0
				while n<len(self.behavior_to_annotate):
					dialog2=ColorPicker(self,'Color for '+self.behavior_to_annotate[n],[self.behavior_to_annotate[n],colors[n]])
					if dialog2.ShowModal()==wx.ID_OK:
						(r,b,g,_)=dialog2.color_picker.GetColour()
						new_color='#%02x%02x%02x'%(r,b,g)
						self.behaviornames_and_colors[self.behavior_to_annotate[n]]=['#ffffff',new_color]
						names_colors[self.behavior_to_annotate[n]]=new_color
					else:
						if n<len(colors):
							names_colors[self.behavior_to_annotate[n]]=colors[n][1]
							self.behaviornames_and_colors[self.behavior_to_annotate[n]]=colors[n]
					dialog2.Destroy()
					n+=1
				self.text_selectbehaviors.SetLabel('Selected: '+str(names_colors)+'.')
			else:
				for color in colors:
					index=colors.index(color)
					if index<len(self.behavior_to_annotate):
						behavior_name=list(self.behaviornames_and_colors.keys())[index]
						self.behaviornames_and_colors[behavior_name]=color
				self.text_selectbehaviors.SetLabel('Selected: '+str(self.behavior_to_annotate)+' with default colors.')
			dialog.Destroy()

			dialog=wx.MessageDialog(self,'Show legend of behavior names in the annotated video?','Legend in video?',wx.YES_NO|wx.ICON_QUESTION)
			if dialog.ShowModal()==wx.ID_YES:
				self.show_legend=True
			else:
				self.show_legend=False
			dialog.Destroy()


	def select_parameters(self,event):

		if self.path_to_categorizer is None:
			parameters=['3 areal parameters','3 length parameters','4 locomotion parameters']
		else:
			parameters=['count','duration','latency','3 areal parameters','3 length parameters','4 locomotion parameters']

		dialog=wx.MultiChoiceDialog(self,message='Select quantitative measurements',caption='Quantitative measurements',choices=parameters)
		if dialog.ShowModal()==wx.ID_OK:
			self.parameter_to_analyze=[parameters[i] for i in dialog.GetSelections()]
		else:
			self.parameter_to_analyze=[]
		dialog.Destroy()

		if len(self.parameter_to_analyze)==0:
			self.parameter_to_analyze=[]

		dialog=wx.MessageDialog(self,'Normalize the distances by the size of an animal? If no, all distances will be output in pixels.','Normalize the distances?',wx.YES_NO|wx.ICON_QUESTION)
		if dialog.ShowModal()==wx.ID_YES:
			self.normalize_distance=True
			self.text_selectparameters.SetLabel('Selected: '+str(self.parameter_to_analyze)+'; with normalization of distance.')
		else:
			self.normalize_distance=False
			self.text_selectparameters.SetLabel('Selected: '+str(self.parameter_to_analyze)+'; NO normalization of distance.')
		dialog.Destroy()


	def analyze_behaviors(self,event):

		if self.path_to_videos is None or self.result_path is None:

			wx.MessageBox('No input video(s) / result folder.','Error',wx.OK|wx.ICON_ERROR)

		else:

			all_events=OrderedDict()
			event_data=OrderedDict()
			all_lengths=[]

			if self.path_to_categorizer is None:
				self.behavior_to_annotate=[]
			else:
				if self.behavior_to_annotate[0]=='all':
					self.behavior_to_annotate=list(self.behaviornames_and_colors.keys())

			for i in self.path_to_videos:
				filename=os.path.splitext(os.path.basename(i))[0].split('_')
				if self.decode_animalnumber is True:
					for x in filename:
						if len(x)>0:
							if x[0]=='n':
								self.animal_number=int(x[1:])
				if self.decode_t is True:
					for x in filename:
						if len(x)>0:
							if x[0]=='b':
								self.t=float(x[1:])
				if self.decode_extraction is True:
					for x in filename:
						if len(x)>0:
							if x[:2]=='xs':
								self.ex_start=int(x[2:])
							if x[:2]=='xe':
								self.ex_end=int(x[2:])

				if self.animal_number==1:
					self.relink=True

				AA=AnalyzeAnimal()
				if self.path_to_categorizer is None:
					categorize_behavior=False
				else:
					categorize_behavior=True

				if self.use_detector is False:
					AA.prepare_analysis(i,self.result_path,self.animal_number,delta=self.delta,names_and_colors=self.behaviornames_and_colors,framewidth=self.framewidth,stable_illumination=self.stable_illumination,dim_tconv=self.dim_tconv,dim_conv=self.dim_conv,channel=self.channel,include_bodyparts=self.include_bodyparts,std=self.std,categorize_behavior=categorize_behavior,animation_analyzer=self.animation_analyzer,path_background=self.background_path,autofind_t=self.autofind_t,t=self.t,duration=self.duration,ex_start=self.ex_start,ex_end=self.ex_end,length=self.length,animal_vs_bg=self.animal_vs_bg,use_detector=False)
					AA.acquire_information(relink=self.relink,background_free=self.background_free)
				else:
					AA.prepare_analysis(i,self.result_path,self.animal_number,delta=self.delta,names_and_colors=self.behaviornames_and_colors,framewidth=self.framewidth,stable_illumination=self.stable_illumination,dim_tconv=self.dim_tconv,dim_conv=self.dim_conv,channel=self.channel,include_bodyparts=self.include_bodyparts,std=self.std,categorize_behavior=categorize_behavior,animation_analyzer=self.animation_analyzer,path_background=self.background_path,autofind_t=self.autofind_t,t=self.t,duration=self.duration,ex_start=self.ex_start,ex_end=self.ex_end,length=self.length,animal_vs_bg=self.animal_vs_bg,use_detector=True)
					if self.detector_batch>1:
						AA.acquire_information_dynamic_batch(self.path_to_detector,batch_size=self.detector_batch,relink=self.relink,background_free=self.background_free)
					else:
						AA.acquire_information_dynamic(self.path_to_detector,relink=self.relink,background_free=self.background_free)

				AA.craft_data()
				if self.path_to_categorizer is not None:
					AA.categorize_behaviors(self.path_to_categorizer,uncertain=self.uncertain)
				AA.annotate_video(self.behavior_to_annotate,show_legend=self.show_legend)
				AA.export_results(normalize_distance=self.normalize_distance,parameter_to_analyze=self.parameter_to_analyze)

				if self.path_to_categorizer is not None:
					for n in list(AA.event_probability.keys()):
						all_events[len(all_events.keys())]=AA.event_probability[n]
						all_lengths.append(len(AA.event_probability[n]))

			if self.path_to_categorizer is not None:

				for n in list(all_events.keys()):
					event_data[len(event_data.keys())]=all_events[n][:min(all_lengths)]
				time_points=AA.all_time[:min(all_lengths)]
			
				all_events_df=pd.DataFrame.from_dict(event_data,orient='index',columns=time_points)
				if min(all_lengths)<16000:
					all_events_df.to_excel(os.path.join(self.result_path,'all_events.xlsx'),float_format='%.2f')
				else:
					all_events_df.to_csv(os.path.join(self.result_path,'all_events.csv'),float_format='%.2f')

				plot_evnets(self.result_path,event_data,time_points,self.behaviornames_and_colors,self.behavior_to_annotate,width=0,height=0)

				folders=[i for i in os.listdir(self.result_path) if os.path.isdir(os.path.join(self.result_path,i))]
				folders.sort()

				for behavior_name in list(self.behaviornames_and_colors.keys()):
					all_summary=[]
					for folder in folders:
						individual_summary=os.path.join(self.result_path,folder,behavior_name,'all_summary.xlsx')
						if os.path.exists(individual_summary) is True:
							all_summary.append(pd.read_excel(individual_summary))
					if len(all_summary)>=1:
						all_summary=pd.concat(all_summary,ignore_index=True)
						all_summary.to_excel(os.path.join(self.result_path,behavior_name+'_summary.xlsx'),float_format='%.2f')


