use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::wrap_pymodule;

mod datahub;
mod market_collector;

/// The main cybotrade module to be exported from Rust to Python.
#[pymodule]
fn cybotrade(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    pyo3_log::init();
    m.add_wrapped(wrap_pymodule!(crate::datahub::datahub))?;
    m.add_wrapped(wrap_pymodule!(crate::market_collector::market_collector))?;

    // Inserting to sys.modules allows importing submodules nicely from Python
    // e.g. from cybotrade.datahub import Datahub
    let sys = PyModule::import(py, "sys")?;
    let sys_modules: &PyDict = sys.getattr("modules")?.downcast()?;
    sys_modules.set_item("cybotrade.datahub", m.getattr("datahub")?)?;
    sys_modules.set_item("cybotrade.market_collector", m.getattr("market_collector")?)?;

    Ok(())
}
