from cybotrade import PythonClass


def test_python_class() -> None:
    py_class = PythonClass(value=10)
    assert py_class.value == 10



def test_doc() -> None:
    import cybotrade

    assert (
        cybotrade.__doc__ == "The main cybotrade module to be exported from Rust to Python."
    )
