use itertools::Itertools;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::wrap_pyfunction;
use std::collections::HashMap;

#[pymodule]
fn entropy(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(letter_frequencies))?;
    m.add_wrapped(wrap_pyfunction!(letter_pair_frequencies))?;
    m.add_wrapped(wrap_pyfunction!(frequencies_to_probabilities))
}

#[pyfunction]
fn letter_frequencies(path: &str) -> PyResult<HashMap<String, i32>> {
    let mut frequency = HashMap::new();
    let text = std::fs::read_to_string(path)?;
    for c in iterate_text_chars(&text) {
        *frequency.entry(c.to_string()).or_insert(0) += 1;
    }
    Ok(frequency)
}

#[pyfunction]
fn letter_pair_frequencies(path: &str) -> PyResult<HashMap<String, i32>> {
    let mut frequency = HashMap::new();
    let text = std::fs::read_to_string(path)?;
    for (c1, c2) in iterate_text_chars(&text).tuple_windows() {
        if c1 != ' ' && c1 != '.' && c2 != ' ' && c2 != '.' {
            *frequency.entry(format!("{}{}", c1, c2)).or_insert(0) += 1;
        }
    }
    Ok(frequency)
}

fn iterate_text_chars<'t>(text: &'t str) -> impl Iterator<Item = char> + 't {
    text.chars().filter_map(|c| match c {
        _ if c.is_ascii_alphabetic() => Some(c.to_ascii_lowercase()),
        _ if c.is_ascii_punctuation() => Some('.'),
        ' ' => Some(' '),
        _ => None,
    })
}

#[pyfunction]
fn frequencies_to_probabilities(py: Python, freq_dict: PyObject) -> PyResult<PyObject> {
    let freqs = freq_dict.cast_as::<PyDict>(py)?;
    let sum = freqs.values().iter().fold(0.0, |sum, v| {
        v.extract::<f32>().map(|freq| sum + freq).unwrap_or(sum)
    });

    let probabilities = PyDict::new(py);
    for (k, freq) in freqs.iter() {
        probabilities.set_item(k, freq.extract::<f32>()? / sum)?;
    }
    Ok(probabilities.to_object(py))
}
