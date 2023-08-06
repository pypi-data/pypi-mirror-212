include subtrees/z_quantum_actions/Makefile

github_actions:
	${PYTHON_EXE} -m venv ${VENV_NAME}
	"${VENV_NAME}/${VENV_BINDIR}/${PYTHON_EXE}" -m pip install --upgrade pip
	"${VENV_NAME}/${VENV_BINDIR}/${PYTHON_EXE}" -m pip install -e ./orquestra-quantum
	"${VENV_NAME}/${VENV_BINDIR}/${PYTHON_EXE}" -m pip install -e '.[dev]'