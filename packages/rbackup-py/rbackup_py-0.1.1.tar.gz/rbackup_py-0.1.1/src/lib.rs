use pyo3::{exceptions::PyException, prelude::*};
use rbackup;

#[pyfunction]
#[pyo3(name = "transfer_files")]
fn transfer_files_py(src: &str, dest: &str) -> PyResult<()> {
    if let Err(e) = rbackup::transfer_files(src, dest) {
        return Err(PyException::new_err(e.to_string()));
    }
    Ok(())
}

/// A Python module implemented in Rust.
#[pymodule]
fn rbackup_py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(transfer_files_py, m)?)?;
    Ok(())
}
