#
# Copyright (c) 2009-2022 CERN. All rights nots expressly granted are
# reserved.
#
# This file is part of iLCDirac
# (see ilcdirac.cern.ch, contact: ilcdirac-support@cern.ch).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# In applying this licence, CERN does not waive the privileges and
# immunities granted to it by virtue of its status as an
# Intergovernmental Organization or submit itself to any jurisdiction.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""Delphes Application to run applications based on Delphes.

.. versionadded:: v34r0

Usage:

>>> delphes = DelphesApp()
>>> delphes.setVersion('key4hep-latest')
>>> delphes.setExecutable("DelphesPythia8_EDM4HEP")
>>> delphes.setDetectorCard('card_IDEA.tcl')
>>> delphes.setOutputCard('edm4hep_IDEA.tcl')
>>> delphes.setPythia8Card('p8_ee_ggqq_ecm91.cmd')
>>> delphes.setRandomSeed(12340)
>>> delphes.setEnergy(91.2)
>>> delphes.setNumberOfEvents(100)
>>> delphes.setOutputFile('output.root')

"""
from __future__ import absolute_import
import types
import os

from ILCDIRAC.Interfaces.API.NewInterface.LCApplication import LCApplication
from ILCDIRAC.Core.Utilities.InstalledFiles import Exists
from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Core.Workflow.Parameter import Parameter
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
import six
from ILCDIRAC.Core.Utilities.PrepareOptionFiles import preparePythia8Card

LOG = gLogger.getSubLogger(__name__)
__RCSID__ = "$Id$"


class DelphesApp(LCApplication):
  """DelphesApp Application Class."""

  def __init__(self, paramdict=None):
    self.randomSeed = -1
    self.executableName = ''
    self.detectorCard = ''
    self.outputCard = ''
    self.pythia8CardContent = ''
    super(DelphesApp, self).__init__(paramdict)
    # Those 5 need to come after default constructor
    self._modulename = 'DelphesAppModule'
    self._moduledescription = 'Module to run DelphesApp'
    self.appname = 'delphesapp'
    self._ops = Operations()
    self._extension = 'root'

  def setRandomSeed(self, randomSeed):
    """Define random seed to use. Default is the jobID.

    :param int randomSeed: Seed to use during simulation.
    """
    self._checkArgs({'randomSeed': int})
    self.randomSeed = randomSeed
    return S_OK()


  def setArguments(self, args):
    """Define the arguments of the script.

    Alternative to :func:`DelphesApp.setExtraCLIArguments`.

    :param str args: Arguments to pass to the command call
    """
    self._checkArgs({'args': (str,)})
    self.extraCLIArguments = args
    return S_OK()
  
  def setExecutableName(self, executableName):
    """Set the executable.

    :param str executableName: Name of the delphes executable program.
    """
    self._checkArgs({'executableName': (str,)})
    self.executableName = executableName
    return S_OK()

  
  def setDetectorCard(self, detectorCard):
    """Set the detector card.

    :param str detectorCard: Name of the detector configuration file in Tcl format.
    """
    self._checkArgs({'detectorCard': (str,)})
    self.detectorCard = detectorCard
    if os.path.exists(detectorCard) or detectorCard.lower().count("lfn:"):
      self.inputSB.append(detectorCard)
    return S_OK()


  def setOutputCard(self, outputCard):
    """Set the output card.

    :param str outputCard: Name of the configuration file steering the content of the edm4hep output in Tcl format.
    """
    self._checkArgs({'outputCard': (str,)})
    self.outputCard = outputCard
    if os.path.exists(outputCard) or outputCard.lower().count("lfn:"):
      self.inputSB.append(outputCard)
    return S_OK()


  def setPythia8Card(self, pythia8CardPath):
    """Set the pythia8 card.

    :param str pythia8CardPath: Name of the Pythia8 configuration file path.
    """
    pythiaCardsLocations = Operations().getValue("/ProcessList/PythiaCardsLocation", [])
    self._checkArgs({'pythia8CardPath': (str,)})
    if os.path.isfile(pythia8CardPath):
      self.pythia8CardContent = open(pythia8CardPath).read()
      return S_OK()
    else:
      for PythiaCardsLocation in pythiaCardsLocations:
        pythia8CardEOS = os.path.join(PythiaCardsLocation, pythia8CardPath)
        if os.path.isfile(pythia8CardEOS):
          LOG.notice(f"Reading pythia card from {pythia8CardEOS}")
          self.pythia8CardContent = open(pythia8CardEOS).read()
          return S_OK()
      return self._reportError('Pythia8 configuration file does not exist!')


  def _userjobmodules(self, stepdefinition):
    res1 = self._setApplicationModuleAndParameters(stepdefinition)
    res2 = self._setUserJobFinalization(stepdefinition)
    if not res1["OK"] or not res2["OK"]:
      return S_ERROR('userjobmodules failed')
    return S_OK()

  def _prodjobmodules(self, stepdefinition):
    res1 = self._setApplicationModuleAndParameters(stepdefinition)
    res2 = self._setOutputComputeDataList(stepdefinition)
    if not res1["OK"] or not res2["OK"]:
      return S_ERROR('prodjobmodules failed')
    return S_OK()

  def _checkConsistency(self, job=None):
    """Check consistency of the DelphesApp application.

    Called from the `Job` instance.

    :param job: The instance of the job
    :type job: ~ILCDIRAC.Interfaces.API.NewInterface.Job.Job
    :returns: S_OK/S_ERROR
    """
    parameterName = [pN for pN in job.workflow.parameters.getParametersNames() if 'ConfigPackage' in pN]
    configversion = None
    if parameterName:
      LOG.notice("Found config parameter", parameterName)
      config = job.workflow.parameters.find(parameterName[0])
      configversion = config.value
    # Platform must always be defined
    platform = job.workflow.parameters.find("Platform").value

    if not self.version:
      return S_ERROR('No version found')
    
    if self.executableName not in ['DelphesPythia8_EDM4HEP', 'DelphesSTDHEP_EDM4HEP', 'DelphesROOT_EDM4HEP']:
      return S_ERROR('Executable not supported. Supported executables: DelphesPythia8_EDM4HEP, DelphesSTDHEP_EDM4HEP, DelphesROOT_EDM4HEP')
    
    if self.randomSeed < -1:
      return S_ERROR('Random Seed has to be equal or greater than -1')
    
    if self.detectorCard:
      if not self.detectorCard.endswith(".tcl"):
        return S_ERROR('Wrong name for the detector config file. Hint: they all end in ".tcl"')
      if not os.path.exists(self.detectorCard) and not self.detectorCard.lower().startswith("lfn:"):
        res = Exists(self.detectorCard, platform=platform, configversion=configversion)
        if not res['OK']:
          return res
    else:
      return S_ERROR('Missing detector config-file.')
    
    if self.outputCard:
      if not self.outputCard.endswith(".tcl"):
        return S_ERROR('Wrong name for the output config file. Hint: they all end in ".tcl"')
      if not os.path.exists(self.outputCard) and not self.outputCard.lower().startswith("lfn:"):
        res = Exists(self.outputCard, platform=platform, configversion=configversion)
        if not res['OK']:
          return res
    else:
      return S_ERROR('Missing output-config-file.')
            
    if self.executableName == "DelphesPythia8_EDM4HEP" and not self.pythia8CardContent:
      return S_ERROR('Missing Pythia 8 Card. The execution of DelphesPythia8_EDM4HEP would not succeed')

    if self.pythia8CardContent:
      res = preparePythia8Card(self.pythia8CardContent, 0, self.randomSeed, self.energy)
      if not res['OK']:
        return res
      
    if self._jobtype != 'User':
      self._listofoutput.append({"outputFile": "@{OutputFile}", "outputPath": "@{OutputPath}",
                                 "outputDataSE": '@{OutputSE}'})

    return S_OK()

  def _applicationModule(self):

    md1 = self._createModuleDefinition()
    md1.addParameter(Parameter("randomSeed", 0, "int", "", "", False, False,
                               "Random seed for the generator"))
    md1.addParameter(Parameter("executableName", "", "string", "", "", False, False,
                               "Name of the executable"))
    md1.addParameter(Parameter("detectorCard", "", "string", "", "", False, False,
                               "Flag that defines the detector card (e.g. ``delphes_card_IDEA.tcl``)"))    
    md1.addParameter(Parameter("outputCard", "", "string", "", "", False, False,
                               "Flag that defines the output card (e.g. ``edm4hep_output_config.tcl``)"))
    md1.addParameter(Parameter("pythia8CardContent", "", "string", "", "", False, False,
                               "Flag that defines the pythia8 card (e.g. ``path/p8_ee_ggqq_ecm91.cmd``)"))      
    md1.addParameter(Parameter("debug", False, "bool", "", "", False, False, "debug mode"))
    return md1

  def _applicationModuleValues(self, moduleinstance):

    moduleinstance.setValue("randomSeed", self.randomSeed)
    moduleinstance.setValue("executableName", self.executableName)
    moduleinstance.setValue("detectorCard", self.detectorCard)
    moduleinstance.setValue("outputCard", self.outputCard)
    moduleinstance.setValue("pythia8CardContent", self.pythia8CardContent)
    moduleinstance.setValue("debug", self.debug)

  def _checkWorkflowConsistency(self):
    return self._checkRequiredApp()

  def _resolveLinkedStepParameters(self, stepinstance):
    if isinstance(self._linkedidx, six.integer_types):
      self._inputappstep = self._jobsteps[self._linkedidx]
    if self._inputappstep:
      stepinstance.setLink("InputFile", self._inputappstep.getType(), "OutputFile")
    return S_OK()
