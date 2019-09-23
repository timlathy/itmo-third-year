use itertools::Itertools;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::collections::{BTreeMap, HashMap};

#[pymodule]
fn entropy(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(letter_probabilities))?;
    m.add_wrapped(wrap_pyfunction!(letter_pair_probabilities))
}

#[pyfunction]
fn letter_probabilities(path: &str) -> PyResult<BTreeMap<String, f32>> {
    let text = std::fs::read_to_string(path)?;

    let mut total_num_chars = 0usize;
    let mut frequency_map = HashMap::new();
    for c in iterate_text_chars(&text) {
        total_num_chars += 1;
        *frequency_map.entry(c).or_insert(0) += 1;
    }

    Ok(frequency_map
        .into_iter()
        .map(|(c, freq)| (c.to_string(), freq as f32 / total_num_chars as f32))
        .collect())
}

#[pyfunction]
fn letter_pair_probabilities(path: &str) -> PyResult<BTreeMap<String, f32>> {
    let text = std::fs::read_to_string(path)?;

    let mut total_num_pairs = 0usize;
    let mut frequency_map = HashMap::new();
    for (c1, c2) in iterate_text_chars(&text).tuple_windows() {
        if c1 != ' ' && c1 != '.' && c2 != ' ' && c2 != '.' {
            total_num_pairs += 1;
            *frequency_map.entry(format!("{}{}", c1, c2)).or_insert(0) += 1;
        }
    }

    Ok(frequency_map
        .into_iter()
        .map(|(pair, freq)| (pair, freq as f32 / total_num_pairs as f32))
        .collect())
}

fn iterate_text_chars<'t>(text: &'t str) -> impl Iterator<Item = char> + 't {
    text.chars().filter_map(|c| match c {
        _ if c.is_ascii_alphabetic() => Some(c.to_ascii_lowercase()),
        _ if c.is_ascii_punctuation() => Some('.'),
        ' ' => Some(' '),
        _ => None,
    })
}
