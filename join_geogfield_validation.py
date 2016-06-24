import arcpy
class ToolValidator(object):
  """Class for validating a tool's parameter values and controlling
  the behavior of the tool's dialog."""

  def __init__(self):
    """Setup arcpy and the list of tool parameters."""
    self.params = arcpy.GetParameterInfo()

  def initializeParameters(self):
    """Refine the properties of a tool's parameters.  This method is
    called when the tool is opened."""
          
    return

  def updateParameters(self):
    """Modify the values and properties of parameters before internal
    validation is performed.  This method is called whenever a parameter
    has been changed."""

    self.params = arcpy.GetParameterInfo()

    if self.params[0].value:
        
        geography = str(self.params[0].value)
        if geography == 'County':
            i = ["NAME", "GEOID", "COUNTYFP", "COUNTYNS", "AFFGEOID", "LSAD"]
            self.params[1].filter.list = i
        elif geography == 'State':
                i = ["NAME", "STUPSPS", "GEOID", "GEOID10", "STATENS", "AFFGEOID", "LSAD"]
                self.params[1].filter.list = i
        elif geography == 'ZCTA':
                i = ["GEOID10", "ZCTA5CE10", "AFFGEOID"]
                self.params[1].filter.list = i
        elif geography == 'PUMA':
                i = ["GEOID10", "PUMACE10", "STATEFP10", "AFFGEOID1", "NAME10","LSAD10"]
                self.params[1].filter.list = i
	elif geography == 'Block Group':
                i = ["GEOID"]
                self.params[1].filter.list = i
	elif geography == 'Congressional District':
                i = ["GEOID", "STATEFP", "CD114FP", "AFFGEOID", "LSAD", "CDSESSN" ]
                self.params[1].filter.list = i
        else:
            pass

    return

  def updateMessages(self):
    """Modify the messages created by internal validation for each tool
    parameter.  This method is called after internal validation."""
    return
