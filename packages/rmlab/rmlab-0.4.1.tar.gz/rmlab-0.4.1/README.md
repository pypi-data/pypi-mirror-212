# RMLab Python Client

This client provides python bindings for RMLab services at **[rmlab.ai](https://rmlab.ai)**, available upon registration.

We offer *simulation* and *revenue optimization* services to airline companies.

**Simulation as a service:**

* Unlimited number of competing carriers.

* Massively parallel simulations on arbitrarily big flight markets.

* Statistical sampling for modelling customers behavior, sensible to seasonality and events.

* Validation of pricing algorithms given demand patterns before deploying to production.


**Revenue optimization as a service:**

* Process arbitrarily large sets of historic data.

* Run state-of-the-art algorithms for forecasting and optimization.

* Fine-grain optimization per flight level.

* AI-based adaptive forecasters & optimizers operating on nightly runs.


**Server infrastructure characteristics:**

* World-wide availability hosted in **[Google Cloud Platform](https://cloud.google.com)**.

* Data scalability across high-performance in-memory storage servers.

* Per-customer fully isolated compute and data environments.

* End-to-end TLS encryption (optional IPsec access).

## TODO

Gitlab CI is compiling the mkdocs project into public/ artifact, but it is not yet visible.

We could build the proxy from both the web-app and this docs artifact or docker image to serve it for rmlab.ai/client-doc
