import asyncio
import json
import warnings
from time import sleep
from typing import Any, Dict, List, Optional, Sequence

import numpy as np
import requests
from orquestra.quantum.api import BaseCircuitRunner
from orquestra.quantum.circuits import Circuit
from orquestra.quantum.distributions import MeasurementOutcomeDistribution
from orquestra.quantum.measurements import Measurements

from .circuit_conversions import export_to_ionq


class IonQRunner(BaseCircuitRunner):
    JOB_DONE = ["completed", "failed", "canceled", "deleted"]

    def __init__(
        self,
        api_token: str,
        target: str,
        max_trials: int = 3,
        use_native_gates: bool = False,
        noise_model: str = "ideal",
        seed: Optional[int] = None,
    ):
        """IonQ Runner class for running circuits on IonQ's QPU or simulator.

        Args:
            api_token (str): Your API key for IonQ.
            target (str): The hardware to run your circuit on. Options are:
              "qpu.harmony", "qpu.aria-1", or "simulator". Using "simulator" is free,
              but using a QPU requires a paid subscription.
            max_trials (int, optional): Number of times to request IonQ create a job
              which will run your circuit. Defaults to 3.
            use_native_gates (bool, optional): Whether to ignore IonQ's compiler and
              use IonQ's native gateset directly. Defaults to False.
            noise_model (Optional[Dict[str, Union[str, int]]], optional): Type of noise
              to be simulated. Options are: "harmony", "aria-1", and "ideal".
              This argument is ignored when target is a QPU. Defaults to "ideal".
            seed (Optional[int]): Seed for the simulator. Defaults to None.

        Raises:
            ValueError: if target is a QPU and noise_model is not "ideal".
        """
        super().__init__()
        if api_token == "":
            raise ValueError(
                "IonQ API token not found. If you are running tests, "
                "you might need to set IONQ_API_TOKEN environment variable."
            )
        self._api_token = api_token
        self.target = target
        self.max_trials = max_trials
        self.use_native_gates = use_native_gates
        self.job_ids: List[str] = []
        self.noise_model = noise_model
        self.seed = seed

        if target[:3] == "qpu" and self.noise_model != "ideal":
            raise ValueError("Noise models are only supported on simulators.")

    def create_job(self, circuit: Circuit, n_samples: int):
        """
        Creates a job on the IonQ backend (QPU or simulator) within which the given
          circuit is executed
        Args:
            circuit_string: quantum circuit to be executed given in textual
              representation.
            n_samples: the number of shots to perform.
        Returns:
            str: the ID of the job within which the circuit was executed.
        """
        # Get the qasm representation of the circuit
        circuit_dict = export_to_ionq(circuit)
        circuit_dict["gateset"] = "native" if self.use_native_gates else "qis"
        self.check_gates_are_supported(circuit_dict)

        request_dict = {
            "shots": n_samples,
            "target": self.target,
            "lang": "json",
            "body": circuit_dict,
        }
        if self.target[:3] != "qpu":
            if self.seed is not None:
                request_dict["noise"] = {"model": self.noise_model, "seed": self.seed}
            else:
                request_dict["noise"] = {"model": self.noise_model}

        max_trials = self.max_trials
        while max_trials > 0:
            response = requests.post(
                "https://api.ionq.co/v0.2/jobs",
                data=json.dumps(request_dict),
                headers={
                    "Authorization": "apiKey " + self._api_token,
                    "Content-Type": "application/json",
                },
            )

            if response.status_code != 200:
                print(response)
                if max_trials == 1:
                    raise ValueError(
                        "Creating a job to run the given circuit failed"
                        "after {} attempts.".format(max_trials)
                    )
                else:
                    print("Creating a job failed, retrying...")
                    sleep(np.random.randint(5, 11))
                    max_trials = max_trials - 1
            else:
                max_trials = 0

        job_id = response.json()["id"]
        self.job_ids.append(job_id)
        return job_id

    def check_gates_are_supported(self, circuit_dict: Dict[str, Any]):
        if circuit_dict["gateset"] == "native":
            for gate_info in circuit_dict["circuit"]:
                if gate_info["gate"] not in ["gpi", "gpi2", "ms"]:
                    raise ValueError(
                        "Gate " + gate_info["gate"] + " is not supported "
                        "by IonQ's native gateset."
                    )
        if circuit_dict["gateset"] == "qis" and self.target == "simulator":
            for gate_info in circuit_dict["circuit"]:
                if gate_info["gate"] in ["gpi", "gpi2", "ms"]:
                    raise ValueError(
                        "Gate " + gate_info["gate"] + " is not supported "
                        "by the non-native gateset inside the IonQ simulator."
                    )

    def get_job(self, job_id: str):
        """
        Returns a dictionary containing information as to the status of the given
        job [ID] and if the job was completed, this dictionary will also contain the
        distribution corresponding to submitted circuit execution.

        Args:
            job_id (str): ID of the job to retrieve.
        Returns:
            dict: a dictionary with the job data.
        """
        max_trials = self.max_trials
        while max_trials > 0:
            response = requests.get(
                "https://api.ionq.co/v0.2/jobs/" + job_id,
                headers={
                    "Authorization": "apiKey " + self._api_token,
                    "Content-Type": "application/json",
                },
            )

            if response.status_code != 200:
                print(response)
                if max_trials == 1:
                    raise ValueError(
                        "Job with id <"
                        + job_id
                        + "> not found after {} trials.".format(self.max_trials)
                    )
                else:
                    print("Issue retrieving job with id <", job_id, ">, retrying...")
                    sleep(np.random.randint(5, 11))
                    max_trials = max_trials - 1
            else:
                max_trials = 0

        return response.json()

    def get_jobs(self, job_ids: List[str]):
        """
        Retrieves a list of jobs corresponding the given job IDs.
        Args:
            job_ids: ID of the job to retrieve.
        Returns:
            List[dict]: a list of dictionaries containing job data.
        """
        jobs_data: Dict[str, List[int]] = {"jobs": []}
        for job_id in job_ids:
            jobs_data["jobs"].append(self.get_job(job_id))

        return jobs_data

    def cancel_job(self, job_id: str):
        """
        Cancels the job corresponding to the given job ID.
        Args:
            job_id: ID of the job to cancel.
        Returns:
            dict: a dictionary with cancellation status.
        """
        response = requests.put(
            "https://api.ionq.co/v0.2/jobs/" + job_id + "/status/cancel",
            headers={
                "Authorization": "apiKey " + self._api_token,
            },
        )

        return response.json()

    def delete_job(self, job_id: str):
        """
        Deletes the job corresponding to the given job ID.
        Args:
            job_id: ID of the job to delete.
        Returns:
            dict: a dictionary with deletion status.
        """
        response = requests.delete(
            "https://api.ionq.co/v0.2/jobs/" + job_id,
            headers={
                "Authorization": "apiKey " + self._api_token,
            },
        )

        return response.json()

    async def get_job_results(self, job_id: str):
        """
        Asynchronously returns a dictionary containing information as to the status of
        the given job [ID] and if the job was completed, this dictionary will also
        contain the distribution corresponding to submitted circuit execution.

        Args:
            job_id: ID of the job to retrieve.
        Returns:
            dict: a dictionary with the job data.
        """
        job = None
        try:
            job = self.get_job(job_id)
        except ValueError as err:
            raise err

        while job["status"] not in self.JOB_DONE:
            await asyncio.sleep(60)
            job = self.get_job(job_id)
            if job["status"] in self.JOB_DONE:
                break

        return job

    async def get_jobs_results(self, job_ids: List[str]):
        """
        Asynchronously retrieves a list of jobs corresponding the given job IDs.
        Args:
            job_ids: ID of the job to retrieve.
        Returns:
            List[dict]: a list of dictionaries containing job data.
        """
        jobs = self.get_jobs(job_ids)["jobs"]

        index = 0
        for job in jobs:
            if job["status"] not in self.JOB_DONE:
                job = await self.get_job_results(job["id"])
                jobs[index] = job
            index += 1

        return jobs

    def _run_and_measure(self, circuit: Circuit, n_samples: int) -> Measurements:
        """
        Method for executing the circuit and measuring the outcome.
        Args:
            circuit: quantum circuit to be executed.
            n_samples: The number of samples to measure.
        Returns:
            Measurements: a measurements object holding bitstrings and associated
            measurements
        """

        # Run the circuit
        job_id = self.create_job(circuit, n_samples)

        # Get the result associated with running the circuit inside the job
        job = asyncio.get_event_loop().run_until_complete(self.get_job_results(job_id))
        if job["status"] != "completed":
            raise ValueError(
                "Job with ID <"
                + job_id
                + "> results could not be retrived. The job status is <"
                + job["status"]
                + ">."
            )

        histogram_data = dict(job["data"]["histogram"])

        bitstring_distribution = convert_histogram_data_to_outcome_distribution(
            histogram_data, circuit.n_qubits
        )

        measurements = Measurements().get_measurements_representing_distribution(
            bitstring_distribution, n_samples
        )

        return measurements

    def _run_batch_and_measure(
        self, circuit_set: Sequence[Circuit], n_samples: Sequence[int]
    ) -> List[Measurements]:
        """Run a set of circuits and measure a certain number of bitstrings.

        It may be useful to override this method for backends that support
        batching.
        Args:
            circuit_set: The circuits to execute.
            n_samples: The number of samples to measure for each circuit.
        Returns:
            List[Measurements]: a list of measurements objects holding bitstrings and
            associated measurements for each circuit.
        """
        new_job_ids = []
        for index, circuit in enumerate(circuit_set):
            new_job_ids.append(self.create_job(circuit, n_samples[index]))
        self.job_ids += new_job_ids

        measurements_set = []
        jobs = asyncio.get_event_loop().run_until_complete(
            self.get_jobs_results(new_job_ids)
        )
        index = 0
        while index < len(circuit_set):
            job = jobs[index]
            if job["status"] != "completed":
                warnings.warn(
                    "Job with ID <"
                    + new_job_ids[index]
                    + "> results could not be retrived. The job status is <"
                    + job["status"]
                    + ">."
                )
                index += 1
                continue
            else:
                histogram_data = dict(job["data"]["histogram"])

                bitstring_distribution = convert_histogram_data_to_outcome_distribution(
                    histogram_data, circuit_set[index].n_qubits
                )

                measurements = (
                    Measurements().get_measurements_representing_distribution(
                        bitstring_distribution, n_samples[index]
                    )
                )
                measurements_set.append(measurements)
                index += 1

        return measurements_set


def convert_histogram_data_to_outcome_distribution(histogram_data, number_of_qubits):
    distribution_dict = {}
    for outcome, probability in histogram_data.items():

        bitstring = bin(int(outcome))[2:].zfill(number_of_qubits)[::-1]
        distribution_dict[bitstring] = probability

    return MeasurementOutcomeDistribution(distribution_dict)
