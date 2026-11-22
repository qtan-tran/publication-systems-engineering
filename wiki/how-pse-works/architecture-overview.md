---
title: How PSE works
description: Understand the core, profiles, semantic modules, and presentation layers in PSE.
---

# Architecture overview

PSE separates three concerns: the shared **core**, reusable **semantic modules**, and publication-type **profiles**. Project configuration chooses which supported features are active for a particular book.

A semantic module owns meaning and stable data. A profile owns presentation. For example, contributor identity is reusable semantic data; the way contributor names appear beneath an edited-volume chapter title belongs to the edited-collection profile.

For the detailed developer contract, see `/docs/architecture/`.
