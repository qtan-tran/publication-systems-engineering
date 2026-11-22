# Semantic Module Authoring Guide

A third-party module needs a unique kebab-case id, a semantic namespace, API version, capabilities, capability requirements, compatibility declaration, synthetic fixture, regression test, documentation, and security review. Do not copy backbone code into a module.

Semantic API changes follow semantic versioning. Breaking macro or manifest changes require a major module API migration note. New optional capabilities are minor changes. Fixes that preserve public behavior are patch changes.

A module-specific QA hook must be registered by the PSE runtime; arbitrary executable hook paths are forbidden.
