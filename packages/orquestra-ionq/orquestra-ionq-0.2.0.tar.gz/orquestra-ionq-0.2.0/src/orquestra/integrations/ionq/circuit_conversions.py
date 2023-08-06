from typing import Dict, List, Union

from orquestra.quantum.circuits import Circuit

ORQUESTRA_IONQ_GATE_MAP = {
    "X": "x",
    "Y": "y",
    "Z": "z",
    "S": "s",
    "T": "t",
    "H": "h",
    "S_Dagger": "si",
    "T_Dagger": "ti",
    "RX": "rx",
    "RY": "ry",
    "RZ": "rz",
    "GPi": "gpi",
    "GPi2": "gpi2",
    "XX": "xx",
    "YY": "yy",
    "ZZ": "zz",
    "SWAP": "swap",
    "CNOT": "cnot",
    "MS": "ms",
    "Control": "cnot or toffoli",
}

HAS_TARGET = {
    "X",
    "Y",
    "Z",
    "S",
    "T",
    "H",
    "S_Dagger",
    "T_Dagger",
    "RX",
    "RY",
    "RZ",
    "GPi",
    "GPi2",
    "CNOT",
}

HAS_MULTIPLE_TARGETS = {"XX", "YY", "ZZ", "SWAP", "MS"}

HAS_PHASE = {"RX", "RY", "RZ", "XX", "YY", "ZZ", "GPi", "GPi2"}

HAS_MULTIPLE_PHASES = {"MS"}


IONQ_GATE_TYPE = Dict[str, Union[str, int, List[int]]]
IONQ_CIRCUIT_TYPE = Dict[str, Union[int, str, List[IONQ_GATE_TYPE]]]


def export_to_ionq(circuit: Circuit) -> IONQ_CIRCUIT_TYPE:
    """
    Converts a Circuit object to a IonQ QASM string.
    Args:
        circuit (Circuit): Circuit object to be converted.
    Returns:
        Dict: IonQ circuit dictionary.
    """
    ionq_circuit_dict: IONQ_CIRCUIT_TYPE = {"qubits": circuit.n_qubits}
    ionq_circuit_dict["circuit"] = []
    for implementation in circuit.operations:
        gate = implementation.gate

        if gate.name not in ORQUESTRA_IONQ_GATE_MAP:
            raise NotImplementedError(f"{gate} gate is not supported by IonQ.")

        gate_dict: IONQ_GATE_TYPE = {}
        gate_dict["gate"] = ORQUESTRA_IONQ_GATE_MAP[gate.name]

        if gate.name in HAS_TARGET:
            # -1 here because of the CNOT and Toffoli gates
            gate_dict["target"] = implementation.qubit_indices[-1]
        if gate.name in HAS_MULTIPLE_TARGETS:
            gate_dict["targets"] = list(implementation.qubit_indices)
        if gate.name in HAS_PHASE:
            gate_dict["phase"] = implementation.params[0]
        if gate.name in HAS_MULTIPLE_PHASES:
            gate_dict["phases"] = list(implementation.params)

        # cnot and toffoli gates are special cases
        if gate.name == "CNOT":
            gate_dict["control"] = implementation.qubit_indices[0]
        if gate.name == "Control":
            if gate.wrapped_gate.name == "X" and gate.num_control_qubits == 1:
                gate_dict["gate"] = "cnot"
                gate_dict["control"] = implementation.qubit_indices[0]
                gate_dict["target"] = implementation.qubit_indices[1]
            elif (gate.wrapped_gate.name == "X" and gate.num_control_qubits == 2) or (
                gate.wrapped_gate.name == "CNOT" and gate.num_control_qubits == 1
            ):
                gate_dict["gate"] = "cnot"
                gate_dict["controls"] = list(implementation.qubit_indices[:2])
                gate_dict["target"] = implementation.qubit_indices[2]
            else:
                raise NotImplementedError(f"{gate} gate is not supported by IonQ.")

        ionq_circuit_dict["circuit"].append(gate_dict)  # type: ignore

    return ionq_circuit_dict
