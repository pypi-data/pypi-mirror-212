mod signal_generator;
mod signal_type;

use pyo3::prelude::*;

#[pymodule]
fn can_message_data_generator(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<signal_type::SignalType>()?;
    m.add_class::<signal_generator::SignalGenerator>()?;
    m.add_function(wrap_pyfunction!(signal_generator::get_max_limit, m)?)?;
    m.add_function(wrap_pyfunction!(signal_generator::get_min_limit, m)?)?;
    Ok(())
}
