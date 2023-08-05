use std::{str::FromStr, sync::Arc};

use ::datahub::Datahub as DatahubRust;
use ::market_collector::{CurrencyPair, Exchange, Interval};
use chrono::{TimeZone, Utc};
use pyo3::{
    exceptions::PyException,
    prelude::*,
    types::{PyDateAccess, PyDateTime, PyDict, PyList, PyString, PyTimeAccess},
};

#[pyclass]
#[derive(Clone)]
struct Datahub {
    datahub: Arc<DatahubRust>,
}

#[pymethods]
impl Datahub {
    #[new]
    pub fn __new__<'p>() -> PyResult<Self> {
        Err(PyErr::new::<PyException, _>("call the 'connect' static method to initialise this class, the constructor is not meant to be used."))
    }

    #[staticmethod]
    pub fn connect<'p>(py: Python<'p>, url: &'p PyString) -> PyResult<&'p PyAny> {
        let url = url.to_string();
        let datahub = pyo3_asyncio::tokio::future_into_py::<_, Datahub>(py, async move {
            Ok(Datahub {
                datahub: Arc::new(
                    DatahubRust::new(url)
                        .await
                        .map_err(|e| PyErr::new::<PyException, _>(e.to_string()))?,
                ),
            })
        })?;
        Ok(datahub)
    }

    pub fn candle<'p>(
        &self,
        py: Python<'p>,
        base: &'p PyString,
        quote: &'p PyString,
        interval: &'p PyString,
        exchange: &'p PyString,
        start_time: &'p PyDateTime,
        end_time: &'p PyDateTime,
    ) -> PyResult<&'p PyAny> {
        let base = base.to_string();
        let quote = quote.to_string();
        let interval = Interval::from_str(&interval.to_string())
            .map_err(|e| PyErr::new::<PyException, _>(e.to_string()))?;
        let exchange = Exchange::from_str(&exchange.to_string())
            .map_err(|e| PyErr::new::<PyException, _>(e.to_string()))?;
        let start_time = Utc
            .with_ymd_and_hms(
                start_time.get_year(),
                start_time.get_month().into(),
                start_time.get_day().into(),
                start_time.get_hour().into(),
                start_time.get_minute().into(),
                start_time.get_second().into(),
            )
            .unwrap();
        let end_time = Utc
            .with_ymd_and_hms(
                end_time.get_year(),
                end_time.get_month().into(),
                end_time.get_day().into(),
                end_time.get_hour().into(),
                end_time.get_minute().into(),
                end_time.get_second().into(),
            )
            .unwrap();

        let datahub = self.datahub.clone();
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let candles = datahub
                .candle(
                    CurrencyPair::new(base, quote),
                    interval,
                    exchange,
                    start_time,
                    end_time,
                    true,
                )
                .await
                .map_err(|e| PyErr::new::<PyException, _>(e.to_string()))?;

            Python::with_gil(|py| {
                Ok::<_, PyErr>(
                    PyList::new(
                        py,
                        candles
                            .into_iter()
                            .map(|candle| {
                                let symbol = PyDict::new(py);
                                symbol.set_item("base", candle.symbol.base)?;
                                symbol.set_item("quote", candle.symbol.quote)?;

                                let dict = PyDict::new(py);
                                dict.set_item("symbol", symbol)?;
                                dict.set_item("open", candle.open)?;
                                dict.set_item("high", candle.high)?;
                                dict.set_item("low", candle.low)?;
                                dict.set_item("close", candle.close)?;
                                dict.set_item("volume", candle.volume)?;
                                dict.set_item("trade_count", candle.trade_count)?;
                                dict.set_item("is_closed", candle.is_closed)?;
                                dict.set_item("exchange", candle.exchange.to_string())?;
                                dict.set_item(
                                    "start_time",
                                    PyDateTime::from_timestamp(
                                        py,
                                        candle.start_time.timestamp() as f64,
                                        None,
                                    )?,
                                )?;
                                dict.set_item(
                                    "end_time",
                                    PyDateTime::from_timestamp(
                                        py,
                                        candle.end_time.timestamp() as f64,
                                        None,
                                    )?,
                                )?;

                                Ok::<_, PyErr>(dict)
                            })
                            .collect::<Result<Vec<_>, _>>()?,
                    )
                    .to_object(py),
                )
            })
        })
    }
}

#[pymodule]
pub fn datahub(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<Datahub>()?;
    Ok(())
}
