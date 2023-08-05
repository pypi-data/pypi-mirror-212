# pylint: disable=R0801

"""
Async implementations of flow classes defined in another module.
"""

import asyncio
from llmflows.flows.async_flowstep import AsyncFlowStep


class AsyncBaseFlow:
    """Base class for all async flows."""

    def __init__(self, first_step: AsyncFlowStep):
        """
        Initializes the AsyncBaseFlow.

        Args:
            first_step (AsyncFlowStep): The first step of the flow.
        """
        self.first_step = first_step

    def set_first_step(self, step: AsyncFlowStep):
        """
        Sets the initial step of the flow.

        Args:
            step (AsyncFlowStep): The initial step for the flow.
        """
        self.first_step = step

    async def execute(self, **inputs: str):
        """
        Placeholder for flow execution method. To be overridden in subclasses.

        Args:
            **inputs (str): Inputs to the flow.

        Raises:
            NotImplementedError: If not implemented in subclass.
        """
        raise NotImplementedError


class AsyncFlow(AsyncBaseFlow):
    """Asynchronous version of a DAG consisting of AsyncFlowSteps."""

    def __init__(self, first_step: AsyncFlowStep):
        """
        Initializes the AsyncFlow.

        Args:
            first_step (AsyncFlowStep): The first step of the flow.
        """
        super().__init__(first_step)
        self.results = []
        self._results_lock = asyncio.Lock()
        self.executed_steps = set()
        self._check_unique_output_keys()

    def _check_unique_output_keys(self):
        """
        Ensures unique output keys among steps.

        Raises:
            ValueError: If duplicate output keys exist.
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

    async def execute(self, verbose: bool = False, **inputs: str):
        """
        Executes the flow.

        Args:
            verbose (bool): If true, flowstep outputs are printed.
            **inputs (str): Inputs to the flow.
        """
        await self._execute_step(self.first_step, inputs, verbose)
        return self.results

    async def _execute_step(self, step: AsyncFlowStep, inputs: dict, verbose: bool):
        """
        Concurrently executes a step and all subsequent steps.

        Args:
            step (AsyncFlowStep): The step to execute.
            inputs (dict): Inputs to the step.
            verbose (bool): If true, step outputs are printed.
        """
        if not step or any(parent.output_key not in inputs for parent in step.parents):
            return

        required_inputs = {key: inputs[key] for key in step.prompt_template.variables}

        if step not in self.executed_steps:
            new_inputs = await step.execute(required_inputs, verbose)
            self.executed_steps.add(step)

            if new_inputs:
                async with self._results_lock:
                    self.results.append({
                        'step': step.name,
                        'output_key': step.output_key,
                        'output_value': new_inputs[step.output_key]
                    })
                inputs.update(new_inputs)

        if step.next_steps:
            await asyncio.gather(
                *[self._execute_step(next_step, inputs, verbose)
                  for next_step in step.next_steps]
            )
