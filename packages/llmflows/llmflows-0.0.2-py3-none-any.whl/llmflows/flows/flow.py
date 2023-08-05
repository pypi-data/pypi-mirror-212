# pylint: disable=R0801

"""
This module provides implementations of BaseFlow and Flow.
"""

from llmflows.flows.flowstep import FlowStep


class BaseFlow:
    """
    Base class for all flows. Each specific flow should extend this class.
    """

    def __init__(self, first_step=None):
        """
        Initializes the BaseFlow.

        Args:
            first_step: The initial step of the flow, defaults to None.
        """
        self.first_step = first_step

    def set_first_step(self, step):
        """
        Sets the initial step of the flow.

        Args:
            step: The initial step for the flow.
        """
        self.first_step = step

    def execute(self, **inputs):
        """
        Executes the flow with the given inputs. 

        This is a placeholder method and should be overridden in each 
        specific flow.

        Args:
            inputs: Inputs to the flow.

        Raises:
            NotImplementedError: If not implemented in a class that extends BaseFlow.
        """
        raise NotImplementedError


class Flow(BaseFlow):
    """
    A Directed Acyclic Graph (DAG) structure consisting of FlowSteps.

    Attributes:
        first_step (FlowStep): The first step in the flow.
        executed_steps (set): The steps that have been executed.

    Raises:
        ValueError: If flow steps have same output key.
    """

    def __init__(self, first_step: FlowStep):
        super().__init__(first_step)
        self.results = []
        self.executed_steps = set()
        self._check_unique_output_keys()

    def _check_unique_output_keys(self):
        """
        Checks that all flow steps have unique output keys.

        Raises:
            ValueError: If any flow steps have same output key.
        """
        queue = [self.first_step]
        visited_steps = set()
        used_output_keys = set()

        while queue:
            current_step = queue.pop(0)

            if current_step in visited_steps or current_step is None:
                continue

            if current_step.output_key in used_output_keys:
                raise ValueError(
                    f"The output key '{current_step.output_key}' has already been used"
                    " in another FlowStep."
                )

            used_output_keys.add(current_step.output_key)
            visited_steps.add(current_step)
            queue.extend(current_step.next_steps)

    def execute(self, verbose=False, **inputs):
        """
        Executes the flow with the given inputs.

        Args:
            verbose: Specifies if the flowstep should print their output
            **inputs: The inputs to the flow.

        Raises:
            ValueError: If any required inputs are missing.
        """
        self._execute_step(self.first_step, inputs, verbose)
        return self.results

    def _execute_step(self, step, inputs, verbose):
        """
        DFS-like execution of the given step with the given inputs.

        Args:
            step (FlowStep): The step to execute.
            inputs (dict): The inputs to the step.

        Returns:
            Any: The output of the step.
        """
        if not step or any(parent.output_key not in inputs for parent in step.parents):
            return

        required_inputs = {key: inputs[key] for key in step.prompt_template.variables}

        # If step has not been executed yet, execute it.
        if step not in self.executed_steps:
            new_inputs = step.execute(required_inputs, verbose)
            self.executed_steps.add(step)

            if new_inputs:
                self.results.append({
                    'step': step.name,
                    'output_key': step.output_key,
                    'output_value': new_inputs[step.output_key]
                })
                inputs.update(new_inputs)

        for next_step in step.next_steps:
            self._execute_step(next_step, inputs, verbose)
