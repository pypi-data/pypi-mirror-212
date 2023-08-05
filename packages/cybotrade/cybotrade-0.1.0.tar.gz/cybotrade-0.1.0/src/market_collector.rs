use ::market_collector::{
    CandleSubscription, CurrencyPair, Exchange, Interval, MarketCollector as MarketCollectorRust,
    MarketCollectorInteractor,
};
use bq_core::domain::exchanges::{Environment, ExchangeCredentials};
use pyo3::{
    exceptions::PyException,
    prelude::*,
    types::{PyDateTime, PyDict, PyList, PyString},
};
use std::{collections::BTreeMap, str::FromStr, sync::Arc};

#[pyclass]
#[derive(Clone)]
struct MarketCollector {
    collector: Arc<MarketCollectorInteractor>,
}

#[pymethods]
impl MarketCollector {
    #[new]
    pub fn __new__<'p>() -> PyResult<Self> {
        Err(PyErr::new::<PyException, _>("call the 'connect' static method to initialise this class, the constructor is not meant to be used."))
    }

    #[staticmethod]
    pub fn connect<'p>(py: Python<'p>, exchanges: &'p PyList) -> PyResult<&'p PyAny> {
        let exchanges = exchanges
            .into_iter()
            .map(|e| {
                let dict = e.downcast::<PyDict>()?;
                let exchange = Exchange::from_str(
                    &dict
                        .get_item("exchange")
                        .ok_or(PyErr::new::<PyException, _>(
                            "exchange must be specified".to_string(),
                        ))?
                        .downcast::<PyString>()?
                        .to_string(),
                )
                .map_err(|e| PyErr::new::<PyException, _>(e.to_string()))?;
                let environment = Environment::from_str(
                    &dict
                        .get_item("environment")
                        .ok_or(PyErr::new::<PyException, _>(
                            "environment must be specified".to_string(),
                        ))?
                        .downcast::<PyString>()?
                        .to_string(),
                )
                .map_err(|e| PyErr::new::<PyException, _>(e.to_string()))?;

                Ok::<_, PyErr>(ExchangeCredentials::from_exchange_public(
                    exchange,
                    environment,
                    None,
                    None,
                    None,
                ))
            })
            .collect::<Result<Vec<_>, _>>()?;
        log::info!("Connecting to exchanges: {:?}", exchanges);

        pyo3_asyncio::tokio::future_into_py(py, async move {
            MarketCollectorRust::new(&exchanges, None, None, None, None)
                .await
                .map_err(|e| PyErr::new::<PyException, _>(e.to_string()))?
                .start()
                .await
                .map(|collector| Self {
                    collector: Arc::new(collector),
                })
                .map_err(|e| PyErr::new::<PyException, _>(e.to_string()))
        })
    }

    pub fn subscribe_candle<'p>(
        &self,
        py: Python<'p>,
        base: &'p PyString,
        quote: &'p PyString,
        interval: &'p PyString,
        exchange: &'p PyString,
        params: Option<&'p PyDict>,
    ) -> PyResult<&'p PyAny> {
        let collector = self.collector.clone();
        let symbol = CurrencyPair::new(base.to_string(), quote.to_string());
        let interval = Interval::from_str(&interval.to_string())
            .map_err(|e| PyErr::new::<PyException, _>(e.to_string()))?;
        let exchange = Exchange::from_str(&exchange.to_string())
            .map_err(|e| PyErr::new::<PyException, _>(e.to_string()))?;
        let params = params.map(|dict| {
            dict.into_iter()
                .map(|(k, v)| (k.to_string(), v.to_string()))
                .collect::<BTreeMap<String, String>>()
        });

        pyo3_asyncio::tokio::future_into_py(py, async move {
            collector
                .subscribe_candle(CandleSubscription {
                    exchanges: vec![(exchange, symbol, interval, params)],
                })
                .await
                .map_err(|e| PyErr::new::<PyException, _>(e.to_string()))
        })
    }

    pub fn listen_candle<'p>(&self, py: Python<'p>) -> PyResult<&'p PyAny> {
        let collector = self.collector.clone();
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let candle = collector
                .listen_candle()
                .await
                .map_err(|e| PyErr::new::<PyException, _>(e.to_string()))?;

            Python::with_gil(|py| {
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
                    PyDateTime::from_timestamp(py, candle.start_time.timestamp() as f64, None)?,
                )?;
                dict.set_item(
                    "end_time",
                    PyDateTime::from_timestamp(py, candle.end_time.timestamp() as f64, None)?,
                )?;

                Ok::<_, PyErr>(dict.to_object(py))
            })
        })
    }
}

#[pymodule]
pub fn market_collector(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<MarketCollector>()?;
    Ok(())
}
