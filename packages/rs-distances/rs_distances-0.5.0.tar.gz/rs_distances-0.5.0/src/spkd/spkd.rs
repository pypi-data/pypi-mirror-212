
use ndarray::{Array, Array1, Array3, s, ArrayBase, OwnedRepr, Dim};
use pyo3::{prelude::*, types::PyList};
use numpy::{PyArray3, IntoPyArray, PyArray1};

pub fn iterate_spiketrains(scr: &mut Array3<f64>, sd: &Array3<f64>)  {
    let (num_qvals, num_spikes_xii, num_spikes_xjj) = scr.dim();
    for xii in 1..num_spikes_xii {
        for xjj in 1..num_spikes_xjj {
            for q in 0..num_qvals {
                let a = scr[[q, xii - 1, xjj]] + 1.0;
                let b = scr[[q, xii, xjj - 1]] + 1.0;
                let c = scr[[q, xii - 1, xjj - 1]] + sd[[q, xii - 1, xjj - 1]];

                scr[[q, xii, xjj]] = a.min(b.min(c));
            }
        }
    }
}

#[pyfunction]
fn iterate_spiketrains_impl(py: Python, scr: &PyArray3<f64>, sd: &PyArray3<f64>)  -> PyResult<PyObject> {

    let mut scr: Array3<f64> = scr.to_owned_array();
    let sd: Array3<f64> = sd.to_owned_array();

    iterate_spiketrains(&mut scr, &sd);

    // Convert the result to a PyArray
    let res = scr.into_pyarray(py).to_owned();
    Ok(res.into())
}


pub fn calculate_spkd(cspks: &Vec<Array1<f64>>, qvals: &ArrayBase<OwnedRepr<f64>, Dim<[usize; 3]>>, _res: Option<f64>)  -> ArrayBase<OwnedRepr<f64>, Dim<[usize; 3]>> {

    let numt: usize = cspks.len(); // number of spike trains
    let num_qvals = qvals.len(); // number of q values

    let mut d = Array3::<f64>::zeros((numt, numt, num_qvals));

    for xi in 0..numt - 1 { // if there are 40 spike trains, xi will be 0..39
        for xj in xi + 1..numt { // if there are 40 spike trains, xj will be 1..39

            let curcounts_xi = cspks[xi].len();
            let curcounts_xj = cspks[xj].len();

            if curcounts_xi != 0 && curcounts_xj != 0 {
                let spk_train_a = &cspks[xi];
                let spk_train_b = &cspks[xj];

                let spk_train_a_offset = spk_train_a.clone();
                

                let outer_diff = Array::from_shape_fn((spk_train_a_offset.len(), spk_train_b.len()), |(i, j)| {
                    (spk_train_a_offset[i] - spk_train_b[j]).abs()
                });

                let sd = qvals.broadcast((num_qvals, spk_train_a_offset.len(), spk_train_b.len())).unwrap()
                    .to_owned() * &outer_diff;

                let mut scr = Array::from_elem((num_qvals, curcounts_xi + 1, curcounts_xj + 1), 0.0);
                scr.slice_mut(s![.., 1.., 0]).assign(&(1..=curcounts_xi).map(|x: usize| x as f64).collect::<Array1<_>>());
                scr.slice_mut(s![.., 0, 1..]).assign(&Array::from_shape_fn((1, curcounts_xj), |(_, j)| (j + 1) as f64));

                iterate_spiketrains(&mut scr, &sd);
      
            } else {
                d.slice_mut(s![xi, xj, ..]).fill(curcounts_xi.max(curcounts_xj) as f64);
            }
        }
    }
    d.mapv_into(|val| val.max(0.0))
}

// a function with a signature but without docs. Both blank lines after the `--` are mandatory.

/// sub(a, b, /)
/// --
///
///
#[pyfunction]
fn calculate_spkd_impl(py: Python, cspks: &PyList, qvals: &PyArray1<f64>, res: Option<f64>) -> PyResult<PyObject> {
    let cspks: Vec<Array1<f64>> = cspks.into_iter().map(|pyarray| {
        let numpy_array: &PyArray1<f64> = pyarray.extract()?;
        Ok(numpy_array.to_owned_array())
    }).collect::<PyResult<_>>()?;

    let qvals: Array1<f64> = qvals.to_owned_array();
    let numqvals = qvals.len();
    let q_reshaped = qvals.into_shape((numqvals, 1, 1)).unwrap();

    // Assume calculate_spkd returns ArrayBase<OwnedRepr<f64>, Dim<[usize; 3]>>
    let d = calculate_spkd(&cspks, &q_reshaped, res);
    
    // Convert the ArrayBase to a PyArray
    let py_array = d.into_pyarray(py);

    // Convert the PyArray to a PyObject
    Ok(py_array.to_object(py))
}

#[pymodule]
fn rs_distances(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(calculate_spkd_impl)).unwrap();
    m.add_wrapped(wrap_pyfunction!(iterate_spiketrains_impl)).unwrap();
    Ok(())
}

#[cfg(test)]
mod tests {
    use ndarray::{ArrayBase, OwnedRepr, Dim};

    use super::*;

    #[test]
    fn test_calculate_spkd() {
        // Mock data - list of 1D np.ndarrays, 3 spike trains
        let mut mock_data: Vec<ArrayBase<OwnedRepr<f64>, Dim<[usize; 1]>>> = vec![
        ArrayBase::from(vec![0.1, 0.15, 0.2, 0.25, 0.3]),
        ArrayBase::from(vec![0.35, 0.4, 0.45, 0.5, 0.55]),
        ArrayBase::from(vec![0.6, 0.65, 0.7, 0.75, 0.8]),
    ];
        
        // simulate a view of data given from a numpy spike train
        let qvals = Array1::from(vec![1.0, 2.0, 3.0]);

        let numqvals = qvals.len();
        let q_reshaped = qvals.into_shape((numqvals, 1, 1)).unwrap();

        calculate_spkd(&mut mock_data, &q_reshaped, Option::None);
    }
}