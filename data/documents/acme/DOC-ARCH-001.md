# DOC-ARCH-001 — Acme Architecture Overview

SYNTHETIC DOCUMENT — Acme Financial Services

Acme runs a hybrid estate: Java and .NET line-of-business systems, a Python risk stack,
SQL Server and Oracle data platforms, Redis caching, IBM MQ for payments events,
Kafka for risk/notification streams, and a mainframe adapter for core banking.

Identity Platform (APP-IDP-001) is a critical shared dependency for customer-facing and payment flows.
Payment Processing and Loan Processing both depend on the Legacy Mainframe Adapter for settlement and account posting.
