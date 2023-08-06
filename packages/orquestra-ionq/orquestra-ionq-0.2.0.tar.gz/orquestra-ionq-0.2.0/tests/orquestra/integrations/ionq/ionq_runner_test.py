import asyncio
import os

import numpy as np
import pytest
from orquestra.quantum.api.circuit_runner_contracts import CIRCUIT_RUNNER_CONTRACTS
from orquestra.quantum.circuits import (
    CNOT,
    MS,
    RX,
    RY,
    RZ,
    SWAP,
    XX,
    YY,
    ZZ,
    Circuit,
    GPi,
    GPi2,
    H,
    S,
    T,
    X,
    Y,
    Z,
)

from orquestra.integrations.ionq import IonQRunner


@pytest.fixture
def ionq_runner():
    api_key = os.getenv("ZAPATA_IONQ_API_TOKEN")
    return IonQRunner(api_key, "simulator", seed=42)


@pytest.fixture
def noisy_ionq_runner():
    api_key = os.getenv("ZAPATA_IONQ_API_TOKEN")
    return IonQRunner(api_key, "simulator", noise_model="harmony", seed=42)


@pytest.fixture
def native_ionq_runner():
    api_key = os.getenv("ZAPATA_IONQ_API_TOKEN")
    return IonQRunner(
        api_key, "simulator", use_native_gates=True, noise_model="harmony", seed=42
    )


@pytest.mark.parametrize("contract", CIRCUIT_RUNNER_CONTRACTS)
def test_ibmq_runner_fulfills_circuit_runner_contracts(ionq_runner, contract):
    assert contract(ionq_runner)


def test_create_job(ionq_runner):
    circ = Circuit([H(0)])
    job_id = ionq_runner.create_job(circ, 100)
    assert job_id != ""


def test_get_job(ionq_runner):
    circ = Circuit([H(0)])
    job_id = ionq_runner.create_job(circ, 100)
    response = ionq_runner.get_job(job_id)
    assert response["id"] == job_id


def test_get_jobs(ionq_runner):
    circ = Circuit([H(0)])
    job_id_1 = ionq_runner.create_job(circ, 100)
    job_id_2 = ionq_runner.create_job(circ, 100)
    response = ionq_runner.get_jobs([job_id_1, job_id_2])
    jobs = response["jobs"]
    assert len(jobs) == 2
    for job in jobs:
        assert job["id"] in ionq_runner.job_ids


def test_cancel_job(ionq_runner):
    circ = Circuit([H(0)])
    job_id = ionq_runner.create_job(circ, 100)
    response = ionq_runner.cancel_job(job_id)
    assert response["id"] == job_id
    assert response["status"] == "canceled"


def test_delete_job(ionq_runner):
    circ = Circuit([H(0)])
    job_id = ionq_runner.create_job(circ, 100)
    response = ionq_runner.delete_job(job_id)
    assert response["id"] == job_id
    assert response["status"] == "deleted"


def test_get_job_results(ionq_runner):
    circ = Circuit([H(0)])
    job_id = ionq_runner.create_job(circ, 100)
    job = asyncio.get_event_loop().run_until_complete(
        ionq_runner.get_job_results(job_id)
    )
    assert job["id"] == job_id


def test_get_jobs_results(ionq_runner):
    circ = Circuit([H(0)])
    job_id_1 = ionq_runner.create_job(circ, 100)
    job_id_2 = ionq_runner.create_job(circ, 100)
    jobs = asyncio.get_event_loop().run_until_complete(
        ionq_runner.get_jobs_results([job_id_1, job_id_2])
    )
    assert len(jobs) == 2
    for job in jobs:
        assert job["id"] in ionq_runner.job_ids


def test_run_and_measure_n_samples(ionq_runner):
    n_samples = 100 + 1
    circ = Circuit([H(0), CNOT(0, 1)])
    measurements = ionq_runner.run_and_measure(circ, n_samples)
    assert len(measurements.bitstrings) == n_samples


def test_run_and_measure_gives_expected_distribution(ionq_runner):
    n_samples = 100
    circ = Circuit([H(0), CNOT(0, 1)])
    measurements = ionq_runner.run_and_measure(circ, n_samples)
    assert len(measurements.bitstrings) == n_samples

    distribution = measurements.get_distribution()
    assert distribution.distribution_dict[(0, 0)] == 0.5
    assert distribution.distribution_dict[(1, 1)] == 0.5


def test_run_batch_and_measure_n_samples(ionq_runner):
    circ = Circuit([H(0), CNOT(0, 1)])
    circuitset = (circ,) * 2
    n_samples = [100 + 1, 100 + 2]
    measurements_set = ionq_runner.run_batch_and_measure(circuitset, n_samples)
    for index in (0, 1):
        assert len(measurements_set[index].bitstrings) == n_samples[index]


def test_noisy_run_and_measure_gives_expected_distribution(noisy_ionq_runner):
    n_samples = 100
    circ = Circuit([H(0), CNOT(0, 1)])
    measurements = noisy_ionq_runner.run_and_measure(circ, n_samples)
    assert len(measurements.bitstrings) == n_samples

    distribution = measurements.get_distribution()
    assert distribution.distribution_dict[(0, 0)] == 0.34
    assert distribution.distribution_dict[(1, 0)] == 0.02
    assert distribution.distribution_dict[(1, 1)] == 0.64


def test_circuit_with_all_gates_works(ionq_runner):
    n_samples = 1000
    circ = Circuit(
        [
            X(0),
            Y(0),
            Z(0),
            S(0),
            T(0),
            S.dagger(0),
            T.dagger(0),
            H(0),
            CNOT(0, 1),
            RX(np.pi / 8)(0),
            RY(np.pi / 8)(0),
            RZ(np.pi / 8)(0),
            XX(np.pi / 8)(0, 1),
            YY(np.pi / 8)(0, 1),
            ZZ(np.pi / 8)(0, 1),
            SWAP(0, 1),
            X.controlled(1)(0, 1),
            X.controlled(2)(0, 1, 2),
        ]
    )

    measurements = ionq_runner.run_and_measure(circ, n_samples)

    distribution = measurements.get_distribution()
    assert distribution.distribution_dict[(0, 0, 1)] == 0.5
    assert distribution.distribution_dict[(1, 0, 1)] == 0.5


def test_circuit_with_native_gates_works(native_ionq_runner):
    n_samples = 1000
    circ = Circuit(
        [
            GPi(np.pi / 8)(0),
            GPi2(np.pi / 8)(0),
            MS(np.pi / 8, np.pi / 16)(0, 1),
        ]
    )

    measurements = native_ionq_runner.run_and_measure(circ, n_samples)

    assert len(measurements.bitstrings) == n_samples
    distribution = measurements.get_distribution()
    assert distribution.distribution_dict[(0, 0)] == 0.267
    assert distribution.distribution_dict[(0, 1)] == 0.255
    assert distribution.distribution_dict[(1, 0)] == 0.224
    assert distribution.distribution_dict[(1, 1)] == 0.254


def test_bad_api_token_raises_error():
    with pytest.raises(ValueError):
        IonQRunner("bad_token", "simulator").run_and_measure(Circuit([X(0)]), 1)


def test_empty_api_token_raises_error():
    with pytest.raises(ValueError):
        IonQRunner("", "simulator").run_and_measure(Circuit([X(0)]), 1)


def test_non_native_gates_on_native_simulator(native_ionq_runner):
    with pytest.raises(ValueError):
        native_ionq_runner.run_and_measure(Circuit([X.controlled(1)(0, 1)]), 1)


def test_native_gates_on_qip_simulator(ionq_runner):
    with pytest.raises(ValueError):
        ionq_runner.run_and_measure(Circuit([GPi(1)(0, 1)]), 1)


def test_unsupported_noise_models_throws_error():
    with pytest.raises(ValueError):
        IonQRunner("token", "qpu.harmony", noise_model="harmony")


def test_get_jobs_fails_with_bad_job_id(ionq_runner):
    with pytest.raises(ValueError) as e_info:
        ionq_runner.get_job("bad_id")
    assert e_info.value.args[0] == "Job with id <bad_id> not found after 3 trials."
