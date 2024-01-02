def pytest_addoption(parser):
    parser.addoption(
        "--num_exercicio",
        action="append",
        default=[],
        help="número do exercicio",
    )

def pytest_generate_tests(metafunc):
    metafunc.parametrize("num_exercicio", metafunc.config.getoption("num_exercicio"))
    