"""
A Case class.
"""


class Case(object):
    """
    Case wraps the data from a single iteration of a recording to make it more easily accessible.

    Parameters
    ----------
    filename : str
        The filename from which the Case was constructed.
    counter : int
        The global execution counter.
    iteration_coordinate : str
        The string that holds the full unique identifier for this iteration.
    timestamp : float
        Time of execution of the case.
    success : str
        Success flag for the case.
    msg : str
        Message associated with the case.

    Attributes
    ----------
    filename : str
        The file from which the case was loaded.
    counter : int
        The global execution counter.
    iteration_coordinate : str
        The string that holds the full unique identifier for this iteration.
    timestamp : float
        Time of execution of the case.
    success : str
        Success flag for the case.
    msg : str
        Message associated with the case.
    """

    def __init__(self, filename, counter, iteration_coordinate, timestamp, success, msg):
        """
        Initialize.
        """
        self.filename = filename
        self.counter = counter
        self.iteration_coordinate = iteration_coordinate

        self.timestamp = timestamp
        self.success = success
        self.msg = msg


class DriverCase(Case):
    """
    Wrap data from a single iteration of a Driver recording to make it more easily accessible.

    Parameters
    ----------
    filename : str
        The filename from which the DriverCase was constructed.
    counter : int
        The global execution counter.
    iteration_coordinate: str
        The string that holds the full unique identifier for the desired iteration.
    timestamp : float
        Time of execution of the case.
    success : str
        Success flag for the case.
    msg : str
        Message associated with the case.
    desvars : array
        Driver design variables to read in from the recording file.
    responses : array
        Driver responses to read in from the recording file.
    objectives : array
        Driver objectives to read in from the recording file.
    constraints : array
        Driver constraints to read in from the recording file.

    Attributes
    ----------
    desvars : array
        Driver design variables that have been read in from the recording file.
    responses : array
        Driver responses that have been read in from the recording file.
    objectives : array
        Driver objectives that have been read in from the recording file.
    constraints : array
        Driver constraints that have been read in from the recording file.
    """

    def __init__(self, filename, counter, iteration_coordinate, timestamp, success, msg, desvars,
                 responses, objectives, constraints, sysincludes, prom2abs):
        """
        Initialize.
        """
        super(DriverCase, self).__init__(filename, counter, iteration_coordinate,
                                         timestamp, success, msg)

        self.desvars = PromotedToAbsoluteMap(desvars[0] if desvars.dtype.names
                                             else None, prom2abs)
        self.responses = PromotedToAbsoluteMap(responses[0] if responses.dtype.names
                                                else None, prom2abs)
        self.objectives = PromotedToAbsoluteMap(objectives[0] if objectives.dtype.names
                                                 else None, prom2abs)
        self.constraints = PromotedToAbsoluteMap(constraints[0] if constraints.dtype.names
                                                  else None, prom2abs)
        self.sysincludes = PromotedToAbsoluteMap(sysincludes[0] if sysincludes.dtype.names
                                                  else None, prom2abs)


class SystemCase(Case):
    """
    Wraps data from a single iteration of a System recording to make it more accessible.

    Parameters
    ----------
    filename : str
        The filename from which the SystemCase was constructed.
    counter : int
        The global execution counter.
    iteration_coordinate: str
        The string that holds the full unique identifier for the desired iteration.
    timestamp : float
        Time of execution of the case
    success : str
        Success flag for the case
    msg : str
        Message associated with the case
    inputs : array
        System inputs to read in from the recording file.
    outputs : array
        System outputs to read in from the recording file.
    residuals : array
        System residuals to read in from the recording file.

    Attributes
    ----------
    inputs : array
        System inputs that have been read in from the recording file.
    outputs : array
        System outputs that have been read in from the recording file.
    residuals : array
        System residuals that have been read in from the recording file.
    """

    def __init__(self, filename, counter, iteration_coordinate, timestamp, success, msg, inputs,
                 outputs, residuals, prom2abs):
        """
        Initialize.
        """
        super(SystemCase, self).__init__(filename, counter, iteration_coordinate,
                                         timestamp, success, msg)

        self.inputs = PromotedToAbsoluteMap(inputs[0] if inputs.dtype.names else None, prom2abs, False)
        self.outputs = PromotedToAbsoluteMap(outputs[0] if outputs.dtype.names else None, prom2abs)
        self.residuals = PromotedToAbsoluteMap(residuals[0] if residuals.dtype.names else None, prom2abs)


class SolverCase(Case):
    """
    Wraps data from a single iteration of a System recording to make it more accessible.

    Parameters
    ----------
    filename : str
        The filename from which the SystemCase was constructed.
    counter : int
        The global execution counter.
    iteration_coordinate: str

    timestamp : float
        Time of execution of the case
    success : str
        Success flag for the case
    msg : str
        Message associated with the case
    abs_err : array
        Solver absolute error to read in from the recording file.
    rel_err : array
        Solver relative error to read in from the recording file.
    outputs : array
        Solver outputs to read in from the recording file.
    residuals : array
        Solver residuals to read in from the recording file.

    Attributes
    ----------
    abs_err : array
        Solver absolute error that has been read in from the recording file.
    rel_err : array
        Solver relative error that has been read in from the recording file.
    outputs : array
        Solver outputs that have been read in from the recording file.
    residuals : array
        Solver residuals that have been read in from the recording file.
    """

    def __init__(self, filename, counter, iteration_coordinate, timestamp, success, msg,
                 abs_err, rel_err, outputs, residuals, prom2abs):
        """
        Initialize.
        """
        super(SolverCase, self).__init__(filename, counter, iteration_coordinate, timestamp,
                                         success, msg)

        self.abs_err = abs_err
        self.rel_err = rel_err
        self.outputs = PromotedToAbsoluteMap(outputs[0] if outputs.dtype.names else None, prom2abs)
        self.residuals = PromotedToAbsoluteMap(residuals[0] if residuals.dtype.names else None,
                                               prom2abs)


class PromotedToAbsoluteMap:
    def __init__(self, values, prom2abs, output=True):
        """
        Initialize.
        """
        self._values = values
        self._prom2abs = prom2abs
        self._input_output = 'output' if output else 'input'

    def __getitem__(self, key):
        return self._values[self._prom2abs[self._input_output][key][0]]
