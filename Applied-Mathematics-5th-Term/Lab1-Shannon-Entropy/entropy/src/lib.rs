use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::collections::HashMap;

#[pymodule]
fn entropy(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(analyze_file))
}

#[pyfunction]
fn analyze_file(path: String) -> PyResult<HashMap<String, i32>> {
    let text = std::fs::read_to_string(path)?;
    let chars = text.chars().filter_map(|c| match c {
        _ if c.is_ascii_alphabetic() => Some(c.to_ascii_lowercase()),
        _ if c.is_ascii_punctuation() => Some('.'),
        ' ' => Some(' '),
        _ => None
    });

    let mut frequency = HashMap::new();
    for c in chars {
        *frequency.entry(c.to_string()).or_insert(0) += 1;
    }
    Ok(frequency)
}
