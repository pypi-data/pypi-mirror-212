import numpy as np
import pytest
from orquestra.quantum.circuits import SWAP, Circuit, _builtin_gates

from orquestra.integrations.ionq.circuit_conversions import export_to_ionq

ORQUESTRA_IONQ_SINGLE_QUBIT_GATES = [
    (_builtin_gates.X, "x"),
    (_builtin_gates.Y, "y"),
    (_builtin_gates.Z, "z"),
    (_builtin_gates.S, "s"),
    (_builtin_gates.T, "t"),
    (_builtin_gates.H, "h"),
    (_builtin_gates.S.dagger, "si"),
    (_builtin_gates.T.dagger, "ti"),
]

ORQUESTRA_IONQ_SINGLE_QUBIT_GATES_WITH_PARAM = [
    (_builtin_gates.RX, "rx"),
    (_builtin_gates.RY, "ry"),
    (_builtin_gates.RZ, "rz"),
    (_builtin_gates.GPi, "gpi"),
    (_builtin_gates.GPi2, "gpi2"),
]

ORQUESTRA_IONQ_TWO_QUBIT_GATES_WITH_PARAM = [
    (_builtin_gates.XX, "xx"),
    (_builtin_gates.YY, "yy"),
    (_builtin_gates.ZZ, "zz"),
]

ORQUESTRA_IONQ_TWO_QUBIT_GATES_WITH_MULTIPLE_PARAMS = [
    (_builtin_gates.MS, "ms"),
]


@pytest.mark.parametrize("gate, ionq_name", ORQUESTRA_IONQ_SINGLE_QUBIT_GATES)
def test_single_qubit_circuit_conversions(gate, ionq_name):
    """Test the circuit conversions."""
    ionq_circuit = export_to_ionq(Circuit([gate(0)]))

    assert ionq_circuit["circuit"] == [{"gate": ionq_name, "target": 0}]
    assert ionq_circuit["qubits"] == 1


def test_two_qubit_circuit_conversions():
    """Test the circuit conversions."""
    ionq_circuit = export_to_ionq(Circuit([SWAP(0, 1)]))

    assert ionq_circuit["circuit"] == [{"gate": "swap", "targets": [0, 1]}]
    assert ionq_circuit["qubits"] == 2


@pytest.mark.parametrize(
    "gate, ionq_name", ORQUESTRA_IONQ_SINGLE_QUBIT_GATES_WITH_PARAM
)
def test_single_qubit_circuit_conversions_with_param(gate, ionq_name):
    """Test the circuit conversions."""
    ionq_circuit = export_to_ionq(Circuit([gate(np.pi / 8)(0)]))

    assert ionq_circuit["circuit"] == [
        {"gate": ionq_name, "target": 0, "phase": np.pi / 8}
    ]
    assert ionq_circuit["qubits"] == 1


@pytest.mark.parametrize("gate, ionq_name", ORQUESTRA_IONQ_TWO_QUBIT_GATES_WITH_PARAM)
def test_two_qubit_circuit_conversions_with_param(gate, ionq_name):
    """Test the circuit conversions."""
    ionq_circuit = export_to_ionq(Circuit([gate(np.pi / 8)(0, 2)]))

    assert ionq_circuit["circuit"] == [
        {"gate": ionq_name, "targets": [0, 2], "phase": np.pi / 8}
    ]
    assert ionq_circuit["qubits"] == 3


@pytest.mark.parametrize(
    "gate, ionq_name", ORQUESTRA_IONQ_TWO_QUBIT_GATES_WITH_MULTIPLE_PARAMS
)
def test_two_qubit_circuit_conversions_with_multiple_params(gate, ionq_name):
    """Test the circuit conversions."""
    ionq_circuit = export_to_ionq(Circuit([gate(np.pi / 4, np.pi / 8)(0, 2)]))

    assert ionq_circuit["circuit"] == [
        {"gate": ionq_name, "targets": [0, 2], "phases": [np.pi / 4, np.pi / 8]}
    ]
    assert ionq_circuit["qubits"] == 3


@pytest.mark.parametrize(
    "cnot_gate", [_builtin_gates.CNOT, _builtin_gates.X.controlled(1)]
)
def test_cnot_conversion(cnot_gate):
    """Test the circuit conversions."""
    ionq_circuit = export_to_ionq(Circuit([cnot_gate(0, 1)]))

    assert ionq_circuit["circuit"] == [{"gate": "cnot", "control": 0, "target": 1}]
    assert ionq_circuit["qubits"] == 2


@pytest.mark.parametrize(
    "toffoli_gate",
    [_builtin_gates.CNOT.controlled(1), _builtin_gates.X.controlled(2)],
)
def test_toffoli_conversion(toffoli_gate):
    """Test the circuit conversions."""
    ionq_circuit = export_to_ionq(Circuit([toffoli_gate(0, 1, 2)]))

    assert ionq_circuit["circuit"] == [
        {
            "gate": "cnot",
            "controls": [0, 1],
            "target": 2,
        }
    ]

    assert ionq_circuit["qubits"] == 3


def test_only_one_operation_on_greater_than_one_qubit_gives_correct_num_qubits():
    """Test that the correct number of qubits is returned for a circuit with
    multiple qubits and only one operation."""
    ionq_circuit = export_to_ionq(Circuit([_builtin_gates.X(1)]))

    assert ionq_circuit["qubits"] == 2


def test_multiple_operations_on_greater_than_one_qubit_gives_correct_circuit():
    """Test that the correct number of qubits is returned for a circuit with
    multiple qubits and multiple operations."""
    ionq_circuit = export_to_ionq(
        Circuit(
            [
                _builtin_gates.X(0),
                _builtin_gates.RX(np.pi / 8)(1),
                _builtin_gates.CNOT(0, 2),
                _builtin_gates.X.controlled(2)(0, 1, 2),
            ]
        )
    )
    assert ionq_circuit == {
        "qubits": 3,
        "circuit": [
            {"gate": "x", "target": 0},
            {"gate": "rx", "target": 1, "phase": np.pi / 8},
            {"gate": "cnot", "target": 2, "control": 0},
            {"gate": "cnot", "controls": [0, 1], "target": 2},
        ],
    }


def test_nonexistent_gate_throws_notimplemented_error():
    """Test that a NotImplementedError is raised if the gate is not supported."""
    with pytest.raises(NotImplementedError):
        export_to_ionq(Circuit([_builtin_gates.CZ(0, 1)]))


@pytest.mark.parametrize(
    "gate", [_builtin_gates.CNOT.controlled(2), _builtin_gates.X.controlled(3)]
)
def test_too_many_controls_throws_notimplemented_error(gate):
    """Test that a NotImplementedError is raised if the number of controls is
    greater than 2."""
    with pytest.raises(NotImplementedError):
        export_to_ionq(Circuit([gate(0, 1, 2, 3)]))


def test_controll_on_wrong_gate_throws_notimplemented_error():
    """Test that a NotImplementedError is raised if the controlled gate is not
    supported."""
    with pytest.raises(NotImplementedError):
        export_to_ionq(Circuit([_builtin_gates.CZ.controlled(1)(0, 1, 2)]))
